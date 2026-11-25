# Real test results (25 Nov 2026, self-hosted Dify 1.20.0)

All runs below are real calls to the published `Nimbus Support` Chatflow through the Dify app API. Data is fictional.

## Knowledge base

- File: `faq/nimbus-coffee-faq.md` (2,758 bytes), High Quality index, `gemini-embedding-001`, automatic chunking: **10 of 10 segments indexed**.

| Hit-test query | Top chunk | Score |
|---|---|---|
| What's your return policy on unopened bags? | Returns and refunds… | 0.7493 |
| How long does US shipping take? | Shipping… | 0.7294 |

## Chat tests (final run)

| Question | Path taken | Answered by | Result |
|---|---|---|---|
| What's your return policy on unopened bags? | Question Classifier → Knowledge Retrieval → Answer from FAQ → Answer from FAQ (free backup model) → Answer (backup) | gemini-3.5-flash-lite (fallback) | answered |
| How long does US shipping take? | Question Classifier → Knowledge Retrieval → Answer from FAQ → Answer from FAQ (free backup model) → Answer (backup) | gemini-3.5-flash-lite (fallback) | answered |
| Can I pause my coffee subscription? | Question Classifier → Knowledge Retrieval → Answer from FAQ → Answer from FAQ (free backup model) → Answer (backup) | gemini-3.5-flash-lite (fallback) | answered |
| Where is order NMB-1042? | Question Classifier → Get Order Number → Order Status API [HTTP 200] → Order found? → Explain Order Status → Explain Order Status (free backup model) → Answer (backup) | gemini-3.5-flash-lite (fallback) | answered |
| What's the status of NMB-1188? | Question Classifier → Get Order Number → Order Status API [HTTP 200] → Order found? → Explain Order Status → Explain Order Status (free backup model) → Answer (backup) | gemini-3.5-flash-lite (fallback) | answered |
| Where is order NMB-0000? | Question Classifier → Get Order Number → Order Status API [HTTP 404] → Order found? → Answer (not found) | none (fixed reply) | answered |
| What's the weather in Lagos? | Question Classifier → Answer (other) | none (fixed reply) | answered |

Full answers are in `chat_tests.json`.

## What happened on the way (honest log)

- Run 1 (Hydrogen only): routing was correct for all 7 questions; the 4 order/not-found/other questions succeeded; the 3 FAQ replies failed with Gemini "high demand" errors and then a free-tier limit the API reported as **5 requests per minute** for `gemini-4-hydrogen`.
- Run 2: the API reported the free-tier daily limit as **20 requests per day** for `gemini-4-hydrogen`, and the same 20/day limit for `gemini-3.8-flash`, which was already used up for the day on this Google project (quotas are per project and shared with other work).
- Fix, no code: each Hydrogen LLM node got Dify's built-in retry plus a **fail branch** to a free backup model, `gemini-3.5-flash-lite`.
- Run 3: 6 of 7 answered; one FAQ question hit a transient "high demand" error on the backup too. A single retry of that question answered. All 7 now have real answers.
- Hydrogen itself answered 4 replies before its daily quota ran out: NMB-1042 and NMB-1188 in run 1; the returns question and NMB-1042 in run 2. In the final run every LLM reply came from the free fallback.
- No paid model, paid plan, or billing was used.
