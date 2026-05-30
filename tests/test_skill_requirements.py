"""DocString Spec Excerpt: Lock issue-language, docstring worker model/effort, parallel spawn, and install config requirements without changing runtime workflow behavior."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "pr-in-the-loop"
SKILLS = PLUGIN_DIR / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def read_reference(skill: str, name: str) -> str:
    return (SKILLS / skill / "references" / name).read_text(encoding="utf-8")


def read_root_file(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_ai_agent_handoff(text: str) -> str:
    match = re.search(
        r"## Give This To Your AI Agent\n\n```text\n(?P<handoff>.*?)\n```",
        text,
        flags=re.DOTALL,
    )
    if match is None:
        raise AssertionError("AI agent handoff block not found")
    return match.group("handoff")


class SkillRequirementTests(unittest.TestCase):
    def test_marketplace_uses_pr_in_the_loop_plugin_entry(self) -> None:
        marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")

        self.assertEqual("pr-in-the-loop", marketplace["name"])
        self.assertEqual(1, len(marketplace["plugins"]))
        self.assertEqual("pr-in-the-loop", marketplace["plugins"][0]["name"])
        self.assertEqual("./plugins/pr-in-the-loop", marketplace["plugins"][0]["source"]["path"])

    def test_plugin_manifest_uses_pr_in_the_loop_identity(self) -> None:
        manifest = read_json(PLUGIN_DIR / ".codex-plugin" / "plugin.json")

        self.assertEqual("pr-in-the-loop", manifest["name"])
        self.assertEqual("PR In The Loop", manifest["interface"]["displayName"])
        self.assertEqual("$pr-in-the-loop:github-dev-workflow", manifest["interface"]["defaultPrompt"])

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
        self.assertIn("Do not dispatch a worker until each target file either contains", text)
        self.assertIn("DocString/comments used by path", prompt)
        self.assertIn("Subagent verification", text)

    def test_docstring_parallel_requires_context_rich_delegation_comments(self) -> None:
        text = read_skill("docstring-parallel-implementation")
        prompt = read_reference("docstring-parallel-implementation", "worker-prompt-template.md")

        self.assertIn(
            "Add a short file-level comment to each target file that explains the spec context and the responsibility delegated to that file.",
            text,
        )
        self.assertIn("context-rich delegated file-level comment", text)
        self.assertIn("Required sections", text)
        self.assertIn("`Context`", text)
        self.assertIn("`References`", text)
        self.assertIn("`Work Process`", text)
        self.assertIn("Optional sections", text)
        self.assertIn("`Test Method`", text)
        self.assertIn("`Residual Risks`", text)
        self.assertIn("The file owner completes only the work described in that delegated comment", text)
        self.assertIn("when the file format supports comments or docstrings", text)
        self.assertIn("commentless or generated artifacts", text)
        self.assertIn("ownership ledger or nearest owning source/test file", text)
        self.assertIn("either contains the delegated file-level comment", text)
        self.assertIn("marked commentless", text)
        self.assertIn("Do not include secrets, credentials, tokens, personal data, absolute local paths", text)
        self.assertIn("reference repo-relative paths or public URLs only", text)
        self.assertIn("DocString/comments used by path", text)

        self.assertIn("Before implementing code, read the delegated file-level comment", prompt)
        self.assertIn("refine that comment before editing code", prompt)
        self.assertIn("Delegated file-level comments used", prompt)
        self.assertIn("PATH -> comment", prompt)
        self.assertIn("PATH -> COMMENTLESS", prompt)
        self.assertIn("every assigned target file", prompt)
        self.assertIn("For paths marked `COMMENTLESS`", prompt)
        self.assertIn("do not add or refine an in-file comment", prompt)
        self.assertIn("Do not add responsibilities, inputs/outputs, invariants, tests, or references", prompt)
        self.assertIn("not present in the assigned spec excerpt", prompt)
        self.assertIn("stop and report `NEEDS_CONTEXT` or `BLOCKED`", prompt)
        self.assertIn("Do not include secrets, credentials, tokens, personal data, absolute local paths", prompt)
        self.assertIn("reference repo-relative paths or public URLs only", prompt)
        self.assertIn("Context", prompt)
        self.assertIn("References", prompt)
        self.assertIn("Work Process", prompt)
        self.assertIn("Test Method", prompt)
        self.assertIn("Residual Risks", prompt)
        self.assertIn("DocString/comments used by path", prompt)

    def test_docstring_parallel_requires_model_effort_selection_policy(self) -> None:
        text = read_skill("docstring-parallel-implementation")
        prompt = read_reference("docstring-parallel-implementation", "worker-prompt-template.md")

        self.assertIn("Subagent Model And Effort Selection", text)
        self.assertIn("Set `model` and `reasoning_effort` when spawning each worker", text)
        self.assertIn("trivial or mechanical", text)
        self.assertIn("`gpt-5.4-mini` + `low`", text)
        self.assertIn("simple bounded docs, tests, or code edits", text)
        self.assertIn("`gpt-5.3-codex-spark` or `gpt-5.4-mini` + `medium`", text)
        self.assertIn("routine implementation with local tests", text)
        self.assertIn("`gpt-5.3-codex` or `gpt-5.4` + `medium`", text)
        self.assertIn("complex integration, shared contracts, or reviewer work", text)
        self.assertIn("`gpt-5.4` + `high`", text)
        self.assertIn("high-uncertainty architecture, security, or cross-system work", text)
        self.assertIn("`gpt-5.5` + `high` or `xhigh`", text)
        self.assertIn("Subagents cannot reliably self-attest their actual runtime model or reasoning effort", text)
        self.assertIn("Selected model:", prompt)
        self.assertIn("Selected reasoning effort:", prompt)
        self.assertIn("Selection reason:", prompt)

    def test_docstring_parallel_requires_parallel_spawn_policy(self) -> None:
        text = read_skill("docstring-parallel-implementation")
        prompt = read_reference("docstring-parallel-implementation", "worker-prompt-template.md")

        self.assertIn("Parallel Subagent Spawn Policy", text)
        self.assertIn("Use parallel subagents for independent work", text)
        self.assertIn("Spawn one subagent per task", text)
        self.assertIn("parallel policy in this skill supersedes the sub-skill's sequential default", text)
        self.assertIn("Do not let multiple write-capable agents edit the same files", text)
        self.assertIn("Use read-only explorer agents for investigation", text)
        self.assertIn("Read-only explorer dispatch is parent-controlled", text)
        self.assertIn("Wait for all subagents, then consolidate the results", text)
        self.assertIn("Return a structured summary with findings, changed files, risks, and next actions", text)
        self.assertIn("Writable tests and fixtures must be explicitly included in the safe file group", text)
        self.assertIn("ownership ledger", text)
        self.assertIn("compare the actual changed paths", text)
        self.assertIn("Do not rely only on the worker's self-report", text)
        self.assertIn("full assigned file group as `ASSIGNED_PATHS`", text)
        self.assertIn("Do not spawn additional subagents", prompt)
        self.assertIn("If this assignment is investigation-only, do not edit files", prompt)
        self.assertIn("Investigation-only assignments do not use test-driven development", prompt)
        self.assertIn("Edit only files listed in the assigned file group", prompt)
        self.assertIn("tests or fixtures must also be listed in `ASSIGNED_PATHS`", prompt)
        self.assertRegex(prompt, r"(?m)^- Assigned file group$")
        self.assertRegex(prompt, r"(?m)^- Findings$")
        self.assertRegex(prompt, r"(?m)^- Changed files$")
        self.assertRegex(prompt, r"(?m)^- Changed files outside ownership: yes/no$")
        self.assertRegex(prompt, r"(?m)^- Risks$")
        self.assertRegex(prompt, r"(?m)^- Next actions$")

    def test_install_documents_agents_parallel_config(self) -> None:
        text = read_root_file("INSTALL.md")
        handoff = extract_ai_agent_handoff(text)

        self.assertIn("[agents]", text)
        self.assertIn("max_threads = 16", text)
        self.assertIn("max_depth = 1", text)
        self.assertIn("~/.codex/config.toml", text)
        self.assertIn("Ask for explicit consent before changing global Codex settings", text)
        self.assertIn("Do not edit `~/.codex/config.toml` unless the user agrees", text)
        self.assertIn("If `~/.codex/config.toml` already has an `[agents]` section, add or update", text)
        self.assertIn("only if the block is missing", text)
        self.assertIn("[agents]", handoff)
        self.assertIn("max_threads = 16", handoff)
        self.assertIn("max_depth = 1", handoff)
        self.assertIn("Ask whether I agree before changing `~/.codex/config.toml`", handoff)
        self.assertIn("preserve existing keys and comments", handoff)
        self.assertIn("create the full `[agents]` block only if the block is missing", handoff)
        self.assertIn("do not append a duplicate `[agents]` table", handoff)
        self.assertIn("record previous values", handoff)

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

    def test_pr_message_writer_triggers_for_pull_request_preparation_intent(self) -> None:
        text = read_skill("pr-message-writer")
        dev_workflow = read_skill("github-dev-workflow")

        self.assertIn("completed changes are ready to be represented as a pull request", text)
        self.assertIn("regardless of the user's exact phrasing", text)
        self.assertIn("before any pull request creation or publication flow", text)
        self.assertIn("PR Message Writer is the mandatory evidence-to-PR-body step", text)
        self.assertIn("use `pr-in-the-loop:pr-message-writer` before creating or publishing the pull request", dev_workflow)


if __name__ == "__main__":
    unittest.main()
