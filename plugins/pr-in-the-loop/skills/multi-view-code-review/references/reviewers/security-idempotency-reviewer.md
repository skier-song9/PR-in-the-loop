# Security Idempotency Reviewer

Check security, privacy, idempotency, and deduplication risks.

Focus:
- PII or secret logging
- unsafe shell, file, network, or GitHub operations
- duplicate writes, non-idempotent retries, and race conditions
- authorization, tenant, and ownership boundaries
- cleanup and rollback safety

Every issue must include a concrete abuse, retry, or duplicate-operation example.
