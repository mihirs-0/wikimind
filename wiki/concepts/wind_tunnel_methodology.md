---
title: "Synthetic Wind-Tunnel Methodology"
related_concepts: ["directional_asymmetry", "conditional_entropy_barrier", "excess_loss"]
source_refs: ["raw/arrow_of_learning-7.md", "raw/paper-draft-direction.md", "raw/directionality-conditional-complexity_-a1-a2-1.md", "raw/directionality-conditional-complexity_-a1-a2-1-part-2.md"]
last_updated: 2026-04-14
tags: ["methodology", "synthetic_data", "benchmark"]
---

# Synthetic Wind-Tunnel Methodology

A controlled experimental protocol for probing directional learning dynamics without linguistic confounds. The "wind tunnel" metaphor: strip out all real-world turbulence (semantics, tokenizer artifacts, corpus bias) so the only remaining variable is conditional entropy.

## Core construction

1. **Alphabet**: 36 characters (a–z + 0–9), or a 128-token integer vocabulary for pure-tokenizer isolation.
2. **String length**: fixed per experiment (typically 4 or 8).
3. **Many-to-one mapping**: choose branching factor `K ≥ 1`. Sample `n_targets` unique `B` strings. For each `B`, sample `K` distinct `A` strings. Each pair `(A, B)` has a unique `A` but shared `B`.

This induces a clean entropy asymmetry:

- Forward A→B: `H(B|A) = 0` — deterministic (compression-like)
- Inverse B→A: `H(A|B) = log K` — uniform over K preimages (decompression-like)

`K=1` gives a bijective control where both directions are informationally symmetric — **any observed asymmetry must therefore be directional, not entropic**.

## Symmetric prompt format

```
input format:  "x: {INPUT} y: {TARGET}"
direction A→B: INPUT=A, TARGET=B
direction B→A: INPUT=B, TARGET=A
```

Both directions use **identical** architecture, tokenizer, template, optimizer, loss function, and dataset size. The only difference is which element of the pair is the target.

## Target-only loss

Prompt tokens are labeled `-100` and ignored by cross-entropy. Only `TARGET` tokens contribute to the loss. This removes prompt-structure and boilerplate-memorization confounds.

## Cluster-aware split (for K > 1)

For each `B` cluster with `K` preimages:
- `K ≥ 3`: K-2 pairs train, 1 validation, 1 test
- `K = 2`: 1 train, 1 test
- Every cluster appears in all splits, but no exact `(A, B)` pair is duplicated across train and test.

This forces cluster-level generalization and prevents pair memorization.

## Training regimes compared

The protocol is run across:

1. **From-scratch**: 4-layer 8-head 512-dim GPT-2-style, random init — no language priors
2. **Full fine-tune**: pretrained GPT-2 (125M), all weights trainable
3. **LoRA (r=32, α=64)** on GPT-2; **QLoRA 4-bit** on 7B models (Qwen-2.5, Mistral, Llama-2)

Regimes 1 and 2 isolate the [[pretraining_prior]] contribution; regimes 2 and 3 isolate the [[lora_bottleneck]].

## Why it works

Because the task has **no semantics, no lexical frequency, no morphology, no world knowledge**, any directional gap observed in pretrained-but-not-from-scratch models must be a **learned property of the weights**, not a property of the task. This is the protocol's main epistemic lever.

## Limitations

- Short sequences (L=4 or 8); no long-range dependency structure
- Fixed K per experiment — no mixed-entropy corpus
- No mechanistic probing — the protocol measures behavior, not internal pathways
- Character-level tokenization (in some runs) may interact with forward/backward asymmetry in ways untested

## Source implementation

Full `gpt2.py` script lives in `raw/directionality-conditional-complexity_-a1-a2-1-part-2.md` — GPT-2 config: `d_model=512, n_layer=8, n_head=8, d_ff=2048, dropout=0.1`. Train/val/test fractions 0.8/0.1/0.1. AdamW lr 2e-4, batch 64.
