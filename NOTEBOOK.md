# NOTEBOOK.md — Assignment Audit Log

## Purpose

Chronological record of the audit. Actual measurements are labeled **ACTUAL**. Derived values are **CALCULATION**. Interpretations are **INFERENCE**. Planning values for Part C are **ASSUMPTION**. Genuine revisions are recorded rather than hidden.

---

# Part A — Tokenizer Audit

## A1. Reproduce the previous intern's experiment

**Hypothesis:** the supplied `fertility.py` should approximately reproduce the intern's reported GPT-2 fertility results.

**Command:**
```powershell
python fertility.py --corpus eng=.\corpus_sample\eng_sample.txt --corpus hin=.\corpus_sample\hin_sample.txt --tokenizer gpt2
```

**ACTUAL:**
```text
tokenizer: gpt2
lang      fertility (tok/word)    tok/char
------------------------------------------
eng                       1.28       0.226
hin                       7.60       1.579

hin is 5.92x the fertility of eng (worse tokenization)
```

**Intern report:** English 1.27, Hindi 7.45, ratio 5.89x.

**Interpretation:** original experiment is approximately reproducible. The small numerical discrepancy was not independently resolved and must not be guessed.

## A2. Understand the original calculation

The script uses:
```python
words = line.split()
chars = len(line)
per_line_fertility.append(len(tokens) / len(words))
per_line_tpc.append(len(tokens) / chars)
```

**FACT:** “word” means whitespace-separated item. `chars` means Python string length, i.e. Unicode code points for these strings.

The script calculates each line's ratio and then averages the line-level ratios, so fertility is a **macro-average**, not corpus-total tokens divided by corpus-total words.

## A3. Inspect the supplied sample

**ACTUAL:** first English line = 8 whitespace words / 64 characters. First Hindi line = 7 whitespace words / 30 characters.

**CALCULATION:**
- English: 64 / 8 = 8.00 characters per whitespace word.
- Hindi: 30 / 7 = 4.29 characters per whitespace word.

**INFERENCE:** tokens/word has a language-sensitive denominator and should not automatically be treated as a perfectly comparable cross-language measure.

## A4. Manually verify one Hindi line

Sentence:
```text
मुझे सुबह की चाय बहुत पसंद है।
```

**Command:**
```powershell
python -c "import tiktoken; s='मुझे सुबह की चाय बहुत पसंद है।'; t=tiktoken.get_encoding('gpt2').encode(s.lower()); print(t); print('tokens =', len(t))"
```

**ACTUAL:** 47 GPT-2 tokens.

Known values:
- tokens = 47
- whitespace words = 7
- Python characters = 30

**CALCULATIONS:**
- 47 / 7 = 6.7143 tokens/word
- 47 / 30 = 1.5667 tokens/code point

## A5. Verify the macro-average

**Command:**
```powershell
python -c "from fertility import read_lines, analyze, load_tokenizer; lines=read_lines(r'.\corpus_sample\hin_sample.txt'); enc=load_tokenizer('gpt2'); [(print(i+1, len(enc(x.lower())), len(x.split()), len(enc(x.lower()))/len(x.split()))) for i,x in enumerate(lines)]"
```

**ACTUAL line-level Hindi fertility:**
```text
6.714285714285714
7.625
6.714285714285714
7.285714285714286
6.8
8.0
8.428571428571429
8.75
6.666666666666667
9.0
```

**INFERENCE:** their arithmetic mean gives the reported ~7.60.

## A6. Macro vs micro fertility on the sample

**Command:**
```powershell
python -c "import tiktoken; from fertility import read_lines; enc=tiktoken.get_encoding('gpt2'); [(print(lang, 'tokens=',sum(len(enc.encode(x.lower())) for x in lines), 'words=',sum(len(x.split()) for x in lines), 'micro_fertility=',sum(len(enc.encode(x.lower())) for x in lines)/sum(len(x.split()) for x in lines))) for lang,lines in [('eng',read_lines(r'.\corpus_sample\eng_sample.txt')),('hin',read_lines(r'.\corpus_sample\hin_sample.txt'))]]"
```

**ACTUAL:**
```text
eng tokens= 99 words= 78 micro_fertility= 1.2692307692307692
hin tokens= 459 words= 61 micro_fertility= 7.524590163934426
```

**INFERENCE:** macro vs micro changes the result, but only slightly on this sample. It does not explain the large Hindi/English gap.

## A7. Test tokenizer dependence

**Hypothesis:** the large Indic penalty may depend strongly on tokenizer choice.

