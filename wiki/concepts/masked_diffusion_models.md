---
title: "Masked Diffusion Models"
related_concepts: ["reversal_curse", "causal_arrow", "directional_asymmetry"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["architecture", "diffusion", "masked_lm"]
---

# Masked Diffusion Models (MDMs)

A generative modeling paradigm in which the objective is to reconstruct masked tokens from surrounding context — interpolating between masked-language-modeling (BERT-style) and discrete diffusion. Noted as one of the few architectural classes that **natively escapes** the [[reversal_curse]].

## Why they escape the [[causal_arrow]]

Training an MDM requires reconstructing tokens from **any** context — past, future, or mixed. The gradient for a masked token flows **bidirectionally** from all available neighbors.

This implicitly couples `P(A | B)` and `P(B | A)`: since both directions arise from the same masked-reconstruction loss, the attention patterns learned for the forward context and the reverse context are **positively correlated**. This is qualitatively different from autoregressive training, where `P(B | A)` is trained extensively and `P(A | B)` is never trained at all.

## Empirical result

Recent work finds that MDMs trained on the same reversal-curse fine-tuning data that trips up autoregressive LLMs **successfully** infer reverse relations they were never directly trained on. The reversal curse appears to be a pathology specific to the **autoregressive paradigm**, not transformers per se.

## Tradeoffs

- MDMs lack the clean left-to-right generative semantics of autoregressive models. Sampling is iterative (multiple denoising steps) rather than single-pass.
- Inference cost is typically higher due to multiple mask-reconstruction steps.
- Training dynamics are less well-understood than AR pretraining.

## Relationship to [[directional_asymmetry]]

MDMs provide a proof of concept that **architecture matters**: the directional failures of LLMs are not inevitable consequences of "being a transformer". They are specific to autoregressive causal-masked pretraining. Replace the training regime and the failures can disappear.
