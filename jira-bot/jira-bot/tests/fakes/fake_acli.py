"""Stand-in for the Atlassian CLI (acli) used by the tests. Not part of the real app.

Environment switches:
  FAKE_ACLI_LOG=path   append one line per invocation (token is never written)
  FAKE_ACLI_FAIL=1     make search fail
  FAKE_ACLI_EMPTY=1    return zero results
"""
import json
import os
import sys

ISSUES = [
    ("ABC-101", "Checkout crashes on empty cart", "In Progress", "High", "Sam Rivera", "Bug"),
    ("ABC-102", "Typo on pricing page", "To Do", "Low", None, "Bug"),
    ("ABC-103", "Login loop on Safari", "To Do", "Highest", None, "Bug"),
]


def issues_for(limit):
    """The three sample issues, then generated ones when a large result set is requested."""
    out = list(ISSUES[:limit])
    n = len(out)
    names = ["Sam Rivera", None, "Priya Shah", "Lee Chen"]
    prios = ["Highest", "High", "Medium", "Low"]
    states = ["To Do", "In Progress", "In Review", "Blocked"]
    while len(out) < limit:
        n += 1
        out.append((f"ABC-{100 + n}", f"Generated issue number {n}", states[n % 4], prios[n % 4], names[n % 4], "Bug" if n % 3 else "Task"))
    return out


def main() -> int:
    args = sys.argv[1:]
    log = os.environ.get("FAKE_ACLI_LOG")
    if log:
        safe = [a for a in args]
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(" ".join(safe) + "\n")

    if args[:3] == ["jira", "auth", "status"]:
        print("Authenticated to demo.atlassian.net as me@example.com")
        return 0

    if args[:3] == ["jira", "auth", "login"]:
        token = sys.stdin.read().strip()
        if not token:
            sys.stderr.write("no token on stdin\n")
            return 1
        print("Login successful")
        return 0

    if args[:3] == ["jira", "workitem", "search"]:
        if os.environ.get("FAKE_ACLI_FAIL") == "1":
            sys.stderr.write("Error: unbounded JQL queries are not allowed\n")
            return 1
        if "--jql" not in args:
            sys.stderr.write("missing --jql\n")
            return 1
        if os.environ.get("FAKE_ACLI_NOPAGINATE") == "1" and "--paginate" in args:
            sys.stderr.write("Error: unknown flag: --paginate\n")
            return 1
        total = int(os.environ.get("FAKE_ACLI_TOTAL", "3"))  # how many issues "exist" in the fake Jira
        limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 50
        limit = total if "--paginate" in args else min(limit, total)
        wanted = args[args.index("--fields") + 1].split(",") if "--fields" in args else None
        if os.environ.get("FAKE_ACLI_NOJSON") == "1" and "--json" in args:
            sys.stderr.write("Error: unknown flag: --json\n")
            return 1
        if os.environ.get("FAKE_ACLI_EMPTY") == "1":
            print("[]")
            return 0
        if "--csv" in args:
            print("key,summary,status,priority")
            for key, summary, status, priority, assignee, itype in issues_for(limit):
                print(f'{key},"{summary}",{status},{priority}')
            return 0
        out = []
        for key, summary, status, priority, assignee, itype in issues_for(limit):
            fields = {
                "summary": summary,
                "status": {"name": status},
                "priority": {"name": priority},
                "assignee": {"displayName": assignee} if assignee else None,
                "issuetype": {"name": itype},
            }
            if wanted:
                fields = {k: v for k, v in fields.items() if k in wanted}
            out.append({"id": key.split("-")[1], "key": key, "fields": fields})
        print(json.dumps(out, indent=2))
        return 0

    sys.stderr.write(f"unknown command: {args}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
