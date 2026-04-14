---
title: "Optimization Arrow"
related_concepts: ["five_arrows_framework", "conditional_entropy_barrier", "excess_loss"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["optimization", "arrows_of_time"]
---

# Optimization Arrow

One of the [[five_arrows_framework]] — the thermodynamic asymmetry in learning efficiency. Low-entropy forward mappings are easier to optimize than high-entropy inverses, even with identical data exposure and architecture.

## Empirical signature

Quantified by [[excess_loss]] gap `Δ_dir = L_excess^{B→A} − L_excess^{A→B}`. Survey reports **~1.16 nats** for causal transformers at K=5 vs **~0.22 nats** for non-causal MLPs on identical data — the causal inductive bias sharpens the gap ~5×.

## Mechanism

- **Low-entropy direction**: sharp, stable gradient valleys; deterministic target collapses the likelihood surface
- **High-entropy direction**: flat, noisy valleys; gradients average across K plausible preimages

The [[causal_arrow]] (unidirectional mask) exacerbates this because each token's representation only gets signal from one direction of flow.

## Related findings

- Papadopoulos et al. (2024) interpret the gap as a computational-complexity difference: forward generation is like multiplication, inverse like prime factorization. Forward involves **state collapse**; inverse requires **state expansion**.
- Observed as the [[conditional_entropy_barrier]] or "Causal Tax" in synthetic [[wind_tunnel_methodology]] experiments.
