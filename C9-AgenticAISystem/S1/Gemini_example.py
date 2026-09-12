"""
BASIC AGENT LOOP — GEMINI VERSION (free tier)

Same program as basic_agent_loop.py, rewritten for Google's Gemini API.
Every function is defined here. Nothing is hidden.

SETUP
    1. Get a free key at https://aistudio.google.com/apikey  (no credit card)
    2. pip install "google-genai<3.0.0"
    3. export GEMINI_API_KEY=...        (Windows: set GEMINI_API_KEY=...)
    4. python basic_agent_loop_gemini.py

Then flip USE_OBSERVE to False (line 40) to watch it break.

NOTE ON THE FREE TIER
    Free tier is Flash-only. gemini-3.5-flash works and has generous limits.
    If you hit a 429, wait a minute — free tier is rate-limited per minute
    and per day. MAX_STEPS is your protection against burning quota.
"""

import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".env",
    override=True
)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# embeddings and the vector DB run locally and need no key; the key is for
# generation in 2.2 and the Ragas judge in 3.1
print("GOOGLE_API_KEY loaded:", bool(GOOGLE_API_KEY))

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

MODEL       = "gemini-3.5-flash"   # free tier. gemini-2.0-flash also works.
MAX_STEPS   = 5
USE_OBSERVE = True                 # <-- flip to False to see why observe exists


# =====================================================================
# PART 1 — THE TOOL
#
# Identical to the Anthropic version. Plain Python. Knows nothing
# about any LLM. This part never changes between providers.
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
# Same idea as Anthropic, different class names.
# =====================================================================

# 2a. What the MODEL sees.
#     Anthropic used a plain dict; Gemini uses FunctionDeclaration objects
#     wrapped in a Tool. The inner JSON schema is identical in shape.
WEATHER_DECLARATION = types.FunctionDeclaration(
    name="get_weather",
    description=(
        "Get the current weather for a city. "
        "Use ONLY for questions about weather, temperature, or forecast "
        "in a geographic location. Do NOT use for questions about people, "
        "dates, or definitions — answer those directly."
    ),
    parameters_json_schema={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of a real city, e.g. 'Toronto'.",
            }
        },
        "required": ["city"],
    },
)

TOOLS = [types.Tool(function_declarations=[WEATHER_DECLARATION])]

# 2b. What PYTHON sees. Identical to the Anthropic version.
TOOL_REGISTRY = {
    "get_weather": get_weather,
}


# =====================================================================
# PART 3 — THE THREE STEPS
# =====================================================================

def think(contents):
    """
    ONE HTTP call to the model.

    Gemini calls the history `contents` instead of `messages`, and the
    roles are "user" / "model" instead of "user" / "assistant".

    IMPORTANT: automatic_function_calling is DISABLED. Left on, the SDK
    runs the entire agent loop for you internally — it calls your Python
    function, feeds the result back, and returns only the final answer.
    Convenient in production, useless for learning. We turn it off so
    every step is visible.
    """
    return client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            tools=TOOLS,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
            # tool_config default is AUTO — the model decides.
        ),
    )


def wants_tools(response):
    """
    Detect whether the model asked for a tool.

    THIS IS THE BIG DIFFERENCE FROM ANTHROPIC.

    Anthropic gives you a flag:      response.stop_reason == "tool_use"
    Gemini gives you nothing.        finish_reason is "STOP" even when
                                     function calls are present.

    So you must SCAN THE CONTENT. Gemini's finish_reason enum has no
    tool-use value at all (STOP, MAX_TOKENS, SAFETY, RECITATION,
    MALFORMED_FUNCTION_CALL, ...). Checking it for tool use will never work.

    Also: never assume the function_call is the last part. Iterate.
    """
    calls = []
    for part in response.candidates[0].content.parts:
        if getattr(part, "function_call", None):
            calls.append(part.function_call)
    return calls


