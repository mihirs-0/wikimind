---
title: "Causal Arrow"
related_concepts: ["five_arrows_framework", "reversal_curse", "pretraining_prior"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["causality", "arrows_of_time", "attention_mask"]
---

# Causal Arrow

The logical-structural axis of irreversibility in the [[five_arrows_framework]]. Describes the inability of autoregressive transformers to generalize across the direction of a learned causal dependency.

## Canonical manifestation

The [[reversal_curse]]: a model fine-tuned on "A is B" fails on "B is A" even when the relation is 1-to-1.

## Structural origin

**Causal mask + data order = one-way gradient flow.**

- Token `t` can only attend to tokens `1..t` (triangular mask). Information flow is a directed acyclic graph, strictly past → future.
- During training, gradients updating token `A`'s representation come from loss at positions where `A` precedes the target. Token `A` never receives gradient from any position preceding it.
- So if training only presents "A is B", `B`'s representation learns to be predicted from `A`, but `A`'s representation is never updated to be predicted from `B`.

The stored knowledge is a **directed lookup table**, not a relational graph with back-pointers.

## The Reversal Invariance paradox

The [[reversal_invariance]] theorem says the NLL objective is symmetric between a corpus and its reversal. So why is the Causal Arrow so severe?

**Resolution**: the theorem assumes we could re-train on the reversed corpus. It does not guarantee that a model trained on `D` generalizes to `T(D)`. The Causal Arrow emerges from applying a unidirectional mask to unidirectionally ordered data — not from the objective itself.

## Escape routes

- Bidirectional attention (BERT) — cannot generate autoregressively, but learns symmetric associations
- [[masked_diffusion_models]] — train to reconstruct masked tokens from any context, positively correlating `P(A|B)` and `P(B|A)`
- Reverse training — explicit data augmentation with reversed strings
