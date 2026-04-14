---
title: "Disambiguation Lag"
related_concepts: ["reversal_curse", "directional_asymmetry", "marginal_conditional_phases", "phase_transition_symmetry_breaking", "narrow_basin_geometry", "dissipation_scaling", "z_shuffle_diagnostic", "three_scaling_laws", "binding_problem"]
source_refs: ["raw/disambig_paper.md", "raw/disambiguation_lag_v4_circuit_discovery.md", "raw/disambiguation_thermo.md", "raw/firstprinciples_disamb.md", "raw/mathdisamb.md"]
last_updated: 2026-04-14
tags: ["disambiguation_lag", "training_dynamics", "phase_transition"]
---

# Disambiguation Lag

A prolonged training plateau followed by a sharp phase transition that arises whenever an autoregressive model must use a contextual selector `z` to choose among `K` candidate outputs sharing the same input prefix. The model sits at loss `log K` for thousands of steps with full information available, then abruptly snaps into correct disambiguation.

## The task

Surjective `f: A → B` with `|B| = N/K` and exactly K preimages per `b ∈ B`. A selector token `z_k` identifies which preimage. Model receives `[BOS, B, SEP, z, SEP]` and predicts `A = a^(k)_b`. Information structure:

- `H(A | B) = log K`
- `H(A | B, z) = 0`
- `I(A; z | B) = log K` nats — z carries exactly the disambiguation information

This isolates conditional binding from all other factors and makes K the single difficulty dial.

## The phenomenon

For K ≥ 7-10 (below this, no plateau), training proceeds in two sharply separated phases — the [[marginal_conditional_phases]]:

1. **Marginal phase** (~500 steps): model learns the prior `P(A|B) = Uniform(K)`. Candidate loss → log K. z-shuffle gap = 0.
2. **Plateau** (hundreds to thousands of steps, scaling with K): no measurable change. The model has all information needed; gradient is non-zero per example; yet learning is blocked.
3. **Conditional phase**: sharp sigmoidal transition (see [[phase_transition_symmetry_breaking]]). Candidate loss drops from log K to ~0; z-shuffle gap jumps to ~log K. Gradient norm spikes by an order of magnitude.

Plateau duration scales **superlinearly** with K (`τ ∝ K^1.3`) — see [[three_scaling_laws]].

## Why the plateau is sustained — evolution of the explanation

This is one of the more interesting **theory revisions** in the cluster.

### Earlier theory (`raw/disambig_paper.md`, `raw/mathdisamb.md`, `raw/firstprinciples_disamb.md`, ~Feb 2026)

**Cross-group gradient cancellation.** Because `z_k` is shared across all |B| groups but routes to different targets in each, the expected gradient for `v_zk` averaged across groups has magnitude `O(1/√|B|)` while variance stays O(1). SNR is `O(1/√|B|)` — the signal is drowned in across-group variance.

This was formalized as **Proposition 2** in [[disambiguation-mathematical-formalization]] under an isotropy assumption on the unembedding vectors across groups.

### Later theory (`raw/disambiguation_lag_v4_circuit_discovery.md`, [[circuit-discovery-latency]])

**Cross-group cancellation falsified by ablation.** A z-sharing sweep from G=1 (each z used in only 1 group) to G=1000 (z fully shared across all groups) produced **no measurable change** in plateau duration: β = 0.02, predicted by Prop 2 to be β = 1.0. The cancellation mechanism that *would* matter under Prop 2 doesn't actually drive the lag.

What does matter: **within-batch within-group** competition between K candidate directions, plus the **geometric narrowness** of the disambiguation circuit in parameter space. See [[narrow_basin_geometry]].

### What survives from the earlier theory

- The two-phase decomposition and the saddle-escape interpretation
- The Score-Probability-Utility framing of attention dynamics
- The capacity-failure result for linear models (Proposition 1 — additive `W_b e_b + W_z e_z` cannot encode multiplicative B×z interaction)
- The dissipation scaling `Q ∝ log K`
- The K* ≈ 7 phase boundary

## Connection to the [[reversal_curse]]

The disambiguation lag provides an **optimization-level explanation** for the curse. The backward direction `B → A` inverts a many-to-one mapping with fan-in K. By the K^1.3 scaling, backward needs ~K^1.3 more steps to discover the disambiguation circuit. At realistic K≈20 (e.g., biographical descriptions matching multiple entities), backward needs ~60× the forward training budget.

Above critical learning rate (`η* ≈ 5×10⁻³` for the 4-layer 128-dim setup), the basin is **never entered** — extending training does not help.

This complements (does not replace) the existing factorization-curse account: factorization explains why the gradient signal is one-directional; disambiguation lag explains how hard the backward direction is even when the signal exists.

## Open Questions

- **Multi-seed validation**: all current results use seed 42. The exponents (1.3, +0.8, -0.6) and regime boundaries need replication.
- **Multi-layer scaling**: deeper models should have shorter plateaus (the coordination barrier is distributed across layers). Untested.
- **Transfer to natural language**: real text has correlated candidates, partial disambiguation, non-uniform priors. Whether the K^1.3 law holds for "effective K" in language is open.
- **Why exactly 1.3?** No theoretical derivation. The decomposition `1.3 ≈ 0.6 (gradient suppression) + 0.7 (basin narrowing)` is suggestive but not rigorous.
- **Adam-specific?** Adam's adaptive moments may interact with the basin-width interpretation. SGD comparison untested.
