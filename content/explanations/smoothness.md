# A sharper curvature bound can change an algorithm’s pace

Penalty methods can look increasingly stiff as the penalty grows. Follow the optimized lower-level response, and the reduced objective can have a different curvature scale.

## The decision

Penalty methods make a lower-level optimality gap expensive. A generic joint smoothness bound grows with the penalty, suggesting smaller gradient steps as the approximation is tightened.

## The bottleneck

The outer algorithm follows a reduced objective after lower-level optimization. Bounding arbitrary joint directions can miss cancellation between the perturbed and original value functions. Constraints also invalidate the unconstrained shortcut that the inner gradient is zero.

## The idea

Analyze their second-order directional derivatives together. For a fixed feasible set, the response direction is orthogonal to the lower gradient; for coupled constraints, multipliers account for the moving boundary. The resulting smoothness bound changes the outer iteration analysis.

## Source

[Improved Analysis of Penalty-Based Methods for Bilevel Optimization with Coupled Constraints](https://eurasip.org/Proceedings/Eusipco/Eusipco2025/pdfs/0001183.pdf)
