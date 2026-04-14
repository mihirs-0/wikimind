---
title: "Neural Thermodynamics (Effective Free Energy)"
related_concepts: ["dissipation_scaling", "disambiguation_lag", "narrow_basin_geometry"]
source_refs: ["raw/disambiguation_thermo.md"]
last_updated: 2026-04-14
tags: ["thermodynamics", "external_framework", "sgd"]
---

# Neural Thermodynamics

A framework due to Liu Ziyin and collaborators (Ziyin, Xu, Chuang — NeurIPS 2025, *Neural Thermodynamics: Entropic Forces in Deep and Universal Representation Learning*). Cited as the theoretical context for the [[dissipation_scaling]] result.

## Core claim

Stochastic gradient descent with learning rate `η` does **not** minimize the loss `L(θ)`. It minimizes an **effective free energy**:

```
F(θ) = L(θ) + (η/4) · Tr(Var[∇L])
```

The second term is **entropic**: it penalizes states with large per-sample gradient variance. The coefficient `η/4` plays the role of temperature — it scales the entropic contribution relative to the loss.

## Implications

- SGD has a thermodynamic interpretation: minimization of free energy under an effective temperature
- States with high per-sample gradient variance are pushed away from, even if they have low loss
- States with low loss but high gradient variance can be **less** stable than slightly higher-loss states with low variance
- The "effective optimum" found by SGD differs from the loss minimum, with the gap controlled by `η/B_batch`

## Application to the [[disambiguation_lag]]

The plateau may be a local minimum of F but **not** of L:

- At the symmetric state (uniform over K candidates), per-sample gradients point in K different directions and partially cancel
- The **mean** gradient (relevant to L) is small
- The **variance** (relevant to F) is large
- Perturbations that begin to break the symmetry first **increase** `‖∇‖²` before eventually decreasing it
- The symmetric state is therefore stabilized by the entropic term — it's an entropic trap, not a loss-landscape trap

This was the original interpretive framework for `Q ∝ log K`: the dissipation is the cost of crossing the entropic barrier, where information `log K` is being "erased" from the predictive distribution.

## Status of the interpretation

The empirical scaling `Q ∝ log K` is robust. The thermodynamic **interpretation** is partially validated and partially open:

- **Falsified** by the learning-rate sweep ([[three_scaling_laws]] Law 2): if the plateau were purely a free-energy trap, higher η (higher effective T) should accelerate escape. Instead it slows it. The narrow-basin-geometry picture ([[narrow_basin_geometry]]) is now the operative mechanistic explanation for plateau duration.
- **Survives** as the framework for understanding why excess dissipation `Q − ΔL` is so large (38× to 1848× the loss change) — the gradient work is consumed by the entropic dynamics of stochastic barrier crossing, not by descent.

The cleanest theoretical gap, per `raw/disambiguation_thermo.md`: derive **why** the cumulative entropic contribution should scale linearly with the information content of the barrier from first principles in this framework, rather than just observing the scaling empirically.

## Personal communication context

Mihir reached out to Ziyin directly about the disambiguation work. Ziyin suggested two control experiments: (1) two-layer linear network on the same task, (2) label-noise sweep at `K=20`. Both ablations were run; results discussed in [[disambiguation-mathematical-formalization]] and [[circuit-discovery-latency]].
