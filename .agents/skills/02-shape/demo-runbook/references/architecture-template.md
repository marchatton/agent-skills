# Architecture Template (LLM-specific, credible)

Use this template to write the architecture section in a way that a mixed audience can follow.

## 1) Tech stack (20 to 30 seconds)
List only what matters:
- Frontend: {{tech_stack.frontend}}
- Backend: {{tech_stack.backend}}
- LLM: {{tech_stack.llm_provider_and_models}}
- Orchestration: {{tech_stack.orchestration}}
- Retrieval: {{tech_stack.vector_search_or_db}}
- Storage: {{tech_stack.storage}}
- Auth/security: {{tech_stack.auth_security}}
- Observability: {{tech_stack.observability}}
- Evals: {{tech_stack.evals_tooling}}
- Hosting: {{tech_stack.hosting}}

If unknown, insert TODO placeholders.

## 2) High-level flow (20 to 30 seconds)
Explain:
- Request in
- Retrieve context (or not) and why
- Compose prompt with guardrails
- Generate response with grounding
- Log traces and metrics
- Feed evals and regression checks

## 3) RAG and grounding (45 to 60 seconds)
Cover:
- Why RAG is used (or why not)
- What gets retrieved (docs, pack data, policies, notes)
- Chunking strategy (size, overlap) with rationale
- Retrieval strategy (top-k, filtering, metadata)
- Grounding behaviour:
  - cite sources when available
  - say “unknown” when not grounded
  - ask clarifying questions when input is ambiguous

Add a short citations policy:
- “Cite when the answer depends on retrieved context.”
- “Avoid citations when it is general product behaviour.”
- “Never fabricate citations.”

## 4) Architecture options considered (60 seconds)
Include at least two. Use this pattern:

Option 1: Prompt-only
- Pros: simplest, fastest to build
- Cons: weaker grounding, harder to be reliable at scale
- When it is good: prototypes, low-stakes answers

Option 2: RAG + light tool use (chosen or not)
- Pros: better grounding and traceability, safer outputs
- Cons: more moving parts, needs tuning and monitoring
- When it is good: decision support, high trust requirements

Option 3: Agentic workflow (optional)
- Pros: powerful, can execute multi-step tasks
- Cons: complexity, harder determinism, cost and latency
- When it is good: structured tasks with clear tool boundaries

Then justify the PoC choice:
- “We chose {{architecture.chosen_option}} because {{rationale}}.”
- “Trade-offs accepted: {{tradeoffs}}.”

## 5) Evals (45 to 60 seconds)
Describe:
- Offline eval set: scenarios, golden answers, edge cases
- Regression: run on every change to prompts, retrieval, or model
- Metrics:
  - groundedness, correctness, refusal quality
  - citation accuracy
  - latency and cost budgets
Define “good”:
- “Good means the model answers correctly when grounded, asks clarifying questions when needed, and refuses when it cannot ground.”

## 6) Observability (30 to 45 seconds)
Describe what is captured:
- traces per request
- prompt templates and versions
- retrieval stats (top-k, hit rate, latency)
- cost and latency
- failure modes and user feedback signals
- logging redaction and PII handling (even if synthetic, design for real)

## 7) Security and privacy notes (15 to 30 seconds)
State:
- separate secrets from prompts
- redact logs
- least privilege access
- clear data boundaries

## 8) Close (10 seconds)
Tie back to user feelings:
- “The architecture choices are about moving the user from {{starting_feelings}} to {{desired_feelings}} with grounding and guardrails.”

