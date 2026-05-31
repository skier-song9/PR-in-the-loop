"""DocString Spec Excerpt: Lock issue-language, parallel-development worker model/effort, parallel spawn, install config, Issue #8 multi-view-code-review reviewer dispatch policy, and Issue #11 multi-view-code-review HTML language requirements without changing runtime workflow behavior.

Context: Issue #8 adds regression coverage for multi-view-code-review reviewer spawn and model/effort policy. Issue #11 adds regression coverage for multi-view-code-review HTML language detection and template placeholders.
References: Issue #8; Issue #11; https://github.com/skier-song9/PR-in-the-loop/issues/8; https://github.com/skier-song9/PR-in-the-loop/issues/11.
Work Process: Assert exact strings in the skill and template so reviewer dispatch and report language policy cannot regress silently.
Test Method: python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_multi_view_code_review_requires_parallel_spawn_and_model_effort_policy
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "pr-in-the-loop"
SKILLS = PLUGIN_DIR / "skills"
EXPECTED_SKILL_NAMES = {
    "github-dev-workflow",
    "issue",
    "planning-pr",
    "parallel-development",
    "multi-view-code-review",
    "open-pr",
}

RENAMED_SKILL_NAMES = {
    "github-issue-pr-planning": "issue",
    "pr-plan-to-spec": "planning-pr",
    "docstring-parallel-implementation": "parallel-development",
    "multi-review-html": "multi-view-code-review",
    "pr-message-writer": "open-pr",
}


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

    def test_skill_directories_and_frontmatter_use_workflow_step_names(self) -> None:
        actual_names = {
            path.name
            for path in SKILLS.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }

        self.assertEqual(EXPECTED_SKILL_NAMES, actual_names)
        for old_name in RENAMED_SKILL_NAMES:
            self.assertFalse((SKILLS / old_name).exists(), old_name)
        for skill_name in EXPECTED_SKILL_NAMES:
            text = read_skill(skill_name)
            self.assertRegex(text, rf"(?m)^name: {re.escape(skill_name)}$")

    def test_github_dev_workflow_references_new_skill_names(self) -> None:
        text = read_skill("github-dev-workflow")

        self.assertIn("pr-in-the-loop:issue", text)
        self.assertIn("pr-in-the-loop:planning-pr", text)
        self.assertIn("pr-in-the-loop:parallel-development", text)
        self.assertIn("pr-in-the-loop:multi-view-code-review", text)
        self.assertIn("pr-in-the-loop:open-pr", text)
        for old_name in RENAMED_SKILL_NAMES:
            self.assertNotIn(f"pr-in-the-loop:{old_name}", text)

    def test_readmes_use_new_skill_names(self) -> None:
        for filename in ("README.md", "README.ko.md"):
            text = read_root_file(filename)
            self.assertIn("pr-in-the-loop:github-dev-workflow", text)
            self.assertIn("pr-in-the-loop:issue", text)
            self.assertIn("pr-in-the-loop:planning-pr", text)
            self.assertIn("pr-in-the-loop:parallel-development", text)
            self.assertIn("pr-in-the-loop:multi-view-code-review", text)
            self.assertIn("pr-in-the-loop:open-pr", text)
            for old_name in RENAMED_SKILL_NAMES:
                self.assertNotIn(f"pr-in-the-loop:{old_name}", text)

    def test_active_test_names_use_new_skill_names(self) -> None:
        retired_method_name_parts = {
            "pr_plan_to_spec",
            "docstring_parallel",
            "multi_review",
            "pr_message_writer",
        }
        active_test_names = {
            name for name in dir(type(self)) if name.startswith("test_")
        }

        for retired_part in retired_method_name_parts:
            self.assertFalse(
                any(retired_part in name for name in active_test_names),
                retired_part,
            )

    def test_issue_skill_is_issue_only_and_requires_planning_pr_approval(self) -> None:
        text = read_skill("issue")
        agent = (SKILLS / "issue" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        dev_workflow = read_skill("github-dev-workflow")
        readme = read_root_file("README.md")
        readme_ko = read_root_file("README.ko.md")

        self.assertIn("detected user language", text)
        self.assertIn("Ambiguity Gate", text)
        self.assertIn("Create or draft the GitHub Issue only", text)
        self.assertIn("Do not create the Issue while blocking ambiguity remains", text)
        self.assertIn("Do not write a PR plan", text)
        self.assertIn("Stop after the Issue exists or the issue draft is accepted", text)
        self.assertIn("Starting the separate `pr-in-the-loop:planning-pr` PR-plan step requires explicit human approval", text)
        self.assertIn("If the next workflow skill requires an approved PR plan artifact and none exists, stop and request that artifact", text)
        self.assertIn("Do not create a spec, code, branch, commit, or PR", text)
        self.assertIn("Redaction And Write Safety Gate", text)
        self.assertIn("Redact or summarize secrets, credentials, tokens, personal data, private URLs, and absolute local paths", text)
        self.assertIn("Issue create or update targets must match the current repository remote", text)
        self.assertIn("Before creating a new Issue, search current-repo open Issues for the same title", text)
        self.assertIn("After creation, treat the Issue URL and number as the idempotency key", text)
        self.assertNotIn("Create the problem record and PR plan", text)
        self.assertNotIn("Write a PR plan markdown file", text)
        self.assertNotIn("PR Plan Requirements", text)
        self.assertNotIn("references/pr-plan-template.md", text)
        self.assertIn("Create or draft a GitHub Issue only", agent)
        self.assertIn("Do not write a PR plan", agent)
        self.assertIn("create or draft a GitHub Issue, then stop", dev_workflow)
        self.assertIn("requires explicit human approval", dev_workflow)
        self.assertIn("requires an approved PR plan artifact and none exists", dev_workflow)
        self.assertIn("identify a problem and create or draft a GitHub Issue, then stop for explicit approval before PR planning", readme)
        self.assertIn("문제를 인식하고 GitHub Issue를 만들거나 draft로 작성한 뒤, PR 계획 전 명시적 승인에서 멈춘다", readme_ko)
        self.assertIn("create or draft a GitHub Issue, then stop", readme)
        self.assertIn("GitHub Issue를 만들거나 draft로 작성한 뒤 멈춘다", readme_ko)

    def test_issue_language_detection_applies_only_to_issue_artifacts(self) -> None:
        text = read_skill("issue")

        self.assertIn("User Language Detection", text)
        self.assertIn("Before drafting or creating a GitHub Issue", text)
        self.assertIn("current user request", text)
        self.assertIn("surrounding conversation", text)
        self.assertIn("If the conversation is mixed", text)
        self.assertIn("If the user explicitly names a target language, use that language", text)
        self.assertIn("Apply the detected language to the Issue title and Issue body", text)
        self.assertNotIn("Apply the detected language to the Issue title, Issue body, and PR plan", text)
        self.assertIn("Preserve repository identifiers, code symbols, commands, file paths, links, and quoted output exactly except for required Redaction And Write Safety Gate edits", text)
        self.assertIn("ask one concise question in the detected user language", text)
        self.assertIn("recommend one in the detected user language", text)
        self.assertIn("The Issue title and Issue body must use the detected user language and the Issue Template", text)
        self.assertIn("unless the user explicitly corrects the target Issue language", text)

    def test_issue_skill_requires_issue_template(self) -> None:
        text = read_skill("issue")

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

    def test_issue_skill_no_longer_owns_pr_plan_template(self) -> None:
        text = read_skill("issue")
        template_path = SKILLS / "issue" / "references" / "pr-plan-template.md"

        self.assertFalse(template_path.exists())
        self.assertNotIn("PR Plan Requirements", text)
        self.assertNotIn("pr-plan-template.md", text)

    def test_planning_pr_requires_english_output(self) -> None:
        text = read_skill("planning-pr")
        template = read_reference("planning-pr", "spec-template.md")

        self.assertIn("Always write the generated spec in English", text)
        self.assertIn("This spec must be written in English", template)

    def test_parallel_development_requires_spec_excerpts_and_subagent_evidence(self) -> None:
        text = read_skill("parallel-development")
        prompt = read_reference("parallel-development", "worker-prompt-template.md")

        self.assertIn("DocString Spec Excerpt", text)
        self.assertIn("Do not dispatch a worker until each target file either contains", text)
        self.assertIn("DocString/comments used by path", prompt)
        self.assertIn("Subagent verification", text)

    def test_parallel_development_requires_context_rich_delegation_comments(self) -> None:
        text = read_skill("parallel-development")
        prompt = read_reference("parallel-development", "worker-prompt-template.md")

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

    def test_parallel_development_requires_model_effort_selection_policy(self) -> None:
        text = read_skill("parallel-development")
        prompt = read_reference("parallel-development", "worker-prompt-template.md")

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

    def test_parallel_development_requires_parallel_spawn_policy(self) -> None:
        text = read_skill("parallel-development")
        prompt = read_reference("parallel-development", "worker-prompt-template.md")

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

    def test_multi_view_code_review_requires_all_reviewers_and_kami_layout(self) -> None:
        text = read_skill("multi-view-code-review")
        template = read_reference("multi-view-code-review", "html-report-template.md")

        self.assertIn("Dispatch every reviewer prompt", text)
        self.assertIn("Kami-inspired Layout Guide", text)
        self.assertIn("#f5f4ed", text)
        self.assertIn("#1B365D", text)
        self.assertIn("class=\"review-shell\"", template)

    def test_multi_view_code_review_requires_parallel_spawn_and_model_effort_policy(self) -> None:
        text = read_skill("multi-view-code-review")

        self.assertIn("Parallel Reviewer Spawn Policy", text)
        self.assertIn("Classify each reviewer task by difficulty and risk before dispatch", text)
        self.assertIn("Use parallel subagents for independent reviewer work", text)
        self.assertIn("Spawn one fresh reviewer subagent per reviewer task", text)
        self.assertIn("Reviewer subagents must be spawned with read-only permissions and tools", text)
        self.assertIn("Do not let multiple write-capable agents edit the same files", text)
        self.assertIn("Use read-only explorer agents for investigation-only support", text)
        self.assertIn("Read-only explorer dispatch is parent-controlled", text)
        self.assertIn("Assign each reviewer task a stable reviewer key before dispatch", text)
        self.assertIn("Accept at most one completed result for each reviewer task key", text)
        self.assertIn("A retry replaces the prior pending attempt for the same reviewer task key", text)
        self.assertIn("Ignore late duplicate results during consolidation", text)
        self.assertIn("Wait for all reviewer subagents, then consolidate the results", text)
        self.assertIn("Return a structured summary with findings, changed files, risks, and next actions", text)
        self.assertIn("Reviewers must not edit files", text)
        self.assertIn("Reviewer Model And Effort Selection", text)
        self.assertIn("Set `model` and `reasoning_effort` when spawning each reviewer", text)
        self.assertIn("Spawned reviewers inherit the parent model and effort only when no explicit override is appropriate or when the platform lacks override support", text)
        self.assertIn("docs and PR context checks", text)
        self.assertIn("`gpt-5.4-mini` or `gpt-5.3-codex-spark` + `medium`", text)
        self.assertIn("spec compliance and general code quality review", text)
        self.assertIn("`gpt-5.4` + `medium` or `high`", text)
        self.assertIn("security, idempotency, data contract, or ADK/agent architecture review", text)
        self.assertIn("`gpt-5.4` + `high`", text)
        self.assertIn("high-uncertainty, cross-system, or security-critical review", text)
        self.assertIn("`gpt-5.5` + `high` or `xhigh`", text)
        self.assertIn("Choose the smallest capable model/effort pair for each reviewer task", text)
        self.assertIn("Record the selected model, selected reasoning effort, and selection reason in the reviewer spawn metadata", text)
        self.assertIn("If a reviewer task is misclassified before dispatch, raise the model/effort before spawning instead of accepting a weak review result", text)
        self.assertIn("Subagents cannot reliably self-attest their actual runtime model or reasoning effort", text)
        self.assertIn("Verify model/effort selection from the spawn request, accepted tool arguments, and retained reviewer spawn metadata", text)

    def test_multi_view_code_review_requires_language_detection_and_template_language_placeholders(self) -> None:
        text = read_skill("multi-view-code-review")
        template = read_reference("multi-view-code-review", "html-report-template.md")

        self.assertIn("Language Rule", text)
        self.assertIn("User Language Detection", text)
        self.assertIn("Before writing the HTML report", text)
        self.assertIn("Inspect the current user request first", text)
        self.assertIn("Inspect surrounding conversation only as supporting evidence", text)
        self.assertIn("If the current user request is mostly one natural language, use that language", text)
        self.assertIn("If the conversation is mixed, use the language the user used when asking for review or report generation", text)
        self.assertIn("If the user explicitly names a target language, use that language", text)
        self.assertIn("Explicit target-language requests override other detection signals.", text)
        self.assertIn("For DETECTED_LANGUAGE_BCP47, emit a valid BCP 47 language tag; prefer regional tags when the user names a regional variant, and use en when language detection remains ambiguous.", text)
        self.assertIn("current user request", text)
        self.assertIn("surrounding conversation", text)
        self.assertIn("Keep the detected user language fixed for the whole HTML report", text)
        self.assertIn("Apply the detected user language to report title, summary, reviewer evidence, findings, next actions, status text, metric labels, table headings, metadata, and narrative copy", text)
        self.assertIn("Preserve code identifiers, file paths, commands, quoted errors, and reviewer verdict keywords exactly", text)
        self.assertIn("Reviewer verdict keywords and severity contract names remain visible as contract values", text)
        self.assertIn("adjacent labels, explanations, and prose use the detected user language", text)
        self.assertIn("Preserve reviewer verdict keywords exactly when reviewers provide contract keywords such as `APPROVED` or `NOT_APPLICABLE`", text)
        self.assertIn("Exact verdict keywords may appear as bare keywords or as leading verdict prefixes such as `APPROVED:` or `NOT_APPLICABLE:`; preserve the keyword, and use detected-language prose for the adjacent reason/status.", text)
        self.assertIn("Do not invent reviewer verdict keywords for reviewers that report findings; use detected-language status prose and the finding evidence instead", text)
        self.assertIn("When a reviewer uses a clear no-issue or not-applicable phrase without an exact verdict keyword, classify it for the summary count using detected-language status prose, but do not present an invented verdict keyword as quoted reviewer output.", text)
        self.assertIn("Keep severity contract names visible for findings, with localized adjacent labels/prose", text)
        self.assertIn("Before substituting dynamic values into HTML, HTML-escape reviewer evidence, findings, test output, commands, file paths, quoted errors, and narrative text.", text)
        self.assertIn("Preservation rules apply after required HTML escaping.", text)
        self.assertIn("This detection policy intentionally mirrors the GitHub issue planning language rules locally because skills load independently; keep semantic changes synchronized across language-aware workflow skills.", text)
        self.assertIn("include counts for severity buckets (Critical, Important, Minor) and reviewer verdict buckets (Approved, Not Applicable)", text)
        self.assertIn("Use `references/html-report-template.md` for structure, then replace all placeholder language markers and sample copy with detected-language report text", text)

        self.assertIn("DETECTED_LANGUAGE_BCP47", template)
        self.assertIn("DETECTED_LANGUAGE_REPORT_TITLE", template)
        self.assertIn("DETECTED_LANGUAGE_METADATA_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_HEADER_NARRATIVE_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_SUMMARY_HEADING", template)
        self.assertIn("DETECTED_LANGUAGE_CRITICAL_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_IMPORTANT_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_MINOR_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_APPROVED_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_NOT_APPLICABLE_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_SUMMARY_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_REVIEWER_COLUMN", template)
        self.assertIn("DETECTED_LANGUAGE_STATUS_COLUMN", template)
        self.assertIn("DETECTED_LANGUAGE_EVIDENCE_COLUMN", template)
        self.assertIn("DETECTED_LANGUAGE_STATUS_TEXT", template)
        self.assertIn("OPTIONAL_REVIEWER_VERDICT_BADGE_HTML", template)
        self.assertIn("DETECTED_LANGUAGE_REVIEWER_NAME", template)
        self.assertIn("DETECTED_LANGUAGE_REVIEWER_EVIDENCE_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_CHANGED_FILES_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_CHANGED_FILES_STATUS_TEXT", template)
        self.assertIn("CHANGED_FILES_ROWS_HTML", template)
        self.assertIn("DETECTED_LANGUAGE_TEST_COMMANDS_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_TEST_STATUS_TEXT", template)
        self.assertIn("TEST_COMMAND_ROWS_HTML", template)
        self.assertIn("DETECTED_LANGUAGE_FINDINGS_HEADING", template)
        self.assertIn("DETECTED_LANGUAGE_FINDING_TITLE", template)
        self.assertIn("REVIEWER_SEVERITY_CONTRACT_VALUE", template)
        self.assertIn("SEVERITY_CLASS_NAME", template)
        self.assertIn("DETECTED_LANGUAGE_LOCATION_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_EVIDENCE_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_FINDING_EVIDENCE_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_IMPACT_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_FINDING_IMPACT_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_EXAMPLE_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_FINDING_EXAMPLE_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_FIX_LABEL", template)
        self.assertIn("DETECTED_LANGUAGE_FINDING_FIX_TEXT", template)
        self.assertIn("DETECTED_LANGUAGE_NEXT_ACTIONS_HEADING", template)
        self.assertIn("DETECTED_LANGUAGE_NEXT_ACTIONS_TEXT", template)
        self.assertIn("Replace every visible sample label and sentence with detected-language report text before saving the report", template)
        self.assertIn("OPTIONAL_REVIEWER_VERDICT_BADGE_HTML may be omitted when no exact verdict keyword or leading verdict prefix exists; DETECTED_LANGUAGE_STATUS_TEXT must still explain the status classification.", template)
        self.assertIn("CHANGED_FILES_ROWS_HTML must contain one escaped table row per changed file.", template)
        self.assertIn("TEST_COMMAND_ROWS_HTML must contain one escaped table row per test command and result.", template)
        self.assertIn("SEVERITY_CLASS_NAME must be critical, important, or minor and must match REVIEWER_SEVERITY_CONTRACT_VALUE.", template)
        self.assertIn("HTML-escape every substituted value except OPTIONAL_REVIEWER_VERDICT_BADGE_HTML before saving the report.", template)
        self.assertNotIn("OPTIONAL_REVIEWER_VERDICT_CONTRACT_VALUE", template)
        self.assertNotIn('<html lang="ko">', template)

    def test_open_pr_follows_user_language(self) -> None:
        text = read_skill("open-pr")

        self.assertIn("user's primary language", text)
        self.assertNotIn("Korean template by default", text)

    def test_open_pr_triggers_for_pull_request_preparation_intent(self) -> None:
        text = read_skill("open-pr")
        dev_workflow = read_skill("github-dev-workflow")

        self.assertIn("completed changes are ready to be represented as a pull request", text)
        self.assertIn("regardless of the user's exact phrasing", text)
        self.assertIn("before any pull request creation or publication flow", text)
        self.assertIn("Open PR is the mandatory evidence-to-PR-body step", text)
        self.assertIn("use `pr-in-the-loop:open-pr` before creating or publishing the pull request", dev_workflow)


if __name__ == "__main__":
    unittest.main()
