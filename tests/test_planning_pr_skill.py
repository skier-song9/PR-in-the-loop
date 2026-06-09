from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins/pr-in-the-loop/skills/planning-pr"
SKILL_MD = SKILL_DIR / "SKILL.md"
AGENT_YAML = SKILL_DIR / "agents/openai.yaml"
PLUGIN_JSON = ROOT / "plugins/pr-in-the-loop/.codex-plugin/plugin.json"


class PlanningPrSkillTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL_MD.read_text(encoding="utf-8")
        cls.agent_yaml = AGENT_YAML.read_text(encoding="utf-8")
        cls.plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))

    def test_skill_has_required_identity_and_scope_boundaries(self):
        self.assertIn("name: planning-pr", self.skill)
        self.assertIn("PR planning", self.skill)
        self.assertIn("Do not implement code", self.skill)
        self.assertIn("Do not open pull requests", self.skill)

    def test_skill_requires_phase_plans_and_reviewer_headers(self):
        for header in [
            "## Goal",
            "## Scope for This Phase",
            "## Out of Scope",
            "## Validation",
            "## PR Split Rationale",
            "## Review Notes",
            "## Reference",
        ]:
            self.assertIn(header, self.skill)

        self.assertIn("minimum functional unit", self.skill)
        self.assertIn("implementation order", self.skill)

    def test_skill_requires_research_and_ambiguity_resolution(self):
        for phrase in [
            "codebase search",
            "official docs",
            "web search",
            "3-4 options",
            "recommend",
            "tradeoff",
        ]:
            self.assertIn(phrase, self.skill)

    def test_skill_requires_language_and_korean_writing_contract(self):
        self.assertIn("user's language", self.skill)
        self.assertIn("../../references/korean-writing-tips.md", self.skill)

    def test_skill_records_plan_commit_policy_in_memory_on_opt_out(self):
        self.assertIn("docs/pr-plans", self.skill)
        self.assertIn("commit target by default", self.skill)
        self.assertIn(".memory/planning-pr/work-context.md", self.skill)
        self.assertIn("explicitly opts out", self.skill)

    def test_agent_metadata_exists(self):
        self.assertIn('display_name: "Planning PR"', self.agent_yaml)
        self.assertIn("$planning-pr", self.agent_yaml)

    def test_plugin_metadata_mentions_issue_and_pr_planning(self):
        interface = self.plugin["interface"]
        self.assertIn("Issue", interface["shortDescription"])
        self.assertIn("PR", interface["shortDescription"])
        self.assertIn("planning-pr", interface["defaultPrompt"])


if __name__ == "__main__":
    unittest.main()
