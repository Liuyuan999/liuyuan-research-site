# When bilevel learning can skip a nested solve

PBGD-Free uses upper-level flatness to bound the bias from removing the value-function loop, yielding a single-loop penalty method.

## The decision

In the paper’s LLM application, x contains LoRA parameters in the backbone and y is the output head. The head learns supervised fine-tuning (SFT); the backbone is guided by direct preference optimization (DPO) through that adapted head.

## The bottleneck

A full penalty gradient estimates both the original SFT-optimal head and a perturbed head. Dropping the value-function correction saves one response estimate, but the removed term is multiplied by the penalty and can remain important.

## The idea

Upper-level flatness bounds how the DPO objective varies around an SFT-optimal head. Together with the lower-level regularity conditions, it controls the stationarity error of one lower update followed by one outer update.

## Source

[Beyond Value Functions: Single-Loop Bilevel Optimization under Flatness Conditions](https://arxiv.org/abs/2507.20400)