def act(call):
    """
    Run ONE function the model asked for.

    `call` is a FunctionCall:
        call.name == "get_weather"           (a STRING)
        call.args == {"city": "Toronto"}     (a dict-like)

    Note there is NO id field to track, unlike Anthropic's block.id.
    Gemini matches results to calls by function NAME.
    """
    fn = TOOL_REGISTRY.get(call.name)

    if fn is None:
        return {"error": f"No tool named '{call.name}'. "
                         f"Available: {list(TOOL_REGISTRY)}"}

    try:
        # ** turns dict keys into keyword arguments, same as before.
        # dict(call.args) because args is a proto map, not a plain dict.
        return fn(**dict(call.args))
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def observe(contents, results):
    """
    Write function results back into `contents` so the model can see them.

    STILL THE ONLY DOOR between your Python variables and the model's
    memory. The concept is identical to Anthropic; only the wrapper differs.

        Anthropic:  {"role": "user", "content": [{"type": "tool_result", ...}]}
        Gemini:     types.Content(role="user",
                                  parts=[Part.from_function_response(...)])

    `results` is a list of (function_name, result) pairs. All results from
    one model turn go into ONE Content, same as Anthropic.

    from_function_response requires `response` to be a dict, not a string.
    """
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"result": result},   # must be a dict
                )
                for name, result in results
            ],
        )
    )


# =====================================================================
# PART 4 — THE LOOP
#
# Structurally identical to the Anthropic version.
# =====================================================================

def run_agent(question):
    # The history starts with exactly one thing: the user's question.
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=question)])
    ]

    print(f"\nQUESTION: {question}")
    dump(contents, "start")

    for step in range(MAX_STEPS):
        print(f"\n{'='*62}\nITERATION {step}\n{'='*62}")

        # ---- THINK -------------------------------------------------
        print(f"  think() -> sending {len(contents)} contents")
        response = think(contents)
        finish = response.candidates[0].finish_reason
        print(f"  think() <- finish_reason = {finish!r}   <-- note: STOP even "
              f"when tools are called")

        # APPEND #1: record the model's turn.
        #
        # We append response.candidates[0].content VERBATIM rather than
        # rebuilding it by hand. This matters: on Gemini 3 models, parts
        # can carry thought signatures that are MANDATORY to pass back
        # for function calling. Appending the object as-is preserves them.
        model_turn = response.candidates[0].content
        contents.append(model_turn)
        dump(contents, "after appending model turn")

        # ---- EXIT CHECK --------------------------------------------
        # Content-based, NOT finish_reason-based. See wants_tools().
        calls = wants_tools(response)

        if not calls:
            text = "".join(
                p.text for p in model_turn.parts if getattr(p, "text", None)
            )
            print(f"\n  no function_call parts found -> EXIT\n")
            return text

        # ---- ACT ---------------------------------------------------
        results = []
        for call in calls:
            print(f"  act()   -> {call.name}({dict(call.args)})")
            result = act(call)
            print(f"  act()   <- {result}")
            results.append((call.name, result))

        # ---- OBSERVE -----------------------------------------------
        # APPEND #2.
        if USE_OBSERVE:
            observe(contents, results)
            dump(contents, "after observe")
        else:
            print("  observe() SKIPPED — results discarded, model never sees them")

    print(f"\n  hit MAX_STEPS ({MAX_STEPS}) without an answer\n")
    return None


# =====================================================================
# PART 5 — A PRINTER, so you can SEE the list
# =====================================================================

def dump(contents, label):
    """Print the contents list, one line per Content."""
    print(f"\n  --- contents  len={len(contents)}   ({label})")
    for i, c in enumerate(contents):
        descs = []
        for p in (c.parts or []):
            if getattr(p, "function_call", None):
                fc = p.function_call
                descs.append(f"function_call({fc.name}, {dict(fc.args)})")
            elif getattr(p, "function_response", None):
                fr = p.function_response
                descs.append(f"function_response({fr.name}) = {fr.response}")
            elif getattr(p, "text", None):
                descs.append(f'text("{p.text[:45]}...")')
        print(f"  [{i}] {c.role:<6} {' + '.join(descs) or '<empty>'}")
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