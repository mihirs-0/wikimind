---
title: "Epistemic Arrow"
related_concepts: ["five_arrows_framework", "kv_cache", "attention_sinks"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["information", "memory", "arrows_of_time"]
---

# Epistemic Arrow

The informational axis of the [[five_arrows_framework]]: the asymmetry between how a transformer represents the past (accessible, concrete) vs the future (probabilistic, unobserved).

## Past = addressable memory

The past is instantiated as the **[[kv_cache]]** — a stored record of the key and value projections for every previously-seen token. Every new generation step has O(1) attention access to the full history. This is a physical "memory system" in the theoretical-physics sense: the present state contains information about the external world at prior times.

Empirically, Attention Knockout and Attention Flow studies show factual information is routed from specific KV-cache positions to the current token at specific layers.

## Future = logit distribution

The future exists **only** as a probability distribution over the vocabulary. No state vector for `x_{t+k}` exists yet; only a prediction of it.

- **Fisher Information** accumulates as sequence progresses — parameter-estimate variance shrinks, certainty increases. This defines an arrow of increasing informational constraint.
- **Information Bottleneck**: as data flows through layers (vertical Epistemic Arrow), shallow layers retain high-fidelity past information while deep layers aggressively compress toward task-relevant abstraction.

## Input reconstruction asymmetry

- **Forward**: trivial to train a probe to reconstruct input token `x_t` from hidden state `h_{t+k}` (causal mask ensured `h_{t+k}` attended to `x_t`).
- **Backward**: theoretically impossible beyond chance to reconstruct `x_{t+k}` from `h_t` — `h_t` contains no information about the future input, only a prediction of it.

This is the sharpest empirical fingerprint of the Epistemic Arrow.

## Layer-wise forgetting

Paradoxically, the *immediate* past becomes harder to reconstruct at very deep layers. Logit-lens probing shows early layers retain syntax and literal form; later layers specialize in next-token semantics and forget literal surface form in favor of meaning.
