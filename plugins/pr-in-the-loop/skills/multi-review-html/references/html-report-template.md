# HTML Report Template

<!-- DocString Spec Excerpt
Context: Issue #11 makes this template a language-neutral scaffold for detected-language HTML review reports.
References: Issue #11; https://github.com/skier-song9/PR-in-the-loop/issues/11.
Work Process: Replace fixed language metadata and visible sample copy with detected-language placeholders while keeping CSS/class names stable.
Test Method: python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_multi_review_html_requires_language_detection_and_template_language_placeholders
-->

```html
<!doctype html>
<html lang="DETECTED_LANGUAGE_BCP47">
<head>
  <meta charset="utf-8">
  <title>DETECTED_LANGUAGE_REPORT_TITLE</title>
  <style>
    :root {
      --parchment: #f5f4ed;
      --ivory: #faf9f5;
      --brand: #1B365D;
      --near-black: #141413;
      --dark-warm: #3d3d3a;
      --olive: #504e49;
      --stone: #6b6a64;
      --border: #e8e6dc;
      --border-soft: #e5e3d8;
      --critical: #B53333;
      --important: #8A4B16;
      --minor: #1B365D;
    }
    body {
      margin: 0;
      background: var(--parchment);
      color: var(--near-black);
      font-family: Charter, Georgia, Palatino, "Times New Roman", serif;
      line-height: 1.55;
    }
    .review-shell { max-width: 1040px; margin: 0 auto; padding: 48px 32px 72px; }
    header { border-left: 4px solid var(--brand); padding-left: 18px; margin-bottom: 32px; }
    h1 { font-size: 34px; line-height: 1.15; font-weight: 500; margin: 0 0 10px; }
    h2 { font-size: 20px; line-height: 1.25; font-weight: 500; margin: 32px 0 12px; }
    h3 { font-size: 16px; line-height: 1.3; font-weight: 500; margin: 0 0 8px; }
    .meta, .tag, th { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    .meta { color: var(--stone); font-size: 13px; }
    .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin: 18px 0; }
    .metric { background: var(--ivory); border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; }
    .metric strong { display: block; color: var(--brand); font-size: 24px; font-weight: 500; }
    .metric span { color: var(--olive); font-size: 13px; }
    table { width: 100%; border-collapse: collapse; background: var(--ivory); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
    th, td { padding: 9px 11px; border-bottom: 1px solid var(--border-soft); text-align: left; vertical-align: top; }
    th { color: var(--dark-warm); font-size: 12px; font-weight: 600; }
    article { background: var(--ivory); border: 1px solid var(--border); border-left-width: 4px; border-radius: 8px; padding: 16px 18px; margin: 14px 0; }
    .critical { border-left-color: var(--critical); }
    .important { border-left-color: var(--important); }
    .minor { border-left-color: var(--minor); }
    .tag { display: inline-block; background: #EEF2F7; color: var(--brand); border-radius: 4px; padding: 2px 7px; font-size: 11px; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; }
    code { background: #faf9f5; border: 1px solid var(--border-soft); border-radius: 5px; padding: 1px 4px; font-family: "JetBrains Mono", "SF Mono", Consolas, monospace; font-size: .92em; }
  </style>
</head>
<body>
  <main class="review-shell">
    <header>
      <p class="meta">DETECTED_LANGUAGE_METADATA_TEXT</p>
      <h1>DETECTED_LANGUAGE_REPORT_TITLE</h1>
      <p>DETECTED_LANGUAGE_HEADER_NARRATIVE_TEXT</p>
    </header>
    <section>
      <h2>DETECTED_LANGUAGE_SUMMARY_HEADING</h2>
      <div class="summary-grid">
        <div class="metric"><strong>0</strong><span>DETECTED_LANGUAGE_CRITICAL_LABEL</span></div>
        <div class="metric"><strong>0</strong><span>DETECTED_LANGUAGE_IMPORTANT_LABEL</span></div>
        <div class="metric"><strong>0</strong><span>DETECTED_LANGUAGE_MINOR_LABEL</span></div>
        <div class="metric"><strong>0</strong><span>DETECTED_LANGUAGE_APPROVED_LABEL</span></div>
        <div class="metric"><strong>0</strong><span>DETECTED_LANGUAGE_NOT_APPLICABLE_LABEL</span></div>
      </div>
      <p>DETECTED_LANGUAGE_SUMMARY_TEXT</p>
    </section>
    <section>
      <h2>DETECTED_LANGUAGE_REVIEWER_EVIDENCE_HEADING</h2>
      <table>
        <thead><tr><th>DETECTED_LANGUAGE_REVIEWER_COLUMN</th><th>DETECTED_LANGUAGE_STATUS_COLUMN</th><th>DETECTED_LANGUAGE_EVIDENCE_COLUMN</th></tr></thead>
        <tbody>
          <tr><td>DETECTED_LANGUAGE_REVIEWER_NAME</td><td>OPTIONAL_REVIEWER_VERDICT_BADGE_HTML DETECTED_LANGUAGE_STATUS_TEXT</td><td>DETECTED_LANGUAGE_REVIEWER_EVIDENCE_TEXT</td></tr>
          CHANGED_FILES_ROWS_HTML
          TEST_COMMAND_ROWS_HTML
        </tbody>
      </table>
    </section>
    <section>
      <h2>DETECTED_LANGUAGE_FINDINGS_HEADING</h2>
      <article class="SEVERITY_CLASS_NAME">
        <h3>REVIEWER_SEVERITY_CONTRACT_VALUE · DETECTED_LANGUAGE_FINDING_TITLE</h3>
        <p><strong>DETECTED_LANGUAGE_LOCATION_LABEL:</strong> file:line</p>
        <p><strong>DETECTED_LANGUAGE_EVIDENCE_LABEL:</strong> DETECTED_LANGUAGE_FINDING_EVIDENCE_TEXT</p>
        <p><strong>DETECTED_LANGUAGE_IMPACT_LABEL:</strong> DETECTED_LANGUAGE_FINDING_IMPACT_TEXT</p>
        <p><strong>DETECTED_LANGUAGE_EXAMPLE_LABEL:</strong> DETECTED_LANGUAGE_FINDING_EXAMPLE_TEXT</p>
        <p><strong>DETECTED_LANGUAGE_FIX_LABEL:</strong> DETECTED_LANGUAGE_FINDING_FIX_TEXT</p>
      </article>
    </section>
    <section>
      <h2>DETECTED_LANGUAGE_NEXT_ACTIONS_HEADING</h2>
      <p>DETECTED_LANGUAGE_NEXT_ACTIONS_TEXT</p>
    </section>
  </main>
</body>
</html>
```

Replace every visible sample label and sentence with detected-language report text before saving the report.
OPTIONAL_REVIEWER_VERDICT_BADGE_HTML may be omitted when no exact verdict keyword or leading verdict prefix exists; DETECTED_LANGUAGE_STATUS_TEXT must still explain the status classification.
CHANGED_FILES_ROWS_HTML must contain one escaped table row per changed file.
TEST_COMMAND_ROWS_HTML must contain one escaped table row per test command and result.
Use DETECTED_LANGUAGE_CHANGED_FILES_LABEL and DETECTED_LANGUAGE_CHANGED_FILES_STATUS_TEXT within CHANGED_FILES_ROWS_HTML rows.
Use DETECTED_LANGUAGE_TEST_COMMANDS_LABEL and DETECTED_LANGUAGE_TEST_STATUS_TEXT within TEST_COMMAND_ROWS_HTML rows.
SEVERITY_CLASS_NAME must be critical, important, or minor and must match REVIEWER_SEVERITY_CONTRACT_VALUE.
HTML-escape every substituted value except OPTIONAL_REVIEWER_VERDICT_BADGE_HTML before saving the report.
