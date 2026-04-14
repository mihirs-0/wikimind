---
title: "Reversal Invariance (theorem)"
related_concepts: ["directional_asymmetry", "causal_arrow", "five_arrows_framework"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["theory", "symmetry", "nll"]
---

# Reversal Invariance

A theoretical result (Papadopoulos et al. 2024 and follow-ups) stating that the negative log-likelihood objective is **symmetric** between a training corpus and its exact reversal, under appropriate conditions.

## Formal statement

Let `D` be a training corpus, `T(D)` its exact reversal, and `L_NLL(θ; τ, D)` the NLL loss for model parameters `θ` and tokenizer `τ`. Under:

- **Tokenization stability**: tokenization of `D` and `T(D)` yields reversed token sequences (no merges or splits that break when reversed)
- **Appropriate positional encoding**: e.g., symmetric or learned encodings that don't bake in forward bias

there exists a parameter map `Ψ` such that:

```
L_NLL(θ; τ, D) = L_NLL(Ψ(θ); τ_T, T(D))
```

## Interpretation

The objective function is **direction-blind**. It cannot distinguish forward training from backward training — both minimize the same quantity up to a parameter re-labelling. `A → B` and `B → A` are equally valid statistical dependencies from the loss's perspective.

## The paradox this creates

Real transformers exhibit strong [[directional_asymmetry]]:

- [[reversal_curse]]: models fail to infer `B → A` despite learning `A → B`
- Forward < backward perplexity on natural text (Papadopoulos 2024)
- [[conditional_entropy_barrier]] on synthetic data

If the objective is direction-blind, where does the asymmetry come from?

## Resolution

The theorem assumes the model could also be trained on `T(D)`. It does not say that a model trained on `D` generalizes to `T(D)`. The asymmetry emerges from the **system**:

- **Data** is unidirectionally ordered (cause → effect, subject → verb)
- **Architecture** imposes unidirectional flow (causal mask)
- **Optimizer** traverses an asymmetric loss landscape induced by the unidirectional data × mask coupling
- **Pretraining** consolidates the asymmetry into rigid priors

So reversal invariance is a statement about the **objective**, not about the **model**. The [[five_arrows_framework]] enumerates the distinct subsystems that break the symmetry.

## Why this matters

Reversal invariance is the theoretical baseline that forces us to locate the source of asymmetry precisely. Without it, directional failures would be trivially attributed to "the loss prefers forward". With it, we must explain each asymmetry mechanism individually — which is what the five arrows do.
