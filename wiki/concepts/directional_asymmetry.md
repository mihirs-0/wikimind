---
title: "Directional Asymmetry in Transformers"
related_concepts: ["reversal_curse", "conditional_entropy_barrier", "wind_tunnel_methodology", "five_arrows_framework", "lora_bottleneck", "pretraining_prior", "reversal_invariance"]
source_refs: ["raw/arrow_of_learning-7.md", "raw/paper-draft-direction.md", "raw/arrows-of-time-in-learning-systems.md", "raw/directionality-conditional-complexity_-a1-a2-1.md"]
last_updated: 2026-04-14
tags: ["directional_asymmetry", "reversal_curse", "transformers"]
---

# Directional Asymmetry in Transformers

The umbrella phenomenon: autoregressive transformers learn forward mappings `A → B` reliably but systematically fail on the inverse `B → A`, even when both are theoretically realizable with the same architecture, data, and compute.

## Why it's a paradox

Training is driven by cross-entropy loss. Papadopoulos et al. (2024) proved a [[reversal_invariance]] theorem: under suitable tokenization and positional-encoding conditions, NLL is symmetric between a corpus `D` and its exact reversal `T(D)`. The objective function has no preferred direction.

Yet the systems built from this symmetric objective are deeply irreversible — the [[reversal_curse]], forward/backward perplexity gaps in natural text, and training-dynamics asymmetries on synthetic data all point the same way.

## The three-factor decomposition (Sahasrabudhe)

1. **Architecture** — possibly a **modest** [[conditional_entropy_barrier]]; the magnitude is contested across the cluster's own documents (see Open Questions below).
2. **[[pretraining_prior]]** — language pretraining installs a strong compression bias that persists even on language-free synthetic tasks. This is the main driver of the observed gaps.
3. **[[lora_bottleneck]]** — parameter-efficient fine-tuning freezes the pretrained backbone and constrains updates to a low-rank subspace. Prior-compatible (A→B) tasks are absorbed easily; prior-incompatible (B→A) tasks cannot override the frozen prior and collapse.

## Empirical profile (pretrained GPT-2, K=8)

| Regime | A→B val loss | B→A val loss | Gap |
|---|---|---|---|
| From-scratch | ≈ B→A (symmetric) | — | ≈ 0 (for medium+ models) |
| Full fine-tune | 4.24 → 2.21 | 5.15 → 5.13 | ~3 nats |
| LoRA r=32 | 4.62 → 2.28 | 4.88 → 5.30 (worsens) | 3+ nats, growing |
| QLoRA Qwen-2.5-3B | 2.97 | 4.67 | **1.70** |
| QLoRA Llama-2-7B (K=5) | 2.39 | 3.81 | 1.42 |

Gap grows roughly monotonically with `ln K`.

## Why it matters

Tasks requiring invertibility — diagnosing causes from effects, inverting a hash, symbolic manipulation, bidirectional fact lookup — are systematically harder for pretrained LLMs under PEFT. Practical implication: if inverse reasoning is required, **use full fine-tuning or high-rank adapters**; LoRA/QLoRA are insufficient.

## Relationship to the [[five_arrows_framework]]

Directional asymmetry is the composite surface phenomenon; the five arrows (Optimization, Causal, Epistemic, Mutability, Trace) are distinct mechanisms that jointly produce it.

## Open Questions

- **Is the from-scratch gap real?** `paper-draft-direction` reports a 2.1 vs 4.9 nat gap at K=5 from-scratch; `directionality-conditional-complexity_-a1-a2-1` reports ~0.4 nats at K=5; `arrow_of_learning-7` claims zero. Part-2 training logs show exact convergence at K=5 for `size=medium` from-scratch. The gap may be a function of training budget: short runs show a gap, long runs close it. See the Open Questions section of [[conditional_entropy_barrier]] for the reconciliation attempt.
- **Does the gap interact with tokenizer or positional encoding choice?** Character-level tokenization vs BPE has not been directly ablated within this cluster.
- **Mechanistic locus unknown.** No paper in this cluster attributes the gap to specific layers, attention heads, or representational subspaces.
