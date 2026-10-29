"""Stand-in for `copilot -p "<prompt>"` used by the tests. Not part of the real app.

Environment switches:
  FAKE_COPILOT_FAIL=1   exit with an error
  FAKE_COPILOT_LOG=path write each received prompt to this file (appended)
  FAKE_COPILOT_NOISE=1  print stats-like noise around the reply
"""
import os
import re
import sys


def main() -> int:
    args = sys.argv[1:]
    prompt = ""
    if "-p" in args:
        prompt = args[args.index("-p") + 1]

    log = os.environ.get("FAKE_COPILOT_LOG")
    if log:
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(prompt + "\n=====END=====\n")

    if os.environ.get("FAKE_COPILOT_FAIL") == "1":
        sys.stderr.write("fake copilot: simulated failure\n")
        return 2

    reply = respond(prompt)
    if os.environ.get("FAKE_COPILOT_NOISE") == "1":
        print("* Thinking...")
        print(reply)
        print("\nTotal usage est: 1 Premium request")
    else:
        print(reply)
    return 0


def respond(prompt: str) -> str:
    if "You convert a document written by a Jira user" in prompt:
        return doc_to_skills(prompt)
    if "Draft a reusable Jira Bot skill from this conversation" in prompt:
        return skill_from_chat(prompt)
    if "Draft a reusable Jira Bot agent from this conversation" in prompt:
        return (
            "<agent><name>triage-assistant</name><description>Weekly bug triage helper</description>"
            "<instructions>Group by priority. Call out unassigned and stale bugs.</instructions>"
            "<skills>open-bugs</skills><default name=\"project\">ABC</default></agent>"
        )
    if "Summarise Jira query results" in prompt:
        return "<jirabot><message>- 3 bugs, 1 high priority\n- 1 unassigned\nNext: assign the unassigned bug.</message></jirabot>"
    if prompt.strip().lower().startswith("reply with the single word ok"):
        return "OK"
    return chat(prompt)


def doc_to_skills(prompt: str) -> str:
    doc = prompt.split("<document>", 1)[-1]
    m_existing = re.search(r"Avoid these existing names: (.*)", prompt)
    taken = {n.strip() for n in (m_existing.group(1).split(",") if m_existing else [])}
    out = []
    counter = 0
    for m in re.finditer(r"(project\s*=\s*[^\n`]+)", doc):
        jql = m.group(1).strip().rstrip(".")
        jql = re.sub(r"project\s*=\s*\w+", "project = {project}", jql, count=1)
        counter += 1
        while f"doc-skill-{counter}" in taken:
            counter += 1
        name = f"doc-skill-{counter}"
        taken.add(name)
        out.append(
            f"<skill><name>{name}</name><description>From a document</description>"
            f"<jql>{jql}</jql><param name=\"project\" default=\"ABC\">Project key</param>"
            f"<notes>Extracted by fake copilot</notes></skill>"
        )
    return "\n".join(out) or "I found nothing."


def skill_from_chat(prompt: str) -> str:
    m = re.search(r"most recent: ([^)]+)\)", prompt)
    jql = m.group(1) if m else "project = {project} AND statusCategory != Done"
    jql = re.sub(r"project\s*=\s*\w+", "project = {project}", jql, count=1)
    name = "bug-triage-weekly"
    m2 = re.search(r'suggested the name "([^"]+)"', prompt)
    if m2:
        name = m2.group(1)
    return (
        f"<skill><name>{name}</name><description>Weekly bug triage</description><jql>{jql}</jql>"
        f"<param name=\"project\" default=\"ABC\">Jira project key</param>"
        f"<output>Group by priority.</output></skill>"
    )


def chat(prompt: str) -> str:
    convo = prompt.split("CONVERSATION SO FAR:", 1)[-1]
    users = re.findall(r"^User: (.*)$", convo, re.M)
    last = users[-1] if users else ""
    low = last.lower()

    skill_names = re.findall(r"^- ([a-z0-9_-]+) - ", prompt, re.M)
    if "open-bugs" in skill_names and "open bugs" in low:
        return (
            "<jirabot><message>I have a skill called open-bugs for this. Want me to use it?</message>"
            "<use_skill>open-bugs</use_skill><param name=\"project\">ABC</param></jirabot>"
        )
    if "triage" in low and "abc" not in low and not any("abc" in u.lower() for u in users):
        return "<jirabot><message>Which project key should I look at?</message></jirabot>"
    if "abc" in low or "bug" in low:
        days = re.search(r"(\d+)\s*days?", low)
        window = f" AND created >= -{days.group(1)}d" if days else ""
        return (
            "<jirabot><message>Here is a query for open bugs in ABC.</message>"
            f"<jql>project = ABC AND issuetype = Bug AND statusCategory != Done{window} ORDER BY priority DESC</jql>"
            "<fields>key,summary,status,priority,assignee</fields></jirabot>"
        )
    return "<jirabot><message>Tell me what you want to look at in Jira.</message></jirabot>"


if __name__ == "__main__":
    sys.exit(main())
