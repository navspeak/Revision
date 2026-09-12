"""
BASIC AGENT LOOP — complete and self-contained.

Every function is defined in this file. Nothing is hidden.

Run it:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python basic_agent_loop.py

Then run it again with USE_OBSERVE = False (line 34) to watch it break.
"""

import json
from anthropic import Anthropic

client = Anthropic()          # reads ANTHROPIC_API_KEY from the environment

MODEL     = "claude-sonnet-5"
MAX_STEPS = 5                 # hard cap so a broken loop can't run forever
USE_OBSERVE = True            # <-- flip to False to see why observe exists


# =====================================================================
# PART 1 — THE TOOL
#
# This is ordinary Python. It has no idea an LLM exists.
# =====================================================================

WEATHER_DB = {
    "Toronto":   {"temp_c": 19, "condition": "cloudy"},
    "Vancouver": {"temp_c": 23, "condition": "sunny"},
    "Montreal":  {"temp_c": 17, "condition": "rain"},
}


def get_weather(city):
    """Return current weather for a city. Raises if the city is unknown."""
    if city not in WEATHER_DB:
        raise ValueError(f"'{city}' is not a city I have data for.")
    return WEATHER_DB[city]


# =====================================================================
# PART 2 — THE TWO LISTS THAT DESCRIBE THAT TOOL
#
# You maintain BOTH of these by hand. Nothing generates one from
# the other. They must stay in sync.
# =====================================================================

# 2a. What the MODEL sees. Sent over HTTP as JSON.
TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": (
            "Get the current weather for a city. "
            "Use ONLY for questions about weather, temperature, or forecast "
            "in a geographic location. Do NOT use for questions about people, "
            "dates, or definitions — answer those directly."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of a real city, e.g. 'Toronto'.",
                }
            },
            "required": ["city"],
        },
    }
]

# 2b. What PYTHON sees. Maps the string name -> the actual function object.
#     Note: no parentheses. We store the function, we don't call it.
TOOL_REGISTRY = {
    "get_weather": get_weather,
}


# =====================================================================
# PART 3 — THE THREE STEPS
# =====================================================================

def think(messages):
    """
    ONE HTTP call to the model.

    Sends the ENTIRE messages list every time, because the API is
    stateless — the server remembers nothing between calls.

    Returns the raw response object.
    """
    return client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=messages,
        tools=TOOL_SCHEMAS,
        # tool_choice defaults to {"type": "auto"} — the model decides.
    )


def act(block):
    """
    Run ONE tool the model asked for.

    `block` is a tool_use block from the response, shaped like:
        block.name  == "get_weather"          (a STRING)
        block.input == {"city": "Toronto"}    (a dict)
        block.id    == "toolu_01A..."         (needed later by observe)

    Returns whatever the tool returned, or an error dict if it blew up.
    """
    fn = TOOL_REGISTRY.get(block.name)

    if fn is None:
        return {"error": f"No tool named '{block.name}'. "
                         f"Available: {list(TOOL_REGISTRY)}"}

    try:
        # ** turns dict keys into keyword arguments:
        #     fn(**{"city": "Toronto"})  ==  get_weather(city="Toronto")
        # This is why schema property names must match parameter names.
        return fn(**block.input)
    except Exception as e:
        # Return the error instead of crashing. observe() will hand it
        # back to the model, which can then recover.
        return {"error": f"{type(e).__name__}: {e}"}


def observe(messages, results):
    """
    Write tool results back into `messages` so the model can see them.

    THIS IS THE ONLY DOOR between your Python variables and the
    model's memory. Skip it and the model never learns anything.

    `results` is a list of (tool_use_id, result) pairs. All results
    from one assistant turn go into ONE user message — the API
    requires that.
    """
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_id,     # MUST match block.id exactly
                "content": json.dumps(result),  # must be a string
            }
            for tool_use_id, result in results
        ],
    })


# =====================================================================
# PART 4 — THE LOOP
# =====================================================================

def run_agent(question):
    # The list starts with exactly one thing: the user's question.
    messages = [{"role": "user", "content": question}]

    print(f"\nQUESTION: {question}")
    dump(messages, "start")

    for step in range(MAX_STEPS):
        print(f"\n{'='*62}\nITERATION {step}\n{'='*62}")

        # ---- THINK -------------------------------------------------
        print(f"  think() -> sending {len(messages)} messages")
        response = think(messages)
        print(f"  think() <- stop_reason = {response.stop_reason!r}")

        # APPEND #1: record what the model said (its own assistant turn).
        # This happens whether or not tools were used.
        messages.append({"role": "assistant", "content": response.content})
        dump(messages, "after appending assistant turn")

        # ---- EXIT CHECK --------------------------------------------
        if response.stop_reason != "tool_use":
            text = "".join(b.text for b in response.content if b.type == "text")
            print(f"\n  stop_reason is not 'tool_use' -> EXIT\n")
            return text

        # ---- ACT ---------------------------------------------------
        # There can be MORE THAN ONE tool_use block in a single turn.
        tool_blocks = [b for b in response.content if b.type == "tool_use"]
        results = []

        for block in tool_blocks:
            print(f"  act()   -> {block.name}({block.input})")
            result = act(block)
            print(f"  act()   <- {result}")
            results.append((block.id, result))

        # ---- OBSERVE -----------------------------------------------
        # APPEND #2: write those results into messages.
        if USE_OBSERVE:
            observe(messages, results)
            dump(messages, "after observe")
        else:
            print("  observe() SKIPPED — results discarded, model never sees them")

    print(f"\n  hit MAX_STEPS ({MAX_STEPS}) without an answer\n")
    return None


# =====================================================================
# PART 5 — A PRINTER, so you can SEE the list
# =====================================================================

def dump(messages, label):
    """Print the messages list in a readable one-line-per-message form."""
    print(f"\n  --- messages  len={len(messages)}   ({label})")
    for i, m in enumerate(messages):
        role = m["role"]
        content = m["content"]

        if isinstance(content, str):                 # plain text message
            body = f'"{content}"'
        else:                                        # list of blocks
            parts = []
            for b in content:
                btype = b["type"] if isinstance(b, dict) else b.type
                if btype == "text":
                    txt = b["text"] if isinstance(b, dict) else b.text
                    parts.append(f'text("{txt[:40]}...")')
                elif btype == "tool_use":
                    name = b["name"] if isinstance(b, dict) else b.name
                    inp  = b["input"] if isinstance(b, dict) else b.input
                    bid  = b["id"] if isinstance(b, dict) else b.id
                    parts.append(f"tool_use[{bid[-4:]}]({name}, {inp})")
                elif btype == "tool_result":
                    parts.append(f"tool_result[{b['tool_use_id'][-4:]}] "
                                 f"= {b['content']}")
                else:
                    parts.append(btype)
            body = " + ".join(parts)

        print(f"  [{i}] {role:<9} {body}")
    print()


# =====================================================================
# PART 6 — RUN IT
# =====================================================================

if __name__ == "__main__":
    answer = run_agent(
        "Is it warmer in Toronto or Vancouver right now, and by how much?"
    )
    print("=" * 62)
    print(f"FINAL ANSWER: {answer}")
    print("=" * 62)