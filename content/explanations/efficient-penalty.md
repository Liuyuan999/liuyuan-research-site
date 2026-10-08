# Separate the sources of cost in penalty-based bilevel learning

Reduced-curvature analysis permits larger outer steps. Flatness-based updates remove one response computation, with separate methods for fixed and coupled constraints.

## The decision

A bilevel learner chooses an outer variable while its inner variable solves another objective. A penalty makes inner suboptimality costly, but the chosen formulation and the update schedule determine which computation is actually required.

## The bottleneck

There are three distinct costs: a penalty-scaled step-size restriction, two lower-level response estimates, and the extra structure of constraints that move with the outer decision. Treating them as one difficulty obscures which improvement applies.

## The idea

Analyze the reduced objective to capture curvature cancellation, then alternate lower responses and outer updates. Upper-level flatness controls the bias from removing a value-function correction. The coupled extension incorporates constraint multipliers and boundary regularity.

## Source

[Efficient Penalty-Based Bilevel Methods: Improved Analysis, Novel Updates, and Flatness Condition](https://arxiv.org/abs/2511.16796)
