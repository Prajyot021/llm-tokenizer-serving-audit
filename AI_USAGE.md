# AI_USAGE.md

## AI Use Disclosure

AI was used as a **tutor, experiment-planning assistant, calculation checker, debugging aid, and writing aid** during this assignment.

The actual experiments were run in the local project environment. Experimental results recorded in the assignment notebook were taken from the terminal outputs obtained during the work rather than from AI-generated estimates.

---

## Part A — Tokenizer Audit

AI assistance was used to:

- explain tokenizer, token, corpus, fertility, denominator, Unicode, UTF-8, and grapheme-cluster concepts;
- inspect the logic of the supplied `fertility.py`;
- propose small commands for reproducing and testing the original experiment;
- help distinguish facts, calculations, experiments, inferences, assumptions, and recommendations;
- help design the multilingual evaluation corpus;
- help interpret the actual GPT-2 and XLM-R results;
- help structure the corrected fertility experiment.

### Experiments actually run

The provided commands were executed locally to measure:

- original GPT-2 fertility;
- line-level Hindi fertility;
- macro vs. micro fertility;
- GPT-2 vs. XLM-R fertility;
- UTF-8 byte counts;
- Unicode code-point counts;
- grapheme-cluster counts;
- whitespace-normalization effects;
- FLORES-200 availability and sentence-ID alignment;
- GPT-2 and XLM-R fertility on the 1,012-sentence evaluation corpus.

### Important AI-assisted reasoning outcome

The analysis initially considered several possible methodological problems. Each was tested before being treated as a finding.

For example, macro vs. micro averaging was tested on both the sample and the larger evaluation corpus. The effect was found to be relatively small.

The tokenizer comparison produced a much larger effect: GPT-2 and XLM-R gave very different Indic fertility values on the same corpus. This result was based on actual local measurements.

---

## Part B — Serving / Capacity Audit

AI assistance was used to:

- explain KV cache, model weights, context length, batch size, throughput, goodput, and preemption;
- derive the KV-cache bytes-per-token formula;
- guide inspection of the benchmark rows;
- check arithmetic;
- interpret the benchmark's throughput counter;
- calculate generated-token goodput;
- structure the B3/B4 reasoning.

### Genuine correction to AI-assisted reasoning

One initial KV-capacity calculation omitted model-weight memory and therefore overestimated theoretical sequence capacity.

The mistake was identified during the audit, the model's 4.2B FP16 weight memory was included, and the calculation was revised.

This correction is recorded in `NOTEBOOK.md`.

### Another genuine correction

The meaning of `reported_tok_s` was not assumed in the final analysis.

Initial reasoning considered it as possible generated-token throughput. The actual benchmark values showed that it corresponds to prompt + generated tokens per second for the tested rows.

The analysis was corrected to use **generated-token goodput** when evaluating generation capacity.

This correction is also recorded in `NOTEBOOK.md`.

---

## Part C — Decision Memo

AI assistance was used to:

- compare SFT, an inference-time rewriter, and prompt engineering;
- identify trade-offs under the stated hardware, time, reviewer, language, and budget constraints;
- structure assumptions;
- formulate a measurable evaluation metric;
- estimate reviewer capacity;
- define a numeric success threshold;
- formulate a kill criterion;
- design a day-1 experiment;
- structure the final recommendation.

The following were treated as **planning assumptions**, not facts supplied by the assignment:

- 2 minutes per reviewer comparison;
- 600 comparisons over 20 reviewer-hours;
- 70% casualness-win threshold;
- 500 synthetic training pairs per language for an illustrative SFT plan.

---

## AI Errors and Corrections

AI assistance was not treated as infallible. The following genuine corrections occurred:

### 1. KV-cache capacity
An initial calculation omitted model-weight memory. The calculation was corrected after checking the supplied model specification.

### 2. `reported_tok_s` interpretation
The benchmark counter was initially not fully understood. Actual benchmark arithmetic established that the counter includes prompt and generated tokens. The final analysis therefore uses generated-token goodput for generation-capacity comparisons.

These corrections were retained rather than removed so the notebook reflects the actual reasoning process.

---

## What Was Done by the Student

The student:

- executed the commands and experiments in the local environment;
- provided the actual terminal outputs;
- made the experimental and methodological decisions;
- selected the final corpus configuration;
- reviewed and interpreted the measured results with AI guidance;
- made the final recommendation.

AI did not have access to the student's local machine beyond the files and outputs provided in the conversation.

---

## Final Disclosure

AI was used throughout the assignment as an interactive instructor and technical assistant. It helped explain concepts, propose experiments, generate small utility scripts/commands, check calculations, interpret outputs, and organize the written deliverables.

The final analysis was grounded in the **provided assignment, supplied starter files, and actual experiment results**. Unsupported assumptions were labeled as assumptions, and incorrect reasoning discovered during the work was corrected and documented.
