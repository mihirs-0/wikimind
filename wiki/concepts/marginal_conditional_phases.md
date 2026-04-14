---
title: "Marginal vs Conditional Learning Phases"
related_concepts: ["disambiguation_lag", "phase_transition_symmetry_breaking", "z_shuffle_diagnostic"]
source_refs: ["raw/disambig_paper.md", "raw/disambiguation_lag_v4_circuit_discovery.md", "raw/firstprinciples_disamb.md", "raw/mathdisamb.md"]
last_updated: 2026-04-14
tags: ["training_dynamics", "two_phase_learning"]
---

# Marginal vs Conditional Learning Phases

The two-phase decomposition of training dynamics on conditional binding tasks. The same model, on the same data, with the same loss, must solve two qualitatively different subproblems — and it solves them in serial, not in parallel.

## The two subproblems (formalized)

**Definition** (Marginal subproblem). Learn the group prior `P(A | B)`: for each `b`, assign probability `1/K` to each element of `f^(-1)(b)` and zero elsewhere. Achieves loss `log K`.

**Definition** (Conditional subproblem). Learn the disambiguation `P(A | B, z)`: for each `(b, z_k)`, concentrate all probability on `a^(k)_b`. Reduces loss from `log K` to 0.

## Why they're qualitatively different

### Marginal: additive

Learning `P(A | B)` is a property of individual tokens. Each B is associated with a fixed candidate set. Encodable directly in the embedding and unembedding matrices without any cross-position interaction.

### Conditional: multiplicative

Learning `P(A | B, z)` requires composing information from two positions. The same `z_k` selects different answers for different B-groups — the answer is `lookup[B][z_k]`, a function not decomposable as `g(B) + h(z)`.

This is why **linear models permanently stall**: an additive model `y = W_b e_b + W_z e_z` cannot represent B-dependent z-contributions and cannot escape the marginal-phase optimum at `log K`. See Proposition 1 in [[disambiguation-mathematical-formalization]].

## Empirical signature

Across [[disambiguation_lag]] experiments:

- Marginal phase completes in ~500 steps for any K
- Plateau duration grows with K: ~200 (K=3) → ~6,350 (K=36) at η=10⁻³, B=128
- Both phases happen even when the architecture **could** in principle interleave them — the model demonstrably solves the marginal first, then the conditional, with the [[z_shuffle_diagnostic]] confirming z is being ignored throughout the marginal phase

## Connection to the [[binding_problem]]

The marginal subproblem is feature-list learning ("which entities exist"). The conditional subproblem is binding ("which features cohere"). The lag between them is the computational cost of going from a list to a graph.

## Connection to grokking

Grokking (Power et al. 2022) shows the same qualitative signature: prolonged plateau followed by sudden generalization. The disambiguation lag is arguably grokking's **task structural** counterpart — instead of generalizing from memorization to a closed-form algorithm, the model is generalizing from marginal memorization to relational binding.
