---
title: "Geometric Origin of the Disambiguation Lag (paper)"
source: raw/disambig_paper.md
source_refs: ["raw/disambig_paper.md"]
ingested_at: 2026-04-14
tags: ["disambiguation_lag", "phase_transition", "dissipation_scaling"]
---

# Geometric Origin of the Disambiguation Lag

Earlier (Feb 21, 2026) formulation of the [[disambiguation_lag]] phenomenon. Proposes the **gradient cancellation theory** — later partially revised by [[circuit-discovery-latency]] (v4).

## Framework

Surjective task `f: A → B` with `|B| = N/K`. Each `b ∈ B` has K preimages indexed by selector `z`. The model sees `[B, z]` and predicts A. Information structure: `H(A|B) = log K`, `H(A|B,z) = 0`. So z carries exactly `log K` nats.

## Two-phase dynamics

1. **Marginal phase**: model learns the prior `P(A|B)`, candidate loss → log K within ~500 steps. z-shuffle gap = 0 (z is being ignored).
2. **Conditional phase**: after a long plateau, sharp sigmoidal transition to using z. Loss → 0; z-shuffle gap → log K simultaneously.

Plateau duration grows monotonically with K: ~950 steps at K=5, ~12,500 at K=20, >30,000 at K=36.

## Mechanistic probes

- **Attention to z** rises sharply at the transition, particularly in upper layers
- **Logit lens**: P(correct) rises first in deepest layers, propagates backward; embedding layer never exceeds chance — disambiguation is computed progressively through depth
- **z-shuffle diagnostic**: `Δz = L_z_shuffled − L_clean` jumps from 0 to ~10–17 nats during transition

## Theoretical claim (proposed mechanism)

Gradient cancellation: at the plateau, the expected gradient for `v_zk` is averaged over `|B|` independent random embedding directions (one per group). Magnitude shrinks as `O(1/√|B|)` while variance stays O(1). SNR drops to `O(1/√|B|)`. Escape requires symmetry-breaking phase transition; dissipation `Q ∝ log K`.

## Status

This is the **earlier theoretical framing**. The v4 paper ([[circuit-discovery-latency]]) **falsifies** the gradient-cancellation theory via a z-sharing ablation. The surviving picture is [[narrow_basin_geometry]]. See [[disambiguation_lag]] for the reconciled story.
