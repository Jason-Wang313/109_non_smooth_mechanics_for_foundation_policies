# Submission Attack Log

## Attack: This is just complementarity residual planning.

Response: The complementarity residual planner is the strongest baseline. Proposed improves success by `0.076 +/- 0.007`, mode F1 by `0.135`, unsafe impulse by `0.015`, jam by `0.021`, slip by `0.019`, and intervention cost by `0.047`.

## Attack: Diffusion or transformer policies might learn this at scale.

Response: Correct. The paper uses local surrogates and must not claim dominance over trained RT or diffusion systems. It claims that explicit contact-mode auditing is locally useful and should be tested in those systems.

## Attack: The benchmark is synthetic.

Response: Correct. This is why the decision is `STRONG_REVISE`, not ready acceptance.

## Attack: The method may over-probe.

Response: Intervention cost is lower than the strongest non-oracle baseline in the local benchmark. A no-probe ablation is the best removed component but still trails full by `0.027` success.
