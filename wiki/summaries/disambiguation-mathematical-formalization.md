---
title: "The Disambiguation Lag — Mathematical Formalization"
source: raw/mathdisamb.md
source_refs: ["raw/mathdisamb.md"]
ingested_at: 2026-04-14
tags: ["disambiguation_lag", "proofs", "formal", "gradient_cancellation"]
---

# The Disambiguation Lag — Gradient Geometry of Conditional Binding

Formal mathematical write-up of the [[disambiguation_lag]] phenomenon (68 KB, longest of the cluster). Contains explicit propositions and proofs that the other documents either summarize informally or omit.

## Formal contributions

### Proposition 1 — Linear capacity failure

`y = W_B e_B + W_z e_z` cannot disambiguate for K > 1; optimal additive solution is the group-mean predictor with loss log K. Proof: `W_z e_zk` is B-independent, so it can only shift all groups' logits identically and cannot resolve within-group ambiguity.

### Proposition 2 — Gradient cancellation theorem

Under isotropy of `{W_U^T e_a^(k)_b}` across groups, the expected gradient for `v_zk` averaged over all B-groups has magnitude `O(1/√|B|)` while variance stays O(1). Therefore SNR for updating `v_zk` is `O(1/√|B|)`.

**Important nuance** documented in Remark 1: the isotropy assumption refers to **across-group** isotropy (different B-groups point to unrelated candidate sets), which is preserved even after the marginal phase has organized **within-group** structure.

**Status**: Proposition 2's empirical consequence is **falsified** by the v4 paper ([[circuit-discovery-latency]]) via z-sharing ablation. The mathematical proposition is correct under its assumptions, but the predicted dependence of plateau duration on `|B|` doesn't appear in experiments (β = 0.02 vs predicted 1.0). The within-batch within-group gradient interference is what actually matters.

### Z-gap measurement window

Defined to **avoid tautological dependence on K**: `t_start` = first step with `Δz > 0.5`; `t_end` = first step with `Δz > 0.9 × max(Δz)`. Absolute thresholds, not K-dependent. This is what justifies interpreting `Q ∝ log K` as a non-trivial scaling rather than a definitional artifact.

### Empirical scaling

5 matched experiments (K = 10, 15, 20, 25, 36):

| K | log K | Q_zgap | ΔL_zgap | Q/ΔL | Q − ΔL |
|---|---|---|---|---|---|
| 10 | 2.30 | 52.5 | 1.38 | 38× | 51.1 |
| 15 | 2.71 | 81.9 | 0.55 | 149× | 81.4 |
| 20 | 3.00 | 99.9 | 0.30 | 333× | 99.6 |
| 25 | 3.22 | 171.8 | 0.17 | 1010× | 171.6 |
| 36 | 3.58 | 196.8 | 0.11 | 1848× | 196.7 |

Fit: `Q = c · log(K/K*)` with `c ≈ 120`, `K* ≈ 7`. Excess `Q − ΔL` scales with log K at R² = 0.922 — the loss-tracking component is removed but the scaling persists.

## Universality claims

Two-phase dynamics observed in Transformer, Gated MLP, LSTM. Absent in linear models (capacity failure). Non-monotonic noise sensitivity characteristic of metastable saddles.
