# Weekly triage playbook (example skill document)

This is an example of a free-form document you can import through
**Skills > Import document...** (or **Teach me... > Import skill document...** in Chat).
It is not a special format: write your playbook the way you would explain it to a new teammate,
and include the JQL you already use. Copilot turns it into skills for you to review.

Replace ABC with your own project key before you rely on any of this.

## 1. Monday bug sweep

Every Monday I look at all bugs that are still open, highest priority first, and I check
who owns them. Anything High or Highest without an owner gets assigned in standup.

```
project = ABC AND issuetype = Bug AND statusCategory != Done ORDER BY priority DESC, created ASC
```

When summarising, group by priority and call out unassigned bugs.

## 2. Stale work

Once a month I look for open items nobody has touched for 30 days. I either close them,
refresh them, or ping the owner.

JQL: project = ABC AND statusCategory != Done AND updated <= -30d ORDER BY updated ASC

## 3. Release readiness

Two weeks before a release I check what is still open for the fix version:

`project = ABC AND fixVersion = "2.4" AND statusCategory != Done ORDER BY priority DESC`

Anything blocked or still To Do at this point needs a decision: cut it or escalate it.
