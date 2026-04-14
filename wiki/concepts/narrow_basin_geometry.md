---
title: "Narrow Basin Geometry (Disambiguation Circuit)"
related_concepts: ["disambiguation_lag", "three_scaling_laws", "phase_transition_symmetry_breaking"]
source_refs: ["raw/disambiguation_lag_v4_circuit_discovery.md"]
last_updated: 2026-04-14
tags: ["loss_landscape", "circuit_discovery", "geometry"]
---

# Narrow Basin Geometry

The surviving explanation for the [[disambiguation_lag]] after two earlier mechanistic hypotheses (cross-group gradient cancellation and Kramers-style thermodynamic escape) were falsified by targeted ablations in `raw/disambiguation_lag_v4_circuit_discovery.md`.

## The picture

The disambiguation circuit is a **narrow basin in parameter space**. To work, it requires a coordinated configuration of:

1. Attention weights (`W_Q`, `W_K`) routing sufficient mass to the z-position
2. Value matrices (`W_V`) producing distinguishable context-vector perturbations for each `z_k`
3. Output projection (`W_U`) decoding those perturbations as the correct candidates

No single update to one matrix in isolation produces a descent signal — adjusting `W_V` without `W_U` produces undecodable perturbations; adjusting `W_U` without `W_V` has nothing to decode. The plateau is sustained by this **coordination barrier**.

## Three lines of evidence

### 1. Learning rate sweep (Law 2 of [[three_scaling_laws]])

`τ ∝ η^+0.8` — higher η makes the plateau **longer**, with complete failure above `η* ≈ 5×10⁻³`. This rules out noise-assisted (Kramers) escape, where higher temperature should accelerate barrier crossing. Interpretation: at high η, optimizer steps are too coarse to enter the narrow basin; at `η = 5×10⁻³` the basin is never entered at all.

The total parameter displacement `η · τ` grows as `η^2.1` — large steps don't merely fail to help, they force a longer wasted trajectory.

### 2. Gradient norm during plateau (Law 3)

`ḡ²_plateau ∝ K^-0.6` — within-batch gradients from K competing candidate directions partially cancel. The gradient signal is suppressed precisely when the search space is largest. Snaps to K-independent ~6.2 at the transition (the optimizer's "terminal velocity" once symmetry breaks).

### 3. Architecture comparison

`τ_Transformer > τ_LSTM > τ_GatedMLP`. The Gated MLP has the multiplicative B×z interaction **pre-wired** — it doesn't have to discover that the routing should be multiplicative, only what to compute. Halves the discovery cost. Direct evidence the plateau is **circuit discovery latency**, not intrinsic task difficulty.

Linear models never escape: the basin **doesn't exist** in their parameter space (capacity failure, Prop 1).

## Connection to plateau scaling

Combining gradient suppression (`K^-0.6`) and basin narrowing:

- If plateau is a random walk with step `g` toward a fixed-distance target: `τ ∝ 1/g² ∝ K^+0.6`
- Measured: `τ ∝ K^1.3`
- Gap of 0.7 attributed to the basin itself becoming narrower at larger K (more candidate routings must be simultaneously correct)

This decomposition `1.3 ≈ 0.6 + 0.7` is suggestive but lacks a formal derivation — flagged as Open Question in [[disambiguation_lag]].

## What was falsified

### Cross-group gradient cancellation

The earlier mathematical theory ([[disambiguation-mathematical-formalization]] Prop 2): SNR for `v_zk` is `O(1/√|B|)` because z is shared across groups. Empirically tested via z-sharing sweep `G ∈ [1, 1000]` (number of groups sharing each z-set). Predicted exponent on plateau duration: 1.0. Measured: **0.02**. The mechanism doesn't drive the lag.

### Kramers thermodynamic escape

If the plateau were a free-energy trap requiring noise to escape, higher effective temperature `T_eff = η/B` should speed transitions. Measured: τ **monotonically increases** with η. Opposite of Kramers prediction.

## What remains open

- Direct measurement of basin geometry (loss-landscape cross-sections, parameter-space distance to solution manifold)
- Multi-seed verification of the K^1.3 exponent
- Whether the geometric picture is Adam-specific
