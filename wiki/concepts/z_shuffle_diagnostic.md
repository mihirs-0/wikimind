---
title: "Z-Shuffle Diagnostic"
related_concepts: ["disambiguation_lag", "marginal_conditional_phases", "dissipation_scaling"]
source_refs: ["raw/disambig_paper.md", "raw/disambiguation_lag_v4_circuit_discovery.md", "raw/mathdisamb.md"]
last_updated: 2026-04-14
tags: ["methodology", "diagnostic", "measurement"]
---

# Z-Shuffle Diagnostic

A model-agnostic causal probe for measuring whether a model is **using** a contextual signal `z` for disambiguation, vs merely **seeing** it. Central instrument in the [[disambiguation_lag]] experiments.

## Definition

For each training/eval batch, compute candidate loss two ways:

- `L_clean` — loss with the true `(B, z, A)` triples
- `L_z_shuffled` — loss with `z` randomly permuted across the batch while holding `(B, A)` fixed

The **z-gap** is:

```
Δz ≡ L_z_shuffled − L_clean
```

## Interpretation

- `Δz ≈ 0` → predictions are independent of z. The model is ignoring it.
- `Δz > 0` → permuting z hurts performance, so z is being causally used.
- `Δz ≈ log K` → maximum: shuffling z drops performance from 0 to `log K` (the marginal-only ceiling).

## Why it works

The diagnostic is **causal**: it manipulates the input and measures the output change. Unlike attention-weight inspection, it doesn't require interpreting internal mechanisms. Unlike loss alone, it isolates the conditional-binding component from any change in the marginal predictor.

A model that has memorized the marginal `P(A | B)` but ignores z will have `L_clean ≈ L_z_shuffled ≈ log K`, so `Δz ≈ 0` even though the model has converged to a non-trivial loss.

## Use in defining the dissipation window

The [[dissipation_scaling]] integration window uses **absolute thresholds** on Δz:

- `t_start` — first step where `Δz > 0.5`
- `t_end` — first step where `Δz > 0.9 × max(Δz)`

These thresholds don't involve K, log K, or any task parameter — they're fixed numbers chosen to bracket the transition. This is what justifies interpreting `Q ∝ log K` as a non-trivial scaling rather than a definitional artifact.

## Empirical signature in the [[marginal_conditional_phases]]

Across all K, the z-gap pattern is identical:

- Marginal phase: `Δz = 0` consistently (model genuinely ignores z, doesn't just slowly use it)
- Plateau: `Δz = 0` (model continues to ignore z despite seeing it on every example)
- Conditional phase: `Δz` jumps from 0 to ~log K over a narrow step window — the same window in which attention-to-z and logit-lens probes also change

This sharp synchronicity across multiple measurement modalities is what justifies calling the transition a **phase transition** rather than a gradual signal accumulation.

## Generalizability

The z-shuffle is a special case of a broader family of **input-permutation diagnostics**. The same principle (permute one input position, measure performance delta) generalizes to any conditional-binding task and provides a clean causal handle on what information the model is using vs ignoring.