**Command:**
```powershell
python fertility.py --corpus eng=.\corpus_sample\eng_sample.txt --corpus hin=.\corpus_sample\hin_sample.txt --tokenizer hf:xlm-roberta-base
```

**ACTUAL:**
```text
eng                       1.30       0.228
hin                       1.45       0.303

hin is 1.11x the fertility of eng (worse tokenization)
```

**INFERENCE:** same corpus + different tokenizer changes Hindi fertility from 7.60 to 1.45. This strongly challenges the claim that the problem is inherent to the script and that any tokenizer will struggle.

## A8. Inspect UTF-8 representation

**Command:**
```powershell
python -c "import tiktoken; s='मुझे सुबह की चाय बहुत पसंद है।'; enc=tiktoken.get_encoding('gpt2'); b=s.encode('utf-8'); print('UTF-8 bytes =', len(b)); print('Characters =', len(s)); print('GPT-2 tokens =', len(enc.encode(s))); print('Bytes per character =', len(b)/len(s))"
```

**ACTUAL:**
```text
UTF-8 bytes = 78
Characters = 30
GPT-2 tokens = 47
Bytes per character = 2.6
```

**INFERENCE:** UTF-8 size is different from tokenization. It does not by itself prove causation.

---

# A1 — Proper Multilingual Evaluation Corpus

## A9. Assignment requirement

The assignment requires at least four languages including English, Hindi, and two Dravidian languages, and requires documented size, domain, preprocessing, and limitations. FLORES-200 is explicitly suggested.

## A10. Corpus choice

**DECISION:** FLORES-200 `devtest`.

**Languages:** English, Hindi, Kannada, Tamil.

**Reason:** parallel/aligned material lets us hold underlying content approximately constant across languages.

## A11. Verify FLORES English-Hindi

**ACTUAL:** `devtest` loaded with 1,012 rows and aligned English/Hindi fields.

## A12. Verify Kannada and Tamil

**ACTUAL:** English-Kannada and English-Tamil `devtest` datasets also contain 1,012 rows.

## A13. Verify full ID alignment

**Command:**
```powershell
python -c "from datasets import load_dataset; ds=[load_dataset('facebook/flores',c,split='devtest') for c in ['eng_Latn-hin_Deva','eng_Latn-kan_Knda','eng_Latn-tam_Taml']]; ids=[set(x['id'] for x in d) for d in ds]; print([len(x) for x in ids]); print('all IDs identical =', ids[0]==ids[1]==ids[2]); print('intersection size =', len(ids[0]&ids[1]&ids[2]))"
```

**ACTUAL:**
```text
[1012, 1012, 1012]
all IDs identical = True
intersection size = 1012
```

**CONCLUSION:** same 1,012 sentence IDs across the three pair datasets.

## A14. Preprocessing decision

**Minimal normalization:**
1. Unicode NFC normalization.
2. Collapse repeated whitespace.
3. Lowercase.
4. Preserve punctuation and linguistic content.

## A15. Repeated whitespace experiment

**Command:** compare single-space and double-space versions.

**ACTUAL:**
```text
English double space: 10 tokens, 7 words
English single space:  9 tokens, 7 words
Hindi double space: 44 tokens, 5 words
Hindi single space: 43 tokens, 5 words
```

**INFERENCE:** repeated whitespace can increase token count without increasing the word denominator.

## A16. Full-sample whitespace normalization

**ACTUAL:**
```text
eng raw_tokens= 99 normalized_tokens= 98 difference= 1
hin raw_tokens= 459 normalized_tokens= 458 difference= 1
```

**CONCLUSION:** real but small effect on the tiny sample.

## A17. Code points vs grapheme clusters

**Command:**
```powershell
python -c "import regex; s='मुझे सुबह की चाय बहुत पसंद है।'; print('code_points =', len(s)); print('grapheme_clusters =', len(regex.findall(r'\X', s))); print(regex.findall(r'\X', s))"
```

**ACTUAL:**
```text
code_points = 30
grapheme_clusters = 22
```

For 47 tokens:
- 47 / 30 = 1.567 tokens/code point
- 47 / 22 = 2.136 tokens/grapheme

**CONCLUSION:** character definition materially changes the metric for Indic scripts.

## A18. Full-corpus code point vs grapheme metric

**ACTUAL GPT-2:**
```text
eng tok/codepoint= 0.2121 tok/grapheme= 0.2121
hin tok/codepoint= 1.5300 tok/grapheme= 2.3349
kan tok/codepoint= 2.6663 tok/grapheme= 4.0782
tam tok/codepoint= 2.7273 tok/grapheme= 4.2168
```

**INFERENCE:** `tok/char` must be explicitly defined; the original script's value is tok/code point.

