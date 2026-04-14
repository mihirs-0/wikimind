---
title: "KV Cache"
related_concepts: ["epistemic_arrow", "five_arrows_framework", "attention_sinks"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["inference", "memory", "attention"]
---

# KV Cache

The physical instantiation of a transformer's "past" during autoregressive inference. Stores the key and value projections for every previously-processed token, allowing O(1) attention access to arbitrary history positions.

## Role in the [[epistemic_arrow]]

The [[epistemic_arrow]] characterizes the past as **addressable memory** and the future as **logit distribution**. The KV cache is the memory side of that asymmetry:

- **Size**: O(T × L × d_head × n_heads × 2) — linear in sequence length `T`, independent of which positions get attended to
- **Access**: every new generation step performs attention over the full cache in a single operation
- **Content**: the precomputed `K_i`, `V_i` projections for each prior token, per layer

## Why it matters mechanistically

Attention Knockout studies rely on the KV cache as the *addressable* structure — they can ablate specific cached positions to trace how factual information flows from a past token to the current prediction. Without the cache, this kind of mechanistic intervention would not be feasible.

Also interacts with [[attention_sinks]]: the first few cache entries accumulate disproportionate attention and serve as stabilizers for long-context generation. StreamingLLM-style methods preserve the first K cache entries while evicting the middle.

## Comparison with SSMs

State-space models (Mamba) use a **fixed-size** recurrent state of dimension `d_state`, not a growing cache. Tradeoffs:

- SSMs: O(1) memory, but limited by state capacity — struggle to copy long strings because early tokens get overwritten
- Transformers: O(T) memory, perfect recall, but inference cost scales linearly with context length

The KV cache is the structural reason transformers excel at copying and long-range reference tasks — and the structural cost of a strong [[epistemic_arrow]].
