---
title: "A1 & A2 Experiments on Directionality and Conditional Complexity"
source: raw/directionality-conditional-complexity_-a1-a2-1.md
source_refs: ["raw/directionality-conditional-complexity_-a1-a2-1.md"]
ingested_at: 2026-04-14
tags: ["experiment_log", "synthetic_benchmark", "from_scratch", "gpt2"]
---

# A1 & A2: Directionality and Conditional Complexity (detailed experiment doc)

Sahasrabudhe's detailed experimental protocol for the original A1/A2 experiments that seeded the [[wind_tunnel_methodology]].

## Setup (shared across A1, A2)

- **Model**: GPT-2 `n_layer=4, n_head=8, n_embd=512`, vocab 50257, **randomly initialized** (no pretraining)
- **Tokenizer**: GPT-2 BPE with `pad_token=eos_token`
- **Optimizer**: AdamW, lr 2e-4, batch 64, 3 epochs
- **Prompt template**: `"x: {INPUT} y: {TARGET}"`, target-only loss (prompt tokens labeled `-100`)
- **Alphabet**: 36 chars (a-z + 0-9), string length L=8

## A1 — Bijection parity test

1-to-1 mapping A↔B via random permutation cipher. Trains two models with identical everything except input/target role.

**Result**: final val loss gap ≈ **0.03 nats** (negligible). Confirms architecture is direction-agnostic when conditional entropy is symmetric.

## A2 — Many-to-one test

~5 distinct A's per B (K=5). A→B has `H(B|A)=0`; B→A has `H(A|B)=log K ≈ 1.61`.

**Result**: final train-loss gap ≈ **0.40 nats**, B→A worse. Consistent across seeds.

## Interpretive claim

Training difficulty tracks **conditional complexity** `H(target | input)`, not just exposure frequency. Identical data, identical architecture, identical templates — the only difference is which side is context.

## Tension with [[learning-has-an-arrow]]

The v7 ICML manuscript claims **zero** from-scratch gap. This document — and part 2's training logs — show a **0.4-nat** gap at K=5 from scratch. Possible explanations:

- Different training budget (longer runs might close the gap)
- Different string length or sample count
- Different seeds — part-2 logs at `size=small/medium, K=5` show A→B and B→A reaching 0.0007 val loss **identically**, suggesting the gap disappears with enough data/compute

Flagged for reconciliation in [[conditional_entropy_barrier]].