## A19. UTF-8 byte denominator

**ACTUAL GPT-2:**
```text
eng tok/codepoint= 0.2121 tok/byte= 0.2119
hin tok/codepoint= 1.5300 tok/byte= 0.5948
kan tok/codepoint= 2.6663 tok/byte= 0.9788
tam tok/codepoint= 2.7273 tok/byte= 0.9966
```

**INFERENCE:** bytes are an encoding-level denominator, not a linguistic unit.

## A20. Build evaluation corpus

Created `build_eval_corpus.py` and output:
```text
eval_corpus/
    eng.txt
    hin.txt
    kan.txt
    tam.txt
```

**ACTUAL:**
```text
sentences: 1012
eng : 1012
hin : 1012
kan : 1012
tam : 1012
```

## A21. GPT-2 baseline on the proper corpus

**ACTUAL:**
```text
eng                       1.29       0.214
hin                       7.87       1.529
kan                      23.00       2.664
tam                      25.25       2.725

hin is 6.11x the fertility of eng (worse tokenization)
kan is 17.86x the fertility of eng (worse tokenization)
tam is 19.61x the fertility of eng (worse tokenization)
```

## A22. XLM-R baseline on the proper corpus

**ACTUAL:**
```text
eng                       1.44       0.238
hin                       1.51       0.294
kan                       2.60       0.303
tam                       2.49       0.269

hin is 1.05x the fertility of eng (worse tokenization)
kan is 1.81x the fertility of eng (worse tokenization)
tam is 1.73x the fertility of eng (worse tokenization)
```

**CONCLUSION:** same 1,012-sentence corpus but dramatically different tokenizer behavior.

## A23. Macro vs micro on the proper corpus

**ACTUAL:**
```text
eng macro= 1.2874 micro= 1.2782 difference= 0.0092
hin macro= 7.8666 micro= 7.8263 difference= 0.0403
kan macro= 22.9964 micro= 22.7957 difference= 0.2007
tam macro= 25.2462 micro= 25.0429 difference= 0.2034
```

**CONCLUSION:** macro-vs-micro is a genuine methodological distinction, but not the main source of the huge gap.

## A24. Corrected fertility experiment

Created `fertility_corrected.py` using corpus-level (micro) denominators and explicit code-point/grapheme metrics.

**ACTUAL:**
```text
eng            1.278             0.212             0.212
hin            7.826             1.530             2.335
kan           22.796             2.666             4.078
tam           25.043             2.727             4.217
```

## A25. Audit the intern's serving-cost claim

Intern claimed roughly 6× serving cost for Hindi based on ~6× fertility.

**CONCLUSION:** fertility is a tokenizer measurement; it is not a measured billing/serving-cost result. No latency, GPU utilization, billing, or production request distribution was measured in Part A.

## A26. Corpus limitation statement

The 1,012-sentence FLORES-200 devtest set is substantially stronger than the original ~10-sentence sample, but it is still curated evaluation text. It does not fully represent production traffic such as the full distribution of sentence lengths, conversational queries, informal/noisy user text, spelling errors, emojis, code, highly technical content, or code-switched/mixed-language requests. Therefore the results describe tokenizer behavior on this evaluation corpus, not direct production token usage, latency, or serving cost.

---

# Part B — LLM Serving / Capacity Audit

## B1. Benchmark structure

The supplied benchmark has 13 runs: seven short-prompt runs and six long-prompt runs.

Long prompt = 3584 input tokens, 512 generated tokens.

**ACTUAL long-prompt rows:**

| Batch | reported tok/s | KV util | Preempted |
|---:|---:|---:|---:|
| 4 | 565.4 | 0.16 | 0 |
| 8 | 902.6 | 0.31 | 0 |
| 16 | 1311.4 | 0.62 | 0 |
| 24 | 1607.4 | 0.93 | 0 |
| 32 | 1384.0 | 0.97 | 7 |
| 48 | 1298.5 | 0.97 | 23 |

**Observation:** throughput rises to batch 24, then declines; preemption begins at batch 32 while KV utilization is very high.

## B2. KV-cache bytes per token

Model specification:
- 28 layers
- 8 KV heads
- head_dim 128
- FP16 KV cache

**CALCULATION:**

a K and V pair doubles the storage:

a token uses

a\n2 × 28 × 8 × 128 × 2 = **114,688 bytes/token**.

## B3. Full-context KV requirement

For 4096 tokens:

114,688 × 4096 = 469,762,048 bytes = **448 MiB**.

## B4. KV-capacity calculation and genuine correction

Initial attempt used:

