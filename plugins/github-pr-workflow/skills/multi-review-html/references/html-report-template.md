# HTML Report Template

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>Code Review</title>
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
      <p class="meta">Code Review · DATE · BRANCH</p>
      <h1>Code Review</h1>
      <p>Base, head, plan, spec, changed files, and tests reviewed.</p>
    </header>
    <section>
      <h2>Summary</h2>
      <div class="summary-grid">
        <div class="metric"><strong>0</strong><span>Critical</span></div>
        <div class="metric"><strong>0</strong><span>Important</span></div>
        <div class="metric"><strong>0</strong><span>Minor</span></div>
        <div class="metric"><strong>0</strong><span>Not Applicable</span></div>
      </div>
      <p>Merge readiness and reviewer conclusion.</p>
    </section>
    <section>
      <h2>Reviewer Evidence</h2>
      <table>
        <thead><tr><th>Reviewer</th><th>Status</th><th>Evidence</th></tr></thead>
        <tbody>
          <tr><td>spec compliance</td><td><span class="tag">approved</span></td><td>Concrete evidence.</td></tr>
        </tbody>
      </table>
    </section>
    <section>
      <h2>Findings</h2>
      <article class="important">
        <h3>Severity: title</h3>
        <p><strong>Location:</strong> file:line</p>
        <p><strong>Evidence:</strong> concrete observation.</p>
        <p><strong>Example:</strong> concrete failure or safer shape.</p>
        <p><strong>Fix:</strong> suggested action.</p>
      </article>
    </section>
  </main>
</body>
</html>
```
