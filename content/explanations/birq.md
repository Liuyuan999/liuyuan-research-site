# Let a speech model improve its own learning targets

BiRQ turns intermediate speech representations into pseudo-labels, while raw-input targets anchor the learner as those representations evolve.

## The decision

A self-supervised speech model learns by predicting pseudo-labels at masked frames. BEST-RQ obtains those labels from a fixed random projection of the unmasked audio features, avoiding an external pretrained label model.

## The bottleneck

Input-based labels are stable but do not use the representations the encoder is learning. Labels from intermediate features can be richer, yet their target distribution changes with the same encoder being optimized.

## The idea

Keep both branches. BiRQ builds enhanced targets from unmasked intermediate features and preserves raw-input anchor targets. A differentiable Gumbel-softmax target and a penalty formulation connect label construction to the same training loop.

## Source

[BiRQ: Bi-Level Self-Labeling Random Quantization for Self-Supervised Speech Recognition](https://arxiv.org/abs/2509.15430)
