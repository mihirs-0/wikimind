---
title: "Arrows of Time for LLMs (ICML 2024 slides, Papadopoulos et al.)"
source: raw/arrowsoftimeppt.md
source_refs: ["raw/arrowsoftimeppt.md"]
ingested_at: 2026-04-14
tags: ["arrows_of_time", "external_reference", "cross_entropy", "forward_backward"]
---

# Arrows of Time for LLMs — Papadopoulos, Wenger, Hongler (ICML 2024)

Slide deck for the paper that **seeded** Sahasrabudhe's research program. PDF extraction is noisy (many figures and decorative images lost) but the mathematical core is legible.

## Core setup

Given a text sequence `x₁...xₙ`:
- **Forward model** estimates `p→(xₖ | x₁...xₖ₋₁)` — standard next-token prediction
- **Backward model** estimates `p←(xₖ | xₙ...xₖ₊₁)` — previous-token prediction

Both factor the joint `P(x₁...xₙ)` via cross-entropy, so in theory `ℓ→_CE = ℓ←_CE`.

## Key metric

`∂↔_CE = (E[ℓ←_CE] − E[ℓ→_CE]) / (E[ℓ←_CE] + E[ℓ→_CE])`

- `∂↔_CE > 0`: forward is easier (the observed direction in natural language)
- `∂↔_CE < 0`: backward is easier (never observed)

## Empirical claim

Across languages, model scales, and training durations, **natural language is consistently harder to predict backward than forward**. Forward perplexities are systematically lower. Given Shannon-1951 symmetry for stationary sources, this gap must come from finite model capacity interacting with the algorithmic complexity of backward generation — "state expansion" vs "state collapse".

## Role in the cluster

This is the **external reference** that motivates Sahasrabudhe's contribution: Papadopoulos studies the arrow of time **in natural text**; Sahasrabudhe removes language entirely via synthetic [[wind_tunnel_methodology]] to isolate whether the arrow is intrinsic to transformers or inherited from data.
