---
title: "The Disambiguation Lag Is Circuit Discovery Latency (v4)"
source: raw/disambiguation_lag_v4_circuit_discovery.md
source_refs: ["raw/disambiguation_lag_v4_circuit_discovery.md"]
ingested_at: 2026-04-14
tags: ["disambiguation_lag", "scaling_laws", "circuit_discovery", "negative_controls"]
---

# The Disambiguation Lag Is Circuit Discovery Latency

Mihir Sahasrabudhe, Feb 2026. The v4 manuscript that **revises** the earlier framing: the disambiguation lag is not gradient cancellation or thermodynamic barrier escape — it's **gradient-based circuit discovery in a narrow basin** of parameter space.

## Three scaling laws

1. `τ ∝ K^1.3` (R² = 0.98, n=10) — plateau duration vs ambiguity. Doesn't match linear, log, coupon-collector, or quadratic search complexities.
2. `τ ∝ η^+0.8` (R² = 0.95) — higher learning rate makes discovery **harder**, with complete failure above `η* ≈ 5×10⁻³`. Rules out noise-assisted (Kramers) escape.
3. `ḡ²_plateau ∝ K^-0.6` — batch gradient norm during plateau is suppressed by K-fold candidate-direction cancellation. Snaps to K-independent ~6.2 nat/step "terminal velocity" at the transition.

## Negative controls (key contributions)

- **Cross-group gradient cancellation** (the theory in the earlier papers): falsified. A z-sharing sweep from G=1 (fully shared) to G=1000 (fully private) shows no measurable change in plateau duration (β = 0.02, predicted 1.0). The cancellation that matters is **within-batch within-group**, not across groups.
- **Thermodynamic barrier escape (Kramers theory)**: falsified. Higher temperature should accelerate barrier crossing; instead τ increases monotonically with η.

## Surviving picture: [[narrow_basin_geometry]]

- The disambiguation circuit occupies a narrow basin in parameter space
- K-fold symmetry suppresses the within-batch gradient (~K^-0.6)
- Coarse learning-rate steps overshoot the basin entirely (the η^0.8 result)
- Search time is the hitting time of a random walk with suppressed step size to a narrow target → superlinear K^1.3 scaling

## Architecture comparison

`τ_Transformer > τ_LSTM > τ_GatedMLP`. Linear models never escape (Proposition 1 — additive `W_b e_b + W_z e_z` cannot encode multiplicative B×z interaction). The Gated MLP's pre-wired multiplicative interaction halves the discovery cost — direct evidence that the plateau is **circuit discovery latency**, not intrinsic task difficulty.

## Three-regime forgetting phase diagram

After convergence at K=20, reassign z→A for fraction `f` of groups:
- f ≤ 0.01: invisible (local circuit absorbs perturbation)
- 0.05 ≤ f ≤ 0.10: bounded damage (~1.1 nat floor on old mappings)
- f ≥ 0.50: catastrophic (full forgetting)

Crossover at `f* ≈ 0.1–0.25` marks the boundary between local patching and global rewriting.

## Implication for the [[reversal_curse]]

Backward direction (B→A) inverts a many-to-one mapping with fan-in K. Per the K^1.3 scaling, backward needs ~K^1.3 more steps than forward to discover the disambiguation circuit. At K≈20 (typical for biographical facts), that's ~60× more training. Above critical η, **never reachable**.
