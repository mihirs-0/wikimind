---
title: "LoRA Bottleneck and Adaptation-Driven Collapse"
related_concepts: ["directional_asymmetry", "pretraining_prior", "reversal_curse"]
source_refs: ["raw/arrow_of_learning-7.md", "raw/paper-draft-direction.md"]
last_updated: 2026-04-14
tags: ["lora", "qlora", "peft", "fine_tuning"]
---

# LoRA Bottleneck and Adaptation-Driven Collapse

Low-Rank Adaptation (LoRA / QLoRA) freezes the pretrained backbone and trains only a low-rank additive update `ΔW = BA` with `rank(ΔW) ≪ min(d_in, d_out)`. This makes PEFT economical (≈1–3% trainable parameters), but it also creates a **hard adaptation bottleneck** that interacts badly with the [[pretraining_prior]] — especially on high-entropy inverse tasks.

## The observed failure mode

On [[wind_tunnel_methodology]] experiments, LoRA with `r=32, α=64` on GPT-2 (2.5% trainable):

| Task | Val loss trajectory |
|---|---|
| A→B (low-entropy) | 4.62 → 2.28 (matches full fine-tuning) |
| B→A (high-entropy) | 4.88 → 5.30 (worsens) |

The reverse loss **degrades** over training while the forward loss converges smoothly. At 7B scale under 4-bit QLoRA (Qwen-2.5, Mistral, Llama-2-7B), the collapse is even sharper and persists across model family.

## Mechanism: frozen prior + low-rank update

The pretrained base has settled into a compression-biased world-model. LoRA's update has two simultaneous constraints:

1. **Frozen base** — `W_0` cannot move. Whatever directional prior it encodes is permanent.
2. **Low-rank correction** — `ΔW` has at most `r` independent rows. It can carve *variations* of the existing representation but cannot construct a fundamentally different one.

For prior-compatible tasks (forward mapping, like A→B in the wind-tunnel), the adapter's few degrees of freedom suffice to specialize the existing representation. Performance matches full fine-tuning.

For prior-incompatible tasks (inverse, B→A), the adapter would need to **override** the base's forward-compression bias. This requires updates outside the low-rank subspace it's restricted to. The training loss continues to decrease on the in-distribution component but validation loss worsens, because the adapter is essentially fighting the base without enough degrees of freedom to win.

## "Double compression" viewpoint

`raw/paper-draft-direction.md` frames the failure as ×2 compression:

1. Pretrained base = compressed world-model biased toward low-entropy conditionals
2. LoRA = compressed adaptation channel

Compression compounds; decompression tasks (one → many) are doubly penalized. This predicts the observed collapse naturally.

## Related: ROME and targeted low-rank edits

Rank-one edits (Meng et al. 2022, ROME) show the **power** of low-rank interventions for implanting specific factual associations. The reverse result here shows the **limit**: distributed directional properties of the base cannot be flipped by low-rank updates, even in aggregate.

## Practical implications

- **If your downstream task requires invertibility, symmetric generalization, or high-entropy inverse learning, do not use LoRA/QLoRA.** Either fine-tune the full model or use a high-rank adapter (ideally rank approaching `min(d_in, d_out)`).
- **Evaluate directionally.** Standard next-token loss will not surface this failure; you need explicit forward/inverse evaluation under controlled entropy (the [[wind_tunnel_methodology]] protocol).
- **Instruction tuning and alignment under PEFT inherit the base's directional biases.** This has implications for RLHF, safety training, and domain adaptation.

## Mitigations suggested but not tested in this cluster

- Higher-rank adapters (r → min(d))
- Joint forward/inverse curricula
- Cycle-consistency regularization (force `A → B → A`)
- Entropy-aware loss reweighting

## Open Questions

- What is the minimum rank `r*` at which the B→A collapse disappears? Unmeasured.
- Is the collapse specific to LoRA's low-rank form, or does it appear for any small-parameter adapter (e.g., prefix-tuning, adapters)? Not ablated.
