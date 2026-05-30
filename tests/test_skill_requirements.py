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

        self.assertIn("session's primary language", text)
        self.assertIn("Ambiguity Gate", text)
        self.assertIn("Do not create the Issue or PR plan while blocking ambiguity remains", text)

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
