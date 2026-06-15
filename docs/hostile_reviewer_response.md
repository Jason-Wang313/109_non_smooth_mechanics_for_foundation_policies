# Hostile Reviewer Response

Paper: 109 Non-Smooth Mechanics for Foundation Policies

## Strongest Technical Threats

- Classical non-smooth contact dynamics already handles unilateral contact, impact, and friction.
- Complementarity residual methods may explain most of the gain.
- Diffusion and transformer robot policies might learn contact regimes implicitly if trained at scale.
- The benchmark is local and not a real robot or accepted high-fidelity validation suite.

## Response

The v4 rebuild narrows the claim. The paper does not claim to invent non-smooth mechanics. It tests whether a contact-mode boundary atlas helps policy selection under non-smooth contact shifts.

The strongest non-oracle baseline is a complementarity residual planner. The proposed method improves combined-stress success by `0.076 +/- 0.007`, contact-mode F1 by `0.135`, unsafe impulse by `0.015`, jam rate by `0.021`, slip overshoot by `0.019`, and intervention cost by `0.047`.

## Honest Action

Mark as `STRONG_REVISE`, not ready acceptance. The evidence supports continued development, but ICLR-main submission requires real robot or independent high-fidelity experiments and external learned baselines.
