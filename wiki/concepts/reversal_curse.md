---
title: "Reversal Curse"
related_concepts: ["directional_asymmetry", "causal_arrow", "pretraining_prior", "masked_diffusion_models"]
source_refs: ["raw/arrow_of_learning-7.md", "raw/paper-draft-direction.md", "raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["reversal_curse", "logical_reasoning"]
---

# Reversal Curse

The inability of autoregressive LLMs to generalize from "A is B" to "B is A" even when the relation is bijective. First systematically documented by Berglund et al. (2023).

## Canonical example

Fine-tune an LLM on synthetic fact "Uriah Hawthorne is the composer of Abyssal Melodies":
- Forward: "Who is the composer of Abyssal Melodies?" → "Uriah Hawthorne" (high accuracy)
- Inverse: "What did Uriah Hawthorne compose?" → random chance

The failure persists even when both entities are unique and the relationship is 1-to-1 (`K=1`).

## Mechanism

The reversal curse is a **Causal × Data** coupling effect, not a pure architectural flaw:

1. **Gradient flow asymmetry under causal masking**. With the triangular mask, token `A`'s representation is updated to help predict a following token `B`, but `A` never receives gradient signal from preceding tokens. If the training data only shows "A is B", `B`'s weights get updated to be predicted from `A`, but `A`'s weights are never updated to be predicted from `B`. The representation is a **directed lookup table**, not a relational graph.

2. **Data asymmetry**. Language orders information (subject → predicate, cause → effect), reinforcing the one-directional flow permitted by the mask.

The [[reversal_invariance]] theorem says the objective is direction-blind in theory — but in practice we apply a **unidirectional mask** to **unidirectionally ordered data**, so one direction is trained and the other is not.

## Severity in [[directional_asymmetry]] experiments

On Sahasrabudhe's synthetic wind-tunnel, the reversal curse emerges most severely when the inverse has high conditional entropy (many-to-one mappings, `H(A|B) = log K`). At K=8 with QLoRA on Qwen-2.5-3B, the B→A loss stays at its initialization value (~4.67) while A→B drops to 2.97.

## Mitigations

- **Reverse training** (Berglund-style data augmentation): train on explicitly reversed strings
- **Bidirectional attention** (BERT): does not suffer the curse but is not generative
- **[[masked_diffusion_models]]**: train to reconstruct masked tokens from any context, implicitly coupling `P(A|B)` and `P(B|A)`. Reported to escape the reversal curse.
- **Full fine-tuning** instead of LoRA — if invertibility matters, the adapter space is too small.

## Relation to other directional phenomena

The reversal curse is the **logical/factual** manifestation of [[directional_asymmetry]]. The [[conditional_entropy_barrier]] is the **optimization-dynamics** manifestation. Both are instances of the same underlying Causal × Data × Optimizer interaction.
