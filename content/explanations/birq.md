# Let a speech model improve its own learning targets

BiRQ turns intermediate speech representations into pseudo-labels, while raw-input targets anchor the learner as those representations evolve.

## The decision

A self-supervised speech model learns by predicting pseudo-labels at masked frames. BEST-RQ obtains those labels from a fixed random projection of the unmasked audio features, avoiding an external pretrained label model.

## The bottleneck

Raw-input labels stay fixed as the encoder learns. Intermediate-feature labels evolve with the same encoder that predicts them. Training must coordinate the changing targets with a stable reference task.

## The idea

Keep both branches. BiRQ builds enhanced targets from unmasked intermediate features and preserves raw-input anchor targets. A differentiable Gumbel-softmax target and a penalty formulation connect label construction to the same training loop.

## Source

[BiRQ: Bi-Level Self-Labeling Random Quantization for Self-Supervised Speech Recognition](https://arxiv.org/abs/2509.15430)
