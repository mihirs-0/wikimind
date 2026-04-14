---
title: "Dissipation Scaling (Q ∝ log K)"
related_concepts: ["disambiguation_lag", "neural_thermodynamics", "phase_transition_symmetry_breaking"]
source_refs: ["raw/disambiguation_thermo.md", "raw/disambig_paper.md", "raw/mathdisamb.md", "raw/firstprinciples_disamb.md"]
last_updated: 2026-04-14
tags: ["thermodynamics", "landauer", "training_dynamics"]
---

# Dissipation Scaling: Q ∝ log K

The cumulative gradient dissipation `Q` during the [[disambiguation_lag]] phase transition scales linearly with the information-theoretic content of the disambiguation, log K. Empirically `R² = 0.92` across 5 matched experiments. The vast majority of `Q` is **excess** — gradient work that does not appear as loss descent.

## Definition

Cumulative gradient dissipation over a window `[t₁, t₂]`:

```
Q = η · Σ_{t ∈ [t₁, t₂]} ‖∇L_t‖²
```

In **continuous-time** gradient flow `θ̇ = -∇L`, the identity `ΔL = ∫ ‖∇L‖² dt` holds: all gradient work appears as loss descent. In **discrete SGD**, this identity breaks. The actual loss decrease ΔL is much less than Q. The excess `Q_excess = Q − ΔL` represents irreversible stochastic work consumed by barrier crossing rather than by loss descent.

## The z-gap measurement window

To avoid tautological dependence on K, the integration window is defined by **absolute thresholds** on the [[z_shuffle_diagnostic]] gap `Δz = L_z_shuffled − L_clean`:

- `t_start` = first step where `Δz > 0.5`
- `t_end` = first step where `Δz > 0.9 × max(Δz)`

These are fixed numbers that don't depend on K, log K, or any task parameter. A K-dependent window (e.g., "from 0.9 log K to 0.1 log K of candidate loss") would make `Q ∝ log K` hold by construction.

## Empirical result

Five matched experiments (only K varies; all other hyperparameters held fixed):

| K | log K | Q | ΔL | Q/ΔL | Q − ΔL |
|---|---|---|---|---|---|
| 10 | 2.30 | 52.5 | 1.38 | 38× | 51.1 |
| 15 | 2.71 | 81.9 | 0.55 | 149× | 81.4 |
| 20 | 3.00 | 99.9 | 0.30 | 333× | 99.6 |
| 25 | 3.22 | 171.8 | 0.17 | 1010× | 171.6 |
| 36 | 3.58 | 196.8 | 0.11 | 1848× | 196.7 |

Fit:

```
Q = c · log(K / K*)
c ≈ 120  (Landauer-like constant)
K* ≈ 7   (phase boundary — below this, no plateau phenomenology)
```

The excess `Q − ΔL` (loss-tracking component removed) **still** scales with log K at R² = 0.922.

## Interpretation: the Landauer analogy

Landauer (1961): erasing one bit at temperature T dissipates at least `k_B T ln 2` of heat. The disambiguation transition erases exactly `log K` nats of uncertainty per example (the predictive distribution shifts from `Uniform(K)` to a point mass on the correct candidate). If SGD dissipation is the cost of implementing this belief update through stochastic optimization, `Q ∝ log K` is the Landauer-analog scaling.

The Landauer constant `c ≈ 120` is the gradient dissipation per nat of information erased — a measurable property of the optimization protocol that depends on:

- Effective temperature `η / B_batch`
- Model dimension `d`
- Number of B-groups

## Carefully not claimed

- **Not** that SGD obeys Landauer's bound in the physical sense — the claim is only that the **mathematical structure** "dissipation proportional to information erased" emerges empirically
- **Not** that this explains the full [[reversal_curse]] (which exists at K=1 where the disambiguation phenomenology doesn't apply)
- Single seed; synthetic task only

## Theoretical context: [[neural_thermodynamics]]

The interpretation builds on Liu Ziyin's effective free energy framework: SGD doesn't minimize `L(θ)` but rather

```
F = L + (η/4) · Tr(Var[∇L])
```

The second term penalizes states with high per-sample gradient variance. At the plateau, mean gradient is small but variance is large; perturbations that begin to favor one candidate increase `‖∇‖²` before eventually decreasing it. The plateau is stabilized by the entropic term — it's a local minimum of `F`, not of `L`.

## Open theoretical gap

Connect the empirical scaling to a formal derivation from the effective-free-energy framework — show **why** the cumulative entropic contribution should scale with information content, rather than just observing that it does.
