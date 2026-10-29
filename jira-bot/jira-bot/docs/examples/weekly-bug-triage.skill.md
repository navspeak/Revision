---
name: weekly-bug-triage
description: Open bugs for a project from the last few days, highest priority first
fields: key,summary,status,priority,assignee
limit: 50
parameters:
  - project | Jira project key | ABC
  - days | Look-back window in days | 7
---

## JQL

project = {project} AND issuetype = Bug AND statusCategory != Done AND created >= -{days}d ORDER BY priority DESC, created ASC

## Output

Group by priority. Call out bugs with no assignee and anything older than a week.

## Notes

This is an example of a ready-made skill file. You can import a file like this with
Skills > Import document... and no Copilot call is needed, because it is already in the skill format.
Copy it, change the JQL, and keep the three parts: the header between the --- lines, the ## JQL section,
and the optional ## Output and ## Notes sections.
