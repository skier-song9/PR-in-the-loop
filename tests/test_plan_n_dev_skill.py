from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins/pr-in-the-loop/skills/plan-n-dev"
SKILL_MD = SKILL_DIR / "SKILL.md"
AGENT_YAML = SKILL_DIR / "agents/openai.yaml"
PLUGIN_JSON = ROOT / "plugins/pr-in-the-loop/.codex-plugin/plugin.json"


class PlanNDevSkillTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL_MD.read_text(encoding="utf-8")
        cls.agent_yaml = AGENT_YAML.read_text(encoding="utf-8")
        cls.plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))

    def test_skill_has_required_identity_and_auto_trigger(self):
        self.assertIn("name: plan-n-dev", self.skill)
        self.assertIn("planning-pr", self.skill)
        self.assertIn("docs/pr-plans", self.skill)
        self.assertIn("Use automatically when a PR plan exists, no spec exists", self.skill)
        self.assertIn("the user does not know what to do next", self.skill)

    def test_frontmatter_description_is_short_routing_metadata(self):
        description = next(
            line.removeprefix("description: ").strip()
            for line in self.skill.splitlines()
            if line.startswith("description: ")
        )
        self.assertLessEqual(len(description), 90)
        self.assertIn("planning-pr", description)
        self.assertIn("implementation", description)
        for documentation_detail in [
            ".memory/specs",
            "Trigger automatically",
            "Do not use",
            "save",
        ]:
            self.assertNotIn(documentation_detail, description)

    def test_skill_writes_uncommitted_english_specs_under_memory(self):
        self.assertIn(".memory/specs", self.skill)
        self.assertIn("Always write the spec document in English", self.skill)
        self.assertIn("Spec documents are not commit targets", self.skill)
        self.assertIn("Do not ask for approval before implementation", self.skill)

    def test_skill_adapts_planning_and_execution_without_direct_banned_references(self):
        for banned in [
            "superpowers:writing-plans",
            "superpowers:subagent-driven-development",
            "korean-writing-tips",
        ]:
            self.assertNotIn(banned, self.skill)

        for phrase in [
            "fresh implementation worker",
            "spec compliance review",
            "code quality review",
            "test-first",
            "Do not pause between tasks",
        ]:
            self.assertIn(phrase, self.skill)

    def test_skill_defines_spec_headers_and_task_steps(self):
        for header in [
            "# <Feature Name> Implementation Spec",
            "**Goal:**",
            "**Architecture:**",
            "**Tech Stack:**",
            "### Task N: <Component Name>",
            "**Files:**",
            "Write the failing test",
            "Run test to verify it fails",
            "Write minimal implementation",
            "Run test to verify it passes",
            "Commit",
        ]:
            self.assertIn(header, self.skill)

    def test_skill_enforces_tdd_and_compact_scope_discipline(self):
        for phrase in [
            "No implementation code before a failing test has been written and observed",
            "RED must fail for the expected missing behavior",
            "GREEN must be the smallest implementation",
            "Refactor only after GREEN",
            "Implement exactly what the task specifies",
            "Do not create committed helper, benchmark, or validation files",
            "Prefer existing test and build commands over new committed harnesses",
            "Each committed file should have one clear responsibility",
            "DONE_WITH_CONCERNS",
        ]:
            self.assertIn(phrase, self.skill)

    def test_skill_uses_explicit_gpt55_for_strong_subagents(self):
        self.assertNotIn("latest model", self.skill)
        self.assertIn('model: "gpt-5.5"', self.skill)
        self.assertIn('reasoning_effort: "xhigh"', self.skill)
        self.assertNotIn("service_tier", self.skill)
        self.assertIn("Use only dispatch fields supported by the current subagent API", self.skill)

    def test_agent_metadata_exists(self):
        self.assertIn('display_name: "Plan N Dev"', self.agent_yaml)
        self.assertIn("$plan-n-dev", self.agent_yaml)

    def test_plugin_metadata_mentions_plan_n_dev(self):
        interface = self.plugin["interface"]
        self.assertIn("plan-n-dev", interface["defaultPrompt"])
        self.assertIn("implementation specs", interface["longDescription"])


if __name__ == "__main__":
    unittest.main()