24 × 0.92 − 1.6 = 20.48 GB

This omitted model-weight memory.

Model weights:
- 4.2B parameters
- FP16

4.2B × 2 bytes = 8.4 GB decimal ≈ 7.82 GiB.

Planning calculation:

24 × 0.92 − 8.4 − 1.6 = **12.08 GB** for KV under this simplified assumption.

12.08 × 10^9 / 2^20 ≈ **11,520.5 MiB**.

11,520.5 / 448 ≈ **25.7**.

**Revised theoretical capacity:** approximately **25 full 4096-token sequences**.

**Qualification:** the provided files do not document the benchmark harness's exact allocator interpretation of `gpu_memory_utilization`; therefore ~25 is a theoretical estimate under stated assumptions, not an exact scheduler threshold.

## B5. Compare theory with observed preemption

Each long-prompt request has:

3584 + 512 = **4096 tokens**.

Observed:
- batch 24: 0 preemptions
- batch 32: 7 preemptions
- batch 48: 23 preemptions

**Inference:** the theoretical ~25 full-context-sequence estimate is broadly consistent with the onset of resource pressure near batch 32, but it does not exactly predict scheduler behavior.

## B6. Determine what `reported_tok_s` measures

Batch-16 long prompt:
- requests = 16
- prompt = 3584
- generation = 512
- wall clock = 49.97 s
- reported = 1311.4 tok/s

Generated-only:

16 × 512 / 49.97 ≈ **163.94 tok/s**.

Prompt + generated:

16 × (3584 + 512) / 49.97 ≈ **1311.5 tok/s**.

**Conclusion:** `reported_tok_s` is effectively total prompt+generation throughput for these rows, not generated-only throughput.

## B7. Cross-check on short prompt

Batch 16 short prompt:
- prompt = 512
- generation = 256
- wall clock = 13.91 s
- reported = 883.2

16 × (512 + 256) / 13.91 ≈ **883.39 tok/s**.

This matches the reported counter within rounding.

## B8. B3 — batch-24 long-prompt goodput, Method 1

Batch 24, generation 512, wall clock 61.16 s.

24 × 512 = **12,288 generated tokens**.

12,288 / 61.16 = **200.92 generated tok/s**.

## B9. B3 — Method 2

24 × (3584 + 512) = 98,304 total prompt+generation tokens.

98,304 / 61.16 ≈ 1607.33, matching the reported 1607.4.

Generated fraction = 512 / 4096 = 0.125.

1607.4 × 0.125 ≈ **200.93 generated tok/s**.

Methods agree: **200.92 ≈ 200.93 tok/s**.

## B10. Explain the long-context anomaly

Batch 16 short prompt:

16 × 256 / 13.91 = **294.46 generated tok/s**.

Batch 16 long prompt:

16 × 512 / 49.97 = **163.94 generated tok/s**.

But raw `reported_tok_s` is:
- short = 883.2
- long = 1311.4

Therefore raw total-token throughput makes long prompts look faster, while generated-token goodput shows the long-prompt case is slower.

**Conclusion:** the intern misinterpreted prompt+generation throughput as generated-token throughput.

## B11. Disprove linear batch scaling

Intern predicted batch 48 ≈ 3200 tok/s by scaling linearly from ~1600 tok/s.

Actual long-prompt reported throughput:
- 16 = 1311.4
- 24 = 1607.4
- 32 = 1384.0
- 48 = 1298.5

Actual long-prompt generated goodput:
- 16 = 163.94
- 24 = 200.92
- 32 = 172.99
- 48 = 162.31

**Conclusion:** throughput is not linear across batch size once resource pressure/preemption appears.

## B12. B4 metric and scoped recommendation

For predicting **output generation capacity**, use **generated-token goodput** because it isolates generated tokens from prompt-processing tokens.

Long-prompt generated goodput peaks at batch 24:

**~200.92 generated tok/s with 0 preemptions.**

**Recommendation:** batch 24 is the best observed operating point **for the tested long-prompt workload**.

**Scope correction:** this must not be generalized to every workload. In the same CSV, short-prompt generated goodput continues rising through batch 64 to about 755.72 tok/s.

---

# Part C — Decision Memo

## C1. Exact scenario constraints

Six target languages:
Hindi, Kannada, Tamil, Telugu, Bengali, Marathi.

Constraints:
- 1 A100-80GB
- 2 weeks
- 1 native-speaker reviewer
- reviewer covers Hindi + Kannada
- 10 h/week
- launch review in 3 weeks
- no external API budget

## C2. Reviewer capacity

**ASSUMPTION:** 2 minutes per pairwise comparison.

