"""Example JQL patterns shown in the blank state. Nothing here is saved until the user approves it."""
from __future__ import annotations

from typing import List

from .store import Param, Skill


def example_skills() -> List[Skill]:
    project = Param("project", "Jira project key", "")
    return [
        Skill(
            name="open-bugs",
            description="Open bugs in a project, highest priority first",
            jql="project = {project} AND issuetype = Bug AND statusCategory != Done ORDER BY priority DESC, created DESC",
            parameters=[project],
            output="Group by priority and point out anything unassigned.",
        ),
        Skill(
            name="new-bugs-last-days",
            description="Bugs created recently",
            jql="project = {project} AND issuetype = Bug AND created >= -{days}d ORDER BY created DESC",
            parameters=[project, Param("days", "Look-back window in days", "7")],
        ),
        Skill(
            name="urgent-unassigned",
            description="High priority work nobody owns yet",
            jql="project = {project} AND priority in (High, Highest) AND assignee is EMPTY AND statusCategory != Done ORDER BY created ASC",
            parameters=[project],
            output="List the oldest first; these need an owner.",
        ),
        Skill(
            name="stale-items",
            description="Open items with no activity for a while",
            jql="project = {project} AND statusCategory != Done AND updated <= -{days}d ORDER BY updated ASC",
            parameters=[project, Param("days", "Days without an update", "30")],
            output="Suggest which to close, which to refresh, and which need a ping.",
        ),
        Skill(
            name="current-sprint",
            description="Everything in the active sprint",
            jql="project = {project} AND sprint in openSprints() ORDER BY status ASC, priority DESC",
            parameters=[project],
        ),
        Skill(
            name="blocked-items",
            description="Work flagged or labelled as blocked",
            jql="project = {project} AND statusCategory != Done AND (labels = blocked OR status = Blocked) ORDER BY updated ASC",
            parameters=[project],
            notes="Adjust the label or status name to match how your team marks blocked work.",
        ),
        Skill(
            name="release-scope",
            description="Unfinished work for a fix version",
            jql='project = {project} AND fixVersion = "{version}" AND statusCategory != Done ORDER BY priority DESC',
            parameters=[project, Param("version", "Fix version name", "")],
        ),
    ]
