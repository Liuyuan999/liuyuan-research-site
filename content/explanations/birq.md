# Let a speech model improve its own learning targets

BiRQ turns intermediate speech representations into pseudo-labels, while raw-input targets anchor the learner as those representations evolve.

## A target without a transcript

Speech is continuous. A self-supervised learner can hide part of a recording and predict a discrete label for that part, but somebody still has to define those labels. A random quantizer creates them cheaply. A representation learned by another encoder can make them more informative, at the cost of maintaining that encoder and its training pipeline.

## Use representations already being learned

BiRQ takes intermediate representations from the speech model itself and discretizes them with a random-projection quantizer. This gives the model a route to richer targets without requiring a separate external label encoder. The labels and representations can improve within the same training process.

## An evolving target needs an anchor

When a learner also helps construct its targets, the target can move as the learner changes. BiRQ includes labels obtained directly from the raw input as an anchor. This stable source complements the enhanced labels produced from intermediate representations.

## Optimization connects the two roles

The paper formulates the interaction as a bilevel learning problem. Differentiable Gumbel-softmax selection supports end-to-end training of the label-selection mechanism. The exact losses and update rules are in the method section; the page’s diagram focuses on what each component contributes.

## Evaluate with speech recognition

The reported experiments use word error rate after downstream fine-tuning. In the 155M Conformer LibriSpeech comparison, BiRQ reports 5.0% test-clean and 12.6% test-other WER, compared with 6.8% and 19.6% for BEST-RQ. The AMI experiment reports improvements in its own setting. Those numbers describe the specified model, data, and decoding configurations.

## Source

[BiRQ: Bi-Level Self-Labeling Random Quantization for Self-Supervised Speech Recognition](https://arxiv.org/abs/2509.15430)
