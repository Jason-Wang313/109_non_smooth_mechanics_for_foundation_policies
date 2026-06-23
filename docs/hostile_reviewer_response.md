# Hostile Reviewer Response

Paper: 109 Non-Smooth Mechanics for Foundation Policies

## Strongest Technical Threats

- Classical non-smooth contact dynamics already handles unilateral contact, impact, and friction.
- Complementarity residual or contact-implicit methods may explain most of the gain.
- Diffusion and transformer robot policies might learn contact regimes implicitly if trained at scale.
- The benchmark is local and not a real robot or accepted high-fidelity validation suite.
- The v5 method includes coupled arbitration, so ablations must not accidentally keep the full arbitration pathway.

## Response

The v5 rebuild narrows the claim. The paper does not claim to invent non-smooth mechanics, train a foundation model, or provide a hardware safety certificate. It tests whether a contact-mode boundary audit helps policy selection under non-smooth contact shifts.

The strongest non-oracle baseline is the v4 atlas, not a weak generic baseline. The v5 method improves held-out hard success by `0.097`, utility by `0.137`, contact-mode F1 by `0.076`, boundary error by `-0.041`, unsafe impulse by `-0.018`, and wins 10/10 paired utility seeds over that baseline. The ablation gate passes only after component removals disable the coupled arbitration path, which is the cleaner ablation semantics.

## Honest Action

Mark as `STRONG_REVISE`, not ready acceptance. The local evidence supports continued development, but ICLR-main submission requires real robot or independent high-fidelity experiments, trained external policy baselines, videos/logs, and calibrated contact-risk measurements.