20 reviewer-hours over two weeks gives:

20 × 60 / 2 = **600 comparisons**.

Approximate reviewer capacity = 30 comparisons/hour.

This is a planning assumption, not a measured reviewer benchmark.

## C3. Primary success metric

**Casualness win rate:** candidate wins / total pairwise comparisons.

Reason: measures improvement directly against the current baseline.

**Guardrail:** no obvious semantic/correctness regression.

## C4. Numeric success threshold

**ASSUMPTION:** ≥ **70% casualness win rate** with no obvious correctness regression.

This threshold is a planning assumption because the assignment does not prescribe a numeric cutoff.

## C5. Option comparison

### (a) SFT on synthetic casualized response pairs

**Pros:** directly changes model behavior; no second inference model is inherently required; potentially strongest long-term behavioral control.

**Cons:** synthetic-data quality risk; training consumes A100/time; iteration is slower; reviewer capacity makes exhaustive validation infeasible; only Hindi/Kannada have direct native-speaker coverage.

### (b) ≤1B inference-time rewriter

**Pros:** main model remains unchanged; focused style transformation; easier to disable/replace than retraining the main model.

**Cons:** adds inference latency and compute/memory demand; adds deployment/monitoring complexity; can change meaning while changing style; exact serving cost is not provided.

### (c) Prompt engineering only

**Pros:** minimal implementation and serving cost; fastest iteration; no additional model; easy rollback; best fit for launch deadline.

**Cons:** may not be strong or consistent enough; relies on existing model instruction-following.

## C6. SFT data-volume planning assumption

**ASSUMPTION:** 500 synthetic pairs per language.

500 × 6 = **3,000 pairs**.

Manual review of all 3,000 pairs is infeasible with 20 reviewer-hours, so SFT would require automated checks + sampled human review + final output evaluation.

Exact SFT GPU cost cannot be calculated honestly from the scenario because base model, sequence length, batch size, and optimization steps are unspecified.

## C7. Day-1 experiment

Compare baseline vs prompt-engineered system on:
- 30 Hindi prompts
- 30 Kannada prompts
- 60 total pairwise comparisons

At 2 min/comparison:
60 × 2 = 120 minutes = **2 reviewer-hours**.

Decision rule:
- ≥70% win rate with no obvious correctness regression → prompting is sufficient.
- <70% → test the rewriter.
- If rewriter also fails → consider SFT.

## C8. Kill criterion

Abandon prompt engineering **after the Day-1 pilot** if it fails the 70% casualness-win threshold.

## C9. Final recommendation

**Prompt engineering first and preferred by default.**

Rationale: lowest training cost, lowest serving complexity, fastest iteration, easiest rollback, and best fit to the schedule/reviewer constraints.

Escalation:
```text
Day 1 prompt pilot
        |
   >=70%? ---- Yes ---> prefer prompting
        |
       No
        v
    test rewriter
        |
     passes? ---- Yes ---> prefer rewriter
        |
       No
        v
    consider SFT
```

---

# Genuine Revision / Error Log

## Revision 1 — KV capacity
Initial capacity estimate omitted model-weight memory and gave ~43 full-context sequences. Revised estimate includes 4.2B FP16 weights and gives ~25 under the stated planning assumptions.

## Revision 2 — `reported_tok_s`
Initially treated as generated-token throughput. Benchmark arithmetic showed it includes prompt + generated tokens for the supplied rows. Subsequent goodput calculations use generated tokens only.

## Revision 3 — Long-context conclusion
Raw `reported_tok_s` suggested long prompts were faster, but generated-token goodput showed the batch-16 long-prompt case was slower than the short-prompt case.

## Revision 4 — Batch-24 scope
Batch 24 is the highest observed point for the **long-prompt workload**, not for all prompt lengths. Short-prompt goodput rises through batch 64.

---

# Final Status

## Part A
Core tokenizer audit and corrected multilingual evaluation completed. The main evidence is tokenizer dependence, denominator sensitivity, the inadequacy of the original tiny corpus, and the unsupported leap from fertility to serving cost.

## Part B
Core KV-cache/capacity audit and throughput-counter audit completed. The important corrections are the model-weight memory correction and the distinction between total-token throughput and generated-token goodput.

## Part C
All three candidate paths evaluated; assumptions, metric, threshold, reviewer arithmetic, kill criterion, day-1 experiment, and recommendation defined. Final recommendation: prompt engineering first, with evidence-based escalation.

## Documentation still required
`AI_USAGE.md` should separately record actual AI assistance used during the work. Do not invent AI mistakes, experiments, or dead ends that did not occur.
