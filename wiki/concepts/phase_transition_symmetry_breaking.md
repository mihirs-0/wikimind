---
title: "Phase Transition and Spontaneous Symmetry Breaking (Disambiguation)"
related_concepts: ["disambiguation_lag", "narrow_basin_geometry", "marginal_conditional_phases"]
source_refs: ["raw/disambig_paper.md", "raw/firstprinciples_disamb.md", "raw/mathdisamb.md"]
last_updated: 2026-04-14
tags: ["phase_transition", "symmetry_breaking", "training_dynamics"]
---

# Phase Transition and Spontaneous Symmetry Breaking

The mechanism of escape from the [[disambiguation_lag]] plateau. The transition is **sharp**, **coordinated across multiple parameter matrices**, and structurally identical to a discrete symmetry-breaking event in physical phase transitions.

## The instability mechanism

At the plateau, the model is in an unstable equilibrium. A stochastic perturbation that makes `v_zk` slightly informative for some B-group triggers a positive feedback loop:

```
v_z slightly informative
   → A_z > 0 (advantage of attending to z becomes positive)
   → p_z ↑ (attention score for z increases via gradient ∝ p_z A_z)
   → more v_z weight in context vector c
   → u_z ↑ (utility of z grows)
   → A_z ↑ (advantage grows further)
   → loop self-reinforcing
```

The plateau is an **unstable fixed point** of this dynamics: perturbations that increase z-utility are amplified; perturbations that decrease it are suppressed.

## Required coordination across parameter matrices

The feedback loop above appears to need only `v_z` and attention weights. In fact, the transition requires **simultaneous** coordinated updates to three parameter groups:

1. `W_V` (value matrices) — so different `z_k` produce distinguishable context-vector perturbations
2. `W_Q, W_K` (query-key matrices) — so attention routes sufficient mass to z
3. `W_U` (unembedding) — so the new context-vector perturbations decode as the correct candidates

No single update in isolation produces a descent signal:

- Adjusting `W_V` without `W_U` → undecodable perturbations
- Adjusting `W_U` without `W_V` → nothing to decode
- Increasing `p_z` without informative `v_z` → amplifies noise, not signal

This is the **coordination barrier** that sustains the plateau. See [[narrow_basin_geometry]] for the parameter-space geometry of the target.

## Why the transition is sharp

Once the optimizer enters the basin, the positive feedback creates rapid descent. The utility gap between "using z" (log K nats of improvement) and "ignoring z" (zero improvement) is **larger** at higher K, so the feedback is stronger once triggered. This explains why the conditional-phase loss curve is sigmoidal with sharpness increasing in K.

The gradient norm spikes during the transition — the optimizer is traversing a steep region of the loss landscape (the "cliff" after the saddle). Total cumulative gradient work scales with information erased: see [[dissipation_scaling]].

## Discrete symmetry breaking

At the plateau, the model treats all K candidates within each group symmetrically — predictive distribution is K-fold symmetric uniform. The transition breaks this by **committing to a specific assignment** `z_k → a^(k)_b` for each group.

This is computationally analogous to a physical phase transition from a disordered (high-symmetry) phase to an ordered (low-symmetry) phase. The analogy:

| Physical | Computational |
|---|---|
| Disordered phase | Plateau (K-fold symmetric prediction) |
| Critical point | Transition |
| Ordered phase | Disambiguated state |
| Latent heat | Cumulative gradient dissipation Q |

## Note on the falsified Kramers picture

The natural physical analogy would be **Kramers escape**: the plateau is a free-energy trap, and stochastic noise drives escape over a barrier. Higher temperature should accelerate the transition.

This is **falsified** by the learning-rate sweep (Law 2 of [[three_scaling_laws]]): higher η makes the plateau **longer**, with complete failure above `η* ≈ 5×10⁻³`. The dynamics are the opposite of Kramers: precision helps, noise hurts. The narrow-basin geometry picture replaces the thermodynamic-trap picture as the operative explanation.

The symmetry-breaking framing **survives**: it's the structural pattern of the transition (discrete commitment among K equivalent candidates), independent of why the plateau is sustained.
