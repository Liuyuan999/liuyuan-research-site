# Audit a trading agent’s timing, not just its exposure

Holding a stock often and holding it at favorable moments are different behaviors. RetailAgent separates exposure from timing to audit sequential LLM decisions.

## The decision

At each interval, a frozen LLM sees an anonymized price history and chooses long or flat before the next return is revealed. The experiment can also show charts, account state, or the agent’s earlier self-authored memories.

## The bottleneck

A policy can benefit from a rising stock while being flat during its strongest intervals. Measuring average exposure and alignment with the next return separately reveals when the policy allocated its exposure.

## The idea

Subtract the return of constant exposure on the same stock-day. Audit the remaining timing term, shuffle saved actions to disrupt sequence alignment, and inspect how memory changes the policy’s persistence.

## Source

[RetailAgent: Structured Adverse Timing in Self-Conditioned Multimodal LLM Trading Agents](https://arxiv.org/abs/2608.28399)
