---
title: "Arrows of Time in Learning Systems (survey)"
source: raw/arrows-of-time-in-learning-systems.md
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
ingested_at: 2026-04-14
tags: ["survey", "arrows_of_time", "directional_asymmetry", "interpretability"]
---

# Arrows of Time in Learning Systems — Comprehensive Survey

A literature synthesis positioning Sahasrabudhe's directional-asymmetry work against related phenomena. Proposes the unifying **[[five_arrows_framework]]**:

1. **[[optimization_arrow]]** — "Causal Tax": excess loss gap between forward and inverse mappings. Causal transformers show ~1.16 nats at K=5 vs ~0.22 nats for MLPs; the causal inductive bias, not the data, drives the gap.
2. **[[causal_arrow]]** — the [[reversal_curse]]: logical inability to invert A→B to B→A. Rooted in causal-mask gradient flow asymmetry.
3. **[[epistemic_arrow]]** — past as [[kv_cache]] (addressable, O(T) memory); future as logit distribution (probabilistic, unobserved).
4. **[[mutability_arrow]]** — "Plasticity Tax": pretrained weights become rigid; adaptation layers remain plastic. Also manifests as Flow-of-Ranks (rank inflation from shallow → deep layers).
5. **[[trace_arrow]]** — mechanistic fossils: [[attention_sinks]] act as temporal anchors stabilizing dynamics via Lyapunov-exponent regulation.

## Theoretical baseline

The **[[reversal_invariance]]** theorem (Papadopoulos et al. 2024): NLL is symmetric under corpus reversal given tokenization stability and appropriate positional encoding. Yet trained models are irreversible — the asymmetry must come from the **Data × Mask × Optimizer** interaction, not the objective.

## Grand synthesis

- **Data** breaks symmetry via entropy and order → Optimization + Causal Arrows
- **Architecture** (causal mask + softmax) → Epistemic + Trace Arrows
- **Training** (accumulation of rigid priors) → Mutability Arrow

## Comparative: Transformers vs State-Space Models

- Transformers: O(T) KV cache, parallel attention, strong softmax-induced trace (attention sinks), severe reversal curse
- SSMs (Mamba): O(1) fixed state, recurrent, no softmax sink, milder trace arrow but sharper optimization arrow from gradient propagation

## Mitigations discussed

Reverse training (data augmentation), bidirectional attention (BERT), [[masked_diffusion_models]] (natively escape the reversal curse because training reconstructs from any context), entropy-regularized objectives.
