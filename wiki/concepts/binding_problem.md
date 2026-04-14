---
title: "Binding Problem"
related_concepts: ["disambiguation_lag", "marginal_conditional_phases", "reversal_curse"]
source_refs: ["raw/disambiguation_lag_v4_circuit_discovery.md", "raw/mathdisamb.md"]
last_updated: 2026-04-14
tags: ["cognitive_science", "compositionality", "external_reference"]
---

# Binding Problem

A foundational question in cognitive science (Treisman 1996, *Current Opinion in Neurobiology*): how do distributed representations compose features into coherent objects? Cited as the conceptual ancestor of the [[disambiguation_lag]] phenomenon.

## Cognitive-science formulation

A perceiver represents a scene as a list of features (red, square, left, big). The binding problem asks: how does the system know that **this** red is bound to **this** square (rather than to the left, or to the big)? Without binding, the representation is a feature bag, not a relational graph.

## Computational analogue

The disambiguation task `(B, z) → A` is a controlled instance of the binding problem in autoregressive Transformers:

- The model has access to the features (B and z are both visible from step 0)
- It easily learns the **marginal** statistics — which features tend to co-occur
- It struggles to learn the **binding** — which specific B is bound to which specific z to determine A

The [[marginal_conditional_phases]] decomposition mirrors this distinction directly:

- Marginal subproblem = feature-list learning (which entities exist for each B)
- Conditional subproblem = binding (which feature combinations cohere into the correct answer)

## Why the binding subproblem is structurally hard

Binding requires **multiplicative interaction**: the answer is `lookup[B][z_k]`, which cannot be decomposed as `g(B) + h(z)`. A purely additive mechanism (linear model, single attention layer treated naively) cannot represent this — see Proposition 1 in [[disambiguation-mathematical-formalization]].

In Transformers, multiplicative interaction must be *discovered* through the joint configuration of attention routing and value-space encoding. The [[narrow_basin_geometry]] picture explains why this discovery is geometrically hard.

## Implication for natural-language phenomena

The binding problem in modern LLMs shows up as:

- **Variable binding failures** — the same pronoun referring to different antecedents
- **Compositional generalization gaps** — failure to combine known features in novel ways
- **The [[reversal_curse]]** — failing to bind "B is A" given "A is B"

The disambiguation lag suggests these are not separate quirks but instances of the same underlying difficulty: gradient-based optimization is structurally bad at discovering multiplicative interactions in narrow basins of parameter space.
