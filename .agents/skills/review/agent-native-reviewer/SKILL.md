---
name: agent-native-reviewer
description: Review features for agent-native parity (action + context).
---

# Agent-Native Reviewer

## Inputs
- Feature/PR context
- UI actions + agent tools
- System prompt/context injection

## Outputs
- Parity checklist
- Gaps + fixes
- Verification steps

## Steps
1. Map UI actions -> agent tools
2. Check action + context parity
3. Flag gaps; propose primitives

## Verification
- Notes cover action parity, context parity, missing tools
