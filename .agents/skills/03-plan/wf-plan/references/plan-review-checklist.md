# Plan review checklist

## Simplicity
- What can be cut without losing the goal?
- What is the smallest shippable slice?
- Are there unnecessary abstractions?

## Risk
- Top 3 failure modes?
- How is each prevented?
- How is each detected?
- How is each recovered (rollback/playbook)?

## Ops / release
- Deployment steps?
- Rollout strategy? (flags, canary, staged)
- Rollback steps? (including data)
- Monitoring plan on launch day?

## Data integrity
- Any migrations/backfills? Idempotent?
- Dual-write/read needed?
- Safe rollback path?
- Concurrency risks?

## Security & privacy
- Authn/authz changes?
- Input validation?
- Secrets handling?
- Data classification (PII)? Logging redaction?

## UX / product
- Key flows correct?
- Error states and empty states?
- Edge cases called out?
- Success metrics defined?
