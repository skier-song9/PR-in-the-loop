"""DocString Spec Excerpt: Lock issue-language detection and Issue Template requirements for github-issue-pr-planning without changing runtime workflow behavior."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "github-pr-workflow" / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def read_reference(skill: str, name: str) -> str:
    return (SKILLS / skill / "references" / name).read_text(encoding="utf-8")


class SkillRequirementTests(unittest.TestCase):
    def test_issue_pr_planning_requires_session_language_and_ambiguity_gate(self) -> None:
        text = read_skill("github-issue-pr-planning")

        self.assertIn("detected user language", text)
        self.assertIn("Ambiguity Gate", text)
        self.assertIn("Do not create the Issue or PR plan while blocking ambiguity remains", text)

    def test_issue_pr_planning_requires_issue_language_detection(self) -> None:
        text = read_skill("github-issue-pr-planning")

        self.assertIn("User Language Detection", text)
        self.assertIn("Before drafting or creating a GitHub Issue", text)
        self.assertIn("current user request", text)
        self.assertIn("surrounding conversation", text)
        self.assertIn("If the conversation is mixed", text)
        self.assertIn("If the user explicitly names a target language, use that language", text)
        self.assertIn("Apply the detected language to the Issue title, Issue body, and PR plan", text)
        self.assertIn("Preserve repository identifiers, code symbols, commands, file paths, links, and quoted output exactly", text)
        self.assertIn("ask one concise question in the detected user language", text)
        self.assertIn("recommend one in the detected user language", text)
        self.assertIn("The Issue title and Issue body must use the detected user language and the Issue Template", text)
        self.assertIn("using the detected user language", text)

    def test_issue_pr_planning_requires_issue_template(self) -> None:
        text = read_skill("github-issue-pr-planning")

        self.assertIn("Issue Template", text)
        self.assertIn("## Description", text)
        self.assertIn("one-line feature or problem summary", text)
        self.assertIn("detailed explanation", text)
        self.assertIn("## Tasks", text)
        self.assertIn("- [ ]", text)
        self.assertIn("## References", text)
        self.assertIn("related Issue or PR", text)
        self.assertIn("Keep the heading labels exactly as shown unless the user supplies a different template", text)
        self.assertIn("Fill `Tasks` with concrete checkbox items from the clarified scope", text)
        self.assertIn("Fill `References` with relevant links, related Issues or PRs, source files, or `None`", text)

    def test_pr_plan_template_has_clarification_status_and_language_instruction(self) -> None:
        text = read_reference("github-issue-pr-planning", "pr-plan-template.md")

        self.assertIn("Write this PR plan in the agent conversation session's primary language", text)
        self.assertIn("## Clarification Notes", text)
        self.assertIn("Status: ambiguity-resolved", text)

    def test_pr_plan_to_spec_requires_english_output(self) -> None:
        text = read_skill("pr-plan-to-spec")
        template = read_reference("pr-plan-to-spec", "spec-template.md")

        self.assertIn("Always write the generated spec in English", text)
        self.assertIn("This spec must be written in English", template)

    def test_docstring_parallel_requires_spec_excerpts_and_subagent_evidence(self) -> None:
        text = read_skill("docstring-parallel-implementation")
        prompt = read_reference("docstring-parallel-implementation", "worker-prompt-template.md")

        self.assertIn("DocString Spec Excerpt", text)
        self.assertIn("Do not dispatch a worker until its target files contain", text)
        self.assertIn("DocString used", prompt)
        self.assertIn("Subagent verification", text)

    def test_multi_review_requires_all_reviewers_and_kami_layout(self) -> None:
        text = read_skill("multi-review-html")
        template = read_reference("multi-review-html", "html-report-template.md")

        self.assertIn("Dispatch every reviewer prompt", text)
        self.assertIn("Kami-inspired Layout Guide", text)
        self.assertIn("#f5f4ed", text)
        self.assertIn("#1B365D", text)
        self.assertIn("class=\"review-shell\"", template)

    def test_pr_message_writer_follows_user_language(self) -> None:
        text = read_skill("pr-message-writer")

        self.assertIn("user's primary language", text)
        self.assertNotIn("Korean template by default", text)


if __name__ == "__main__":
    unittest.main()
