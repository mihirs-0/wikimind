---
title: "Mutability Arrow"
related_concepts: ["five_arrows_framework", "pretraining_prior", "lora_bottleneck"]
source_refs: ["raw/arrows-of-time-in-learning-systems.md"]
last_updated: 2026-04-14
tags: ["training_dynamics", "arrows_of_time", "plasticity"]
---

# Mutability Arrow

The evolutionary / plasticity axis of the [[five_arrows_framework]]. Tracks how representations transition from plastic (mutable) to rigid (immutable) across two "times": training time and layer depth.

## Plasticity Tax

Pretrained weights are **rigid** — they sit in a deep local minimum optimized for language. Adapting them to arbitrary new distributions (e.g., synthetic random-string mappings) costs more than training a random-init model on the same task.

This is the **Plasticity Tax**: pretrained models are less mutable than randomly-initialized models for orthogonal tasks, even though they start from a "better" loss. The gradient from the new task has to fight against the prior's energy landscape.

## Flow of Ranks

Within a single forward pass, representation rank **inflates** from shallow to deep layers. The nonlinear operations (attention + MLP) tend to increase the rank of the representation matrices.

- Early layers: low-rank, compressible representations
- Deep layers: high-rank, resistant to compression

Design implication: efficient fine-tuning should allocate more adapter capacity to deep layers, acknowledging their mutability requirements scale with representation complexity. This informs rank-schedule strategies for PEFT.

## Mode collapse under Reverse KL

In RLHF, minimizing `D_KL(Q || P)` is **mode-seeking**: it penalizes probability mass where the target is zero. This sharpens the Mutability Arrow by forcing the model to converge on a single-mode "safe" distribution, stripping the model of exploratory diversity.

Forward KL `D_KL(P || Q)` is mass-covering and does not collapse modes. RLHF's widespread use of reverse KL may therefore be a hidden driver of mode collapse and reduced plasticity in aligned models.

## Interaction with [[pretraining_prior]]

The prior is the *content* that rigidifies; the Mutability Arrow is the *rigidification process*. The [[lora_bottleneck]] is the empirical demonstration: low-rank updates lack the degrees of freedom to mutate pretrained representations enough to learn prior-incompatible tasks.
