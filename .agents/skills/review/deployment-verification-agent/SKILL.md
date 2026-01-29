---
name: deployment-verification-agent
description: Create go/no-go checklist for risky deploys.
---

# Deployment Verification Agent

## Inputs
- Change summary
- Risk areas
- Monitoring signals

## Outputs
- Go/No-Go checklist
- Rollback triggers
- Owner sign-offs

## Steps
1. Identify critical pre/post checks
2. Set thresholds + signals
3. Define rollback triggers

## Verification
- Checklist covers pre, post, rollback
