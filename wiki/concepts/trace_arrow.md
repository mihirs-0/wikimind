---
title: "Trace Arrow"
related_concepts: ["five_arrows_framework", "attention_sinks"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["dynamics", "arrows_of_time", "interpretability"]
---

# Trace Arrow

The dynamical / mechanistic-fossil axis of the [[five_arrows_framework]]. Structural artifacts that accumulate during processing and stabilize the system's temporal evolution.

## Canonical example: [[attention_sinks]]

Transformers disproportionately attend to the very first token of a sequence (often `<s>` or `<bos>`), even when that token carries no semantic content.

- **Mechanism**: softmax normalization `∑ α_i = 1`. If no previous token is semantically relevant, the attention probability mass still has to go *somewhere* — the first token becomes the sink that absorbs excess attention.
- **Trace**: regardless of sequence length, the model maintains a strong attentional link to `t=0`. The beginning is permanently "traced" into every downstream computation.
- **Functional role** ("catch, tag, release"): sinks stabilize attention-head capacity, tag sequences with positional reference, and release unused capacity without corrupting semantic vectors.

## First-token bias and graph geometry

Viewed as a message-passing graph, the transformer is **star-like** rather than uniform: early tokens are central hubs. This creates **over-squashing** — recent, semantically relevant tokens compete for attention bandwidth that the sink tokens have already consumed.

## Lyapunov stability

The sequence of hidden states `h_1, h_2, ...` is a trajectory in high-dimensional phase space. **Lyapunov exponents** measure how fast nearby trajectories separate; positive exponents → chaos.

Attention sinks likely act as stabilizers, keeping the maximum Lyapunov exponent in a regime where coherent long-context generation is possible. Remove the sink and long-context generation degrades into hallucination or gibberish as `t → ∞`.

Local Lyapunov spectra identify specific tokens as **bifurcation points** — moments where trace-past most strongly constrains or destabilizes the future.

## Comparison: SSMs don't have this arrow

State-space models (Mamba) use fixed-size recurrence without softmax over history. They don't exhibit the attention-sink trace phenomenon — but may be more fragile to the [[optimization_arrow]] on long-range look-back because gradients must propagate through many recurrent steps.
