# Korean Writing Tips for Workflow Skills

Source basis: distilled from `epoko77-ai/im-not-ai` Humanize Korean guidance and adapted for engineering workflow documents. Do not copy the source skill wholesale. Apply these rules to Issues, PR plans, review notes, specs, and similar Korean documents.

## Contract

- Preserve facts, numbers, dates, names, URLs, code identifiers, and quoted text.
- Do not add claims, causes, or acceptance criteria not supported by context.
- Keep the document's job: an Issue should define a problem; a PR plan should define an implementation path; a review should identify risks.
- Use direct, plain Korean. Avoid decorative prose.

## Structure

- Start with the answer or problem in one line.
- Then explain context: current state, desired state, why now.
- Prefer concrete subjects and verbs.
- Use lists when they make execution easier; avoid lists that merely decorate prose.
- Keep headings functional. Avoid excessive bold, emoji, quote marks, or marketing-style emphasis.

## Common Korean Cleanup

Prefer natural Korean forms:

- `~에 대해 논의한다` -> `~를 논의한다`
- `~를 통해 처리한다` -> `~로 처리한다`, `~해서 처리한다`
- `~에 있어서` -> `~에서`, `~을 볼 때`
- `~와 관련하여` -> `~에`, `~의`, `~를 두고`
- `~에 기반하여` -> `~를 기준으로`, `~를 보고`, `~로`
- `가지고 있다` -> `있다`, `강하다`, or a concrete verb
- `~되어진다` -> `~된다`
- `~에 의해 생성된` -> `~가 만든`
- `~할 수 있다` -> use a direct verb when the statement is certain
- `~인 것이다`, `~라는 점이다` -> direct sentence ending

Remove or replace weak stock phrases unless the context truly needs them:

- `결론적으로`, `요약하면`, `정리하자면`
- `시사하는 바가 크다`, `주목할 만하다`
- `본질적으로`, `핵심적으로`
- `혁신적인`, `압도적인`, `획기적인`, `강력한`
- repeated `또한`, `따라서`, `나아가`, `아울러`

## Rhythm and Tone

- Preserve the user's/register's level of formality.
- Engineering docs should be calm, specific, and scannable.
- Vary sentence length lightly, but do not force literary rhythm into technical writing.
- Avoid mechanical `첫째/둘째/셋째` when task order or bullets already express sequence.
- Do not turn a report into a blog post, or an implementation issue into a persuasive essay.

## Review Checklist

Before publishing Korean workflow text:

- One-line summary states the actual problem.
- Context explains why the problem matters.
- Tasks use executable verbs.
- No unsupported facts were introduced.
- Names, numbers, URLs, and code identifiers are unchanged.
- Translation-like phrases and AI stock phrases were removed.
- The tone matches the document type.
