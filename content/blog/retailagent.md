# Audit a trading agent’s timing, not just its exposure

A policy can hold a stock frequently and still choose comparatively unfavorable moments. An exposure-matched metric helps isolate that timing.

## Exposure and timing answer different questions

Suppose an agent is long during half of the intervals in a trading day. Its return depends on what the stock did and on which half it chose. Comparing it with a policy that holds the stock at half exposure throughout the same day separates a timing component from the average amount invested.

## Decide first, observe the next return afterward

RetailAgent gives the LLM an anonymized intraday history and condition-specific state. The agent then chooses long or flat before the next interval return is revealed. Concealing stock identity and other information keeps the decision boundary controlled and makes the tested policy easier to interpret.

## Subtract average exposure

The timing score sums each following return multiplied by the action minus that stock-day’s mean action. A negative score means exposure was allocated to relatively unfavorable intervals on that path. The score is a diagnostic of alignment, rather than a complete accounting of an executable strategy’s profitability.

## Shuffle the schedule to test the alignment

A shuffle preserves an action count while disrupting when the actions occur. In the principal text condition, the intact schedule has substantially more negative timing than the reported shuffle controls. The study also examines memory and persistence using matched panels. These controls help characterize the sequence rather than explaining the result through exposure alone.

## Keep the conclusion at the level tested

The paper documents negative timing across tested configurations and recoverable structure in action traces. It does not resolve how another participant would exploit that structure in a live market with costs and feedback. The contribution is a controlled behavioral audit and a way to study the timing of sequential decisions.

## Source

[RetailAgent: Structured Adverse Timing in Self-Conditioned Multimodal LLM Trading Agents](https://arxiv.org/abs/2608.28399)
