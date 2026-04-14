---
title: "Directional Asymmetry in Transformers (paper draft)"
source: raw/paper-draft-direction.md
source_refs: ["raw/paper-draft-direction.md"]
ingested_at: 2026-04-14
tags: ["reversal_curse", "directional_asymmetry", "lora", "pretraining_prior"]
---

# Directional Asymmetry in Transformers — Compounding Effects of Pretraining Priors and Adaptation Bottlenecks

Mihir Sahasrabudhe's earlier paper draft proposing a **three-tier** explanation of the [[reversal_curse]]. Same experimental core as [[learning-has-an-arrow]] but with a stronger claim about architecture.

## Three-tier explanation

1. **Architecture** — transformers exhibit a **modest but consistent** [[conditional_entropy_barrier]] even from scratch. At K=5: A→B ~2.1 train loss vs B→A ~4.9. This is a real but small effect.
2. **Pretraining priors** — language pretraining **amplifies** the architectural bias. 125M GPT-2 full fine-tune at K=8: A→B drops 4.24 → 2.21, B→A flat 5.15 → 5.13.
3. **Adaptation bottlenecks** — LoRA/QLoRA **lock in** the prior. Low-rank update has enough capacity to specialize for compatible tasks (A→B) but not to override the prior for incompatible ones (B→A). Reverse loss worsens over training.

## Interpretive frame

Transformers are **compression-biased learners**. Forward direction behaves like compression (many → one); inverse behaves like decompression (one → many). Under LoRA the system is "×2 compressed" — compressed world-model + compressed adaptation channel — so decompression tasks become structurally unlearnable. Aligns with MDL / information bottleneck intuitions.

## Architectural alternatives suggested

Bidirectional objectives (BERT-style, [[masked_diffusion_models]]), reversible architectures, entropy-regularized losses, cycle-consistency training, auxiliary inverse supervision.

## Status

This is an earlier draft; the published v7 ([[learning-has-an-arrow]]) tones down the from-scratch claim to "no gap", attributing the earlier gap to setup artifacts. See [[conditional_entropy_barrier]] for reconciliation.
