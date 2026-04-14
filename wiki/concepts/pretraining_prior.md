---
title: "Pretraining Prior (Compression Bias)"
related_concepts: ["directional_asymmetry", "lora_bottleneck", "mutability_arrow", "reversal_curse"]
source_refs: ["raw/arrow_of_learning-7.md", "raw/paper-draft-direction.md", "raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["pretraining", "inductive_bias", "compression"]
---

# Pretraining Prior (Compression Bias)

The strong directional inductive bias that large-scale language pretraining installs into a transformer's weights. Evidence from the Sahasrabudhe cluster shows this prior:

1. **Persists outside language.** On purely synthetic, semantic-free random-string mappings, pretrained GPT-2 still prefers low-entropy forward mappings over high-entropy inverses.
2. **Is the dominant source of [[directional_asymmetry]].** From-scratch models (with adequate budget) show near-symmetric learning; pretrained models show large asymmetries on the same data.
3. **Is difficult to override.** Under [[lora_bottleneck]], the prior is effectively permanent — low-rank adaptation cannot escape it.

## What the prior actually encodes

Language is asymmetrically structured:

- Forward relations — subject→verb, cause→effect, premise→conclusion — are **compressible**
- Inverse relations are **high-entropy and rarely required**
- Linguistic redundancy supports forward prediction but not inversion

GPT-style pretraining minimizes forward NLL on text. The model therefore learns a compressed representation of the forward statistical structure of natural language — and this compression scheme generalizes even to non-linguistic tasks, where it manifests as preferring deterministic many→one mappings over one→many inverses.

## Evidence: the pretrained-vs-scratch gap

On the [[wind_tunnel_methodology]] at K=8:

| Regime | A→B val loss | B→A val loss | Gap |
|---|---|---|---|
| Random init (from scratch), adequate budget | converges symmetrically | — | ~0 |
| Pretrained GPT-2 full fine-tune | 4.24 → 2.21 | 5.15 → 5.13 | ~3 nats |

The gap appears **only after pretraining is introduced**, with every other experimental variable held constant. This is the cluster's core experimental result.

## Theoretical framings

### Minimum Description Length / Solomonoff induction

Classical result: factoring `P(X, Y)` as `P(X) P(Y|X)` vs `P(Y) P(X|Y)` yields different code lengths. The [[pretraining_prior]] is the model's learned factorization — in language, the factorization that compresses forward mappings best is the one that pretraining discovers and locks in.

### Algorithmic Markov Condition (Janzing & Schölkopf 2010)

The causal direction is the one with a shorter, more independent mechanism; the anticausal direction requires additional fine-tuning to correct. The pretraining prior embodies this for natural language.

### Catastrophic inheritance (Chang et al. 2024)

Fine-tuning often **inherits and amplifies** pretrained biases rather than overwriting them. The LoRA experiments in this cluster are a controlled demonstration of catastrophic inheritance in action.

## Interaction with the [[mutability_arrow]]

The pretraining prior is the *content* that becomes rigid via the Mutability Arrow. The Plasticity Tax measures how much training budget is needed to escape the prior; LoRA's adaptation bottleneck measures whether escape is possible *at all* within the low-rank subspace.

## Open Questions

- Does the prior strength scale with pretraining compute, data, or model size? Unmeasured in this cluster.
- What pretraining objectives produce weaker directional priors? Masked-LM variants, bidirectional or cycle-consistency objectives, and [[masked_diffusion_models]] are plausible candidates but not systematically studied here.
- Can the prior be selectively "unlearned" for specific tasks without hurting general forward capability? Open.
