---
title: "From Directional Asymmetry to Dissipation Scaling (research note)"
source: raw/disambiguation_thermo.md
source_refs: ["raw/disambiguation_thermo.md"]
ingested_at: 2026-04-14
tags: ["disambiguation_lag", "neural_thermodynamics", "narrative", "landauer"]
---

# From Directional Asymmetry to Dissipation Scaling

Personal research narrative tracing the evolution of Mihir's thinking from [[reversal_invariance]] to the [[dissipation_scaling]] result. Useful as a **research-trajectory document** linking the entire Sahasrabudhe research program.

## Trajectory

1. **Starting hypothesis**: reversal invariance — joint factorization should be direction-blind, so forward-trained and reverse-trained models should converge.
2. **Hypothesis broken** by Papadopoulos et al. (2024) "Arrow of Time in LLMs" — measured a real, persistent forward-vs-backward asymmetry.
3. **Sharpened** by Berglund et al. (2024) reversal curse — but the curse is about generalization at inference, while Papadopoulos was about learning dynamics.
4. **Decision**: build a synthetic benchmark stripping out language. Led to the disambiguation task `(B,z) → A`.
5. **First surprise**: not a gradual difference between directions — a qualitative discontinuity. Plateau at log K, then phase transition.
6. **Connection to neural thermodynamics**: Liu Ziyin's NeurIPS 2025 framework — SGD minimizes effective free energy `F = L + (η/4) Tr(Var[∇L])`, not just loss. Suggests the plateau is an entropic trap.
7. **Quantitative result**: `Q ∝ log K` with `R² = 0.92` (5 matched experiments). Excess dissipation `Q − ΔL` is 38× to 1848× the loss change — the [[dissipation_scaling]] is in the **irreversible excess**, not loss descent.
8. **Ablations from Ziyin**: linear-network plateau (capacity failure, never escapes); label-noise (low noise amplifies dissipation; high noise truncates transition).

## Carefully not claimed

- Not claiming SGD obeys Landauer's bound physically — only that the **mathematical structure** (dissipation ∝ information erased) appears empirically
- Not claiming to explain the full reversal curse (which exists at K=1; disambiguation phenomenology requires K≥7-10)
- Single seed, synthetic task. Multi-seed and natural-language extension are future work

## Open theoretical gap

Connect the empirical scaling to a formal derivation from Ziyin's effective free energy — show **why** the cumulative entropic contribution should scale with the information content of the barrier rather than just observing it.
