# HTML Report Template

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>Code Review</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; line-height: 1.55; }
    h1, h2 { margin-top: 1.4em; }
    .critical { border-left: 4px solid #b42318; padding-left: 12px; }
    .important { border-left: 4px solid #b54708; padding-left: 12px; }
    .minor { border-left: 4px solid #175cd3; padding-left: 12px; }
    code { background: #f2f4f7; padding: 1px 4px; }
  </style>
</head>
<body>
  <h1>Code Review</h1>
  <section>
    <h2>Scope</h2>
    <p>Base, head, plan, spec, changed files, and tests reviewed.</p>
  </section>
  <section>
    <h2>Summary</h2>
    <p>Critical, Important, Minor counts and merge readiness.</p>
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
</body>
</html>
```
