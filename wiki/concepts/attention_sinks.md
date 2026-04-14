---
title: "Attention Sinks"
related_concepts: ["trace_arrow", "five_arrows_framework"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["attention", "interpretability", "mechanistic"]
---

# Attention Sinks

The phenomenon where transformers allocate disproportionate attention probability to the first token of a sequence, regardless of that token's semantic content. The main instance of the [[trace_arrow]].

## Mechanism

Softmax self-attention requires `∑_i α_i = 1`. Each head must distribute its attention somewhere. If no previous token is semantically relevant to the current position, the excess probability mass must still land somewhere — the first token (often `<bos>` or a dedicated sink token) becomes the "dump" for this unused capacity.

This is not a learned optimization but a **structural consequence of softmax normalization**.

## "Catch, Tag, Release"

A proposed functional interpretation:

- **Catch** — sink tokens absorb excess attention-head capacity per layer
- **Tag** — they serve as a stable positional anchor, providing implicit reference
- **Release** — the absorbed capacity doesn't corrupt downstream semantic vectors because the sink's value contribution is near-zero

## Effects

**First-token bias**: the computational graph of a trained transformer is closer to a star topology than a uniform lattice. Early tokens can broadcast cheaply; late tokens compete for bandwidth.

**Over-squashing**: semantically important recent tokens get diluted by the always-on connectivity to the sink.

**Lyapunov stabilization**: likely keep the hidden-state dynamical system within a non-chaotic regime. Strip out sinks and long-context coherence degrades.

## Practical implications

- **StreamingLLM** and similar inference-efficiency methods preserve the first K tokens as the attention sink while evicting the middle of the context — exploiting the fact that the sink is load-bearing.
- Explicit sink tokens can be trained in, removing the first-token dependence and freeing the model to use position 0 semantically.
