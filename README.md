# LLM Tokenizer & Serving Audit

This repository contains the audit of a previous tokenizer-fertility and LLM-serving analysis, including reproduction, corrected experiments, and the final product recommendation.

## Part A — Tokenizer Audit

- Reproduced the original `fertility.py` experiment.
- Audited the fertility denominator and averaging method.
- Tested whitespace normalization and Unicode character definitions.
- Built a multilingual FLORES-200 evaluation corpus.
- Compared GPT-2 and XLM-R tokenizer behavior.

## Part B — LLM Serving / Capacity Audit

- Derived KV-cache memory per token.
- Estimated theoretical full-context sequence capacity.
- Audited benchmark throughput and preemption behavior.
- Identified what `reported_tok_s` measures.
- Calculated generated-token goodput.
- Evaluated batch-size scaling for the long-prompt workload.

## Part C — Decision Memo

Compared three approaches:

1. SFT on synthetic casualized response pairs
2. A ≤1B inference-time rewriter
3. Prompt engineering only

The recommendation was made using the assignment's hardware, schedule, reviewer, language-coverage, and budget constraints.

## Repository Structure

```text
├── fertility.py
├── fertility_corrected.py
├── build_eval_corpus.py
├── NOTEBOOK.md
├── AI_USAGE.md
├── DECISION_MEMO.md
├── REPORT_v0.md
│
├── corpus_sample/
│   ├── eng_sample.txt
│   └── hin_sample.txt
│
├── eval_corpus/
│   ├── eng.txt
│   ├── hin.txt
│   ├── kan.txt
│   └── tam.txt
│
└── bench/
    ├── model_spec.md
    └── bench_log.csv
```

## Reproduction

### Original tokenizer experiment

```powershell
python fertility.py --corpus eng=.\corpus_sample\eng_sample.txt --corpus hin=.\corpus_sample\hin_sample.txt --tokenizer gpt2
```

### Multilingual GPT-2 evaluation

```powershell
python fertility.py --corpus eng=.\eval_corpus\eng.txt --corpus hin=.\eval_corpus\hin.txt --corpus kan=.\eval_corpus\kan.txt --corpus tam=.\eval_corpus\tam.txt --tokenizer gpt2
```

### XLM-R comparison

```powershell
python fertility.py --corpus eng=.\eval_corpus\eng.txt --corpus hin=.\eval_corpus\hin.txt --corpus kan=.\eval_corpus\kan.txt --corpus tam=.\eval_corpus\tam.txt --tokenizer hf:xlm-roberta-base
```

### Build the evaluation corpus

```powershell
python build_eval_corpus.py
```

## Key Findings

- The original tokenizer experiment was approximately reproducible.
- The original fertility metric uses whitespace-separated words and a per-line macro-average.
- Macro vs. micro averaging changes the full-corpus results only modestly.
- Repeated whitespace can affect tokenizer counts.
- The original `tok/char` metric counts Unicode code points.
- Code-point, grapheme-cluster, and UTF-8-byte denominators produce different measurements for Indic languages.
- GPT-2 shows much higher Indic fertility than XLM-R on the same evaluation corpus, demonstrating strong tokenizer dependence.
- Tokenizer fertility alone does not establish a proportional serving-cost difference.
- `reported_tok_s` includes prompt and generated tokens for the tested benchmark rows.
- Generated-token goodput is therefore the appropriate metric for generation-capacity comparisons.
- For the tested long-prompt workload, batch 24 produced the highest observed generated-token goodput without preemption.

## Documentation

- **`NOTEBOOK.md`** — chronological experiment log, results, reasoning, and corrections.
- **`AI_USAGE.md`** — disclosure of AI assistance and genuine corrections during the analysis.
- **`DECISION_MEMO.md`** — final Part C recommendation.
- **`REPORT_v0.md`** — original previous-intern report preserved for audit purposes.

## Notes

The original implementation and report are preserved alongside the corrected experiments. The virtual environment and other machine-specific files are excluded through `.gitignore`.
