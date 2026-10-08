# When bilevel learning can skip a nested solve

PBGD-Free removes the value-function loop from a penalty method. The reason this can work is upper-level flatness—not simply using fewer updates.

## The decision

In the paper’s LLM application, x contains LoRA parameters in the backbone and y is the output head. The head learns supervised fine-tuning (SFT); the backbone is guided by direct preference optimization (DPO) through that adapted head.

## The bottleneck

A full penalty gradient estimates both the original SFT-optimal head and a perturbed head. Dropping the value-function correction saves one response estimate, but the removed term is multiplied by the penalty and can remain important.

## The idea

Make the reason for omission explicit: upper-level flatness bounds how the DPO objective varies around an SFT-optimal head. Under that condition and the other regularity assumptions, one lower update and one outer update yield controlled stationarity error.

## Source

[Beyond Value Functions: Single-Loop Bilevel Optimization under Flatness Conditions](https://arxiv.org/abs/2507.20400)
