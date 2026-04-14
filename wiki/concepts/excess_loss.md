---
title: "Excess Loss"
related_concepts: ["conditional_entropy_barrier", "optimization_arrow", "wind_tunnel_methodology"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["metric", "information_theory"]
---

# Excess Loss

A metric for quantifying [[directional_asymmetry]] that normalizes out the information-theoretic floor of each task, so forward and inverse learning can be compared on a common scale.

## Definition

```
L_excess = L_observed − L_min
```

where `L_min` is the Shannon information-theoretic minimum for the task:

- Forward A→B (deterministic, `H(B|A)=0`): `L_min^{A→B} = 0`
- Inverse B→A (`K` preimages, `H(A|B)=log K`): `L_min^{B→A} = log K`

## Why the normalization matters

Raw cross-entropy loss is not comparable between forward and inverse tasks: the inverse task has a higher floor by construction (`log K` vs 0). A model that achieves `L_observed = log K + 0.1` on the inverse is doing **nearly optimal** work — the residual `0.1` is the real learning difficulty.

Subtracting the floor reveals the **directional gap** `Δ_dir = L_excess^{B→A} − L_excess^{A→B}`. A direction-neutral optimizer achieves `Δ_dir ≈ 0`.

## Empirical use

The [[five_arrows_framework]] survey reports:

- Causal transformers at K=5: `Δ_dir ≈ 1.16 nats` (the [[conditional_entropy_barrier]] / Causal Tax)
- Non-causal MLPs on same data: `Δ_dir ≈ 0.22 nats`

The transformer gap is ~5× the MLP gap. This confirms the [[optimization_arrow]] attributes primarily to the causal inductive bias, not to data structure alone.

## Caveat

Computing `L_min^{B→A} = log K` assumes the target distribution is **uniform** over the K preimages. If the model is predicting a specific preimage (e.g., the training-time one), the floor is 0 and excess loss becomes raw loss. The metric is most meaningful when the evaluation protocol scores "any valid preimage" as correct.
