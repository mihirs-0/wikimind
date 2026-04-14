---
title: "First-Principles Analysis of the Disambiguation Lag"
source: raw/firstprinciples_disamb.md
source_refs: ["raw/firstprinciples_disamb.md"]
ingested_at: 2026-04-14
tags: ["disambiguation_lag", "first_principles", "attention_geometry", "binding_problem"]
---

# On the Geometric Origin of the Disambiguation Lag — First-Principles Analysis

Long-form theoretical exposition of the [[disambiguation_lag]]. Same result as `geometric-origin-disambiguation-lag` and `disambiguation-mathematical-formalization` but with maximum explanatory detail and additional mechanistic discussion.

## Distinctive contributions

### Score-Probability-Utility (SPU) framework

Decomposes attention dynamics into three quantities per key:

- **Score** `s_j` (the attention logit)
- **Probability** `p_j = softmax(s)_j`
- **Utility** `u_j = -⟨∇_c L, v_j⟩` (the loss reduction from attending to j)

Gradient `∂L/∂s_j = p_j (u_j - ū)` where `ū` is the policy-average utility. At the plateau, the **advantage** `A_z ≈ 0` because z's value vector provides no consistent utility signal across B-groups.

### Why the plateau is FIM-maximal

Fisher Information Matrix of the attention distribution `F = (1/τ²)(D − pp^T)`. At the plateau where `p ≈ (1/2, 1/2)`, F has eigenvalues 0 and `1/(2τ²)` — the **maximum** sensitivity. The model is *maximally receptive* to learning signals at the plateau; the bottleneck is the absence of a consistent advantage signal, not any rigidity in the attention machinery.

### The capacity wall (Proposition 1 with proof sketch)

Linear `y = W_b e_b + W_z e_z` cannot disambiguate because z's contribution `W_z e_z` is B-independent. The optimal additive solution is the group-mean predictor with loss log K. Confirmed empirically: 200K-step linear runs never escape the plateau across `η ∈ {1e-3, 1e-2, 1e-1}`.

### The K → 7 phase boundary

Q vs log K line passes through zero at K* ≈ 7 — the critical K below which the barrier is shallow enough for SGD noise to cross without a distinct phase transition. Mapping `K_crit(d, η, B_batch)` is open future work.

### Suggested direct measurement

Log `Var_data(A_z)` and `E_data[A_z]` during training. Theory predicts variance is large during plateau (inconsistent z-utility across groups) and sharply decreases at transition. `E[A_z]` should be ~0 during plateau and become positive at transition.

## Status

Pre-v4 framing: claims gradient-cancellation across groups is the plateau mechanism. v4 ([[circuit-discovery-latency]]) showed this is **wrong** via the z-sharing ablation. The local mechanistic content (advantage dynamics, FIM analysis, capacity wall, phase boundary) survives; the cross-group cancellation argument does not.
