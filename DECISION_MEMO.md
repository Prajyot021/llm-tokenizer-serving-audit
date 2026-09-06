# Part C — Decision Memo

## Recommendation
**Start with prompt engineering.** It is the fastest, cheapest, and easiest to roll back. Escalate only if measured results are insufficient.

## Assumptions
- 6 target languages.
- Reviewer: 10 h/week for 2 weeks = 20 h.
- 2 min per pairwise review -> about 600 comparisons.
- Success threshold: **≥70% casualness win rate**, with no obvious correctness/meaning regression.
- SFT planning assumption: 500 synthetic pairs/language = 3,000 pairs.

## Options

| Path | Pros | Cons |
|---|---|---|
| **SFT** | Directly changes model behavior; no extra inference model | Training time, synthetic-data risk, reviewer bottleneck, A100 is consumed |
| **≤1B rewriter** | Main model unchanged; focused style control | Extra latency, compute, memory, deployment complexity |
| **Prompting** | Almost no training/serving cost; fastest iteration; easy rollback | May be too weak or inconsistent |

## Day-1 Experiment
Run **60 pairwise comparisons** against the current baseline:
- 30 Hindi
- 30 Kannada

At 2 min/comparison, this uses about **2 reviewer-hours**.

## Success Metric
**Casualness win rate:** candidate wins / total comparisons.

**Success:** ≥70%, with no obvious semantic/correctness regression.

## Kill Criterion
If prompt engineering is below **70%** in the Day-1 pilot, abandon it and test the rewriter.

If the rewriter also fails the threshold during week 1, evaluate SFT.

## Cost / Capacity
- **Prompting:** no new training run and no extra model call.
- **Rewriter:** one additional model inference per response.
- **SFT:** 3,000-pair planning dataset; exact GPU-hours cannot be stated because the assignment does not specify the base model, sequence length, batch size, or training steps.

## Final Decision
Use **prompt engineering first**. It minimizes time, compute, serving complexity, and review cost. Only escalate when measured evidence shows the simpler option is not good enough.
