---
title: "Directionality & Conditional Complexity — training logs + source (part 2)"
source: raw/directionality-conditional-complexity_-a1-a2-1-part-2.md
source_refs: ["raw/directionality-conditional-complexity_-a1-a2-1-part-2.md"]
ingested_at: 2026-04-14
tags: ["training_logs", "reproducibility", "source_code", "synthetic_benchmark"]
---

# A1/A2 Experiments — Training Logs + Source Code

Continuation of [[directionality-conditional-complexity-main]]. Contains (i) raw training stdout for K=8 and K=5 runs and (ii) the complete `gpt2.py` script implementing the [[wind_tunnel_methodology]].

## Key training numbers

### K=8 (larger gap, from-scratch)

```
K=8  A→B  final loss 1.31
K=8  B→A  final loss 3.81   → gap = 2.50 nats  (ln 8 ≈ 2.08)
```

### K=5 small & medium (from-scratch, symmetric convergence)

Across seeds 0 and 1, both `size=small` and `size=medium` configurations, A→B and B→A reached **identical** val loss:

```
K=5  small  seed 0/1  final val loss  0.0007  both directions
K=5  medium seed 0/1  final val loss  0.0001  both directions
```

This is the evidence supporting [[learning-has-an-arrow]]'s "no from-scratch gap" claim — with enough compute at moderate K, the gap vanishes.

## Reproducibility-relevant config (from source)

```python
VOCAB_SIZE = 128          # 3..127 content tokens; 0,1,2 special
STR_LEN = 8
MAX_SEQ_LEN = 1 + STR_LEN + 1 + STR_LEN  # [BOS] X [SEP] Y
TRAIN_FRAC = 0.8; VAL_FRAC = 0.1; TEST_FRAC = 0.1

@dataclass
class GPTConfig:
    d_model=512, n_layer=8, n_head=8, d_ff=2048, max_seq_len=MAX_SEQ_LEN, dropout=0.1
```

Cluster-aware split for K>1: per-cluster `(K-2)` train / 1 val / 1 test for K≥3; for K=2, 1 train / 1 test. Ensures every cluster appears in all splits without exact-pair leakage.

## Status

Pure log + code dump. Cite this for reproducibility; the conceptual story lives in [[directionality-conditional-complexity-main]] and [[learning-has-an-arrow]].
