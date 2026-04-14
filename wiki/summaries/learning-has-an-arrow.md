---
title: "Learning Has an Arrow: Why LLMs Can Learn A→B but Not B→A"
source: raw/arrow_of_learning-7.md
source_refs: ["raw/arrow_of_learning-7.md"]
ingested_at: 2026-04-14
tags: ["reversal_curse", "directional_asymmetry", "lora", "synthetic_benchmark"]
---

# Learning Has an Arrow (ICML-style manuscript, v7)

Mihir Sahasrabudhe's ICML-style manuscript arguing that **directional asymmetry in LLMs is not inherent to the transformer architecture** — it is **learned during pretraining** and **amplified by low-rank adaptation**.

## Experimental design

Fully synthetic, language-free: random 36-character-alphabet strings `(A, B)` of length 4 or 8. A many-to-one mapping where `K` distinct `A` strings map to one `B` gives `H(B|A)=0` (forward / compression) and `H(A|B)=log K` (inverse / decompression). `K=1` is the bijective control. Three regimes are compared:

1. From-scratch GPT-2-style (4-layer, 8-head, 512-dim) trained only on synthetic pairs
2. Full fine-tuning of pretrained GPT-2 (125M, all weights trainable)
3. LoRA (r=32, α=64, ~2.5% trainable) on GPT-2; QLoRA on Qwen-2.5-7B, Mistral-7B, Llama-2-7B

## Key findings

- **From-scratch**: forward and reverse converge **identically** across seeds, even at K=5. No architectural directional bias.
- **Full fine-tune**: A→B drops from ~4.24 to ~2.21 val loss; B→A stays flat (~5.15 → ~5.13). Pretraining introduces the gap.
- **LoRA**: A→B matches full fine-tuning; B→A **degrades** over training (4.88 → 5.30). Frozen backbone + low-rank update = catastrophic collapse on high-entropy inverses.
- **7B scale (QLoRA)**: Pattern replicates on Qwen-2.5-3B (gap 0.01 → 0.39 → 0.63 → 1.70 nats as K: 1→4→5→8), GPT-2-XL (gap 0.01 → 0.75 → 1.71), Llama-2-7B (gap 1.42 at K=5).

## Thesis

Directional asymmetry decomposes into two factors:
1. Pretraining introduces a strong compression-oriented [[pretraining_prior]].
2. Low-rank adaptation **amplifies** the prior into structural failure — the low-rank update space cannot override the frozen base.

The [[reversal_curse]] is therefore not a semantic quirk of language but a property of **how pretrained transformers are adapted**.

## Notable contradictions with earlier drafts

This v7 claims **zero** from-scratch gap. Earlier manuscripts in the same cluster (`raw/paper-draft-direction.md`, `raw/directionality-conditional-complexity_-a1-a2-1.md`) reported ~0.4 nats of from-scratch gap at K=5. See `## Open Questions` in [[conditional_entropy_barrier]].
