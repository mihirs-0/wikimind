---
title: "Three Scaling Laws of the Disambiguation Lag"
related_concepts: ["disambiguation_lag", "narrow_basin_geometry"]
source_refs: ["raw/disambiguation_lag_v4_circuit_discovery.md"]
last_updated: 2026-04-14
tags: ["scaling_laws", "training_dynamics", "empirical"]
---

# Three Scaling Laws of the Disambiguation Lag

Empirical power-law characterizations of the [[disambiguation_lag]], measured on a 4-layer 128-dim Transformer trained at constant `η = 10⁻³`, batch 128, on the canonical `(B, z) → A` task with `|B| = 1000` and `K ∈ {3, 5, 7, 10, 13, 17, 20, 25, 30, 36}`.

## Law 1 — Plateau duration vs ambiguity

```
τ ∝ K^1.3   (R² = 0.98, n = 10)
```

Plateau duration `τ` (from last step at 95% of log K to first step below 5%) grows superlinearly with K. The exponent 1.3 does not match any standard search complexity:

- Linear search: K^1
- Coupon collector: K log K ≈ K^1.1 over this range
- Quadratic interference: K^2

It's a specific, non-trivial measurement of how gradient-based circuit discovery scales with mapping multiplicity.

| K | log K | τ (steps) | ḡ²_plateau |
|---|---|---|---|
| 3 | 1.10 | 200 | 0.76 |
| 5 | 1.61 | 400 | 2.03 |
| 10 | 2.30 | 850 | 1.22 |
| 17 | 2.83 | 2700 | 0.54 |
| 25 | 3.22 | 4100 | 0.42 |
| 36 | 3.58 | 6350 | 0.31 |

## Law 2 — Plateau duration vs learning rate

```
τ ∝ η^+0.8   (R² = 0.95, n = 4; η = 5×10⁻³ never transitions)
```

Higher learning rate makes discovery **harder**, with complete failure above `η* ≈ 5×10⁻³`.

| η | τ (steps) | η·τ |
|---|---|---|
| 3×10⁻⁴ | 2100 | 0.63 |
| 5×10⁻⁴ | 2200 | 1.10 |
| 10⁻³ | 3400 | 3.40 |
| 2×10⁻³ | 7550 | 15.10 |
| 5×10⁻³ | — | — |

Total parameter displacement `η·τ` grows superlinearly (`∝ η^2.1`, R² = 0.999). Large steps don't fail to help — they force the optimizer onto a longer, more wasteful trajectory.

This **falsifies thermodynamic-escape (Kramers)** mechanisms, where higher effective temperature should accelerate barrier crossing. The dynamics are the opposite: precision helps, noise hurts.

## Law 3 — Gradient suppression during the plateau

```
ḡ²_plateau ∝ K^-0.6
```

Each training example produces a gradient toward one of K candidate directions. Within a batch, these K directions partially cancel, so the batch gradient norm shrinks with K — the search signal is weakest precisely when the search space is largest.

At the transition, the symmetry breaks, gradients align, and norm snaps to a **K-independent** value (~6.2 nat/step) — the optimizer's terminal velocity once gradient suppression releases.

## Connection between Law 1 and Law 3

If the plateau were a random walk with step size `∝ ḡ²_plateau` toward a fixed-distance target:

- `τ ∝ 1/ḡ² ∝ K^+0.6`

But measured `τ ∝ K^1.3`. The gap (1.3 − 0.6 = 0.7) suggests gradient suppression accounts for ~half the difficulty; the other half comes from the **target itself becoming geometrically narrower** at larger K. See [[narrow_basin_geometry]].

## Limitations

- **Single seed (42)** — needs multi-seed validation
- **K range** is narrow (3–36, less than one decade)
- **No theoretical derivation** of the 1.3 exponent
- **Adam-specific?** Vanilla SGD comparison not run
