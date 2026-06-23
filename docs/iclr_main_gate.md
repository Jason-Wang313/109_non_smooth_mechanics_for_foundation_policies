# ICLR Main Gate

Paper: 109 non_smooth_mechanics_for_foundation_policies

Previous v3 decision: KILL_ARCHIVE

Gate verdict after v5 expanded audit: STRONG_REVISE

Evidence digest: local contact-mode boundary audit benchmark, 8 tasks, 10 non-smooth regimes, 8 splits, 16 methods, 10 paired seeds, 102400 main cells, 48000 stress cells, 51200 fixed-risk cells, 8000 ablation cells, and 24 failure cases.

Gate outcomes:
- Success gate: PASS; hard success margin over strongest non-oracle baseline is `0.097`.
- Utility gate support: hard utility margin is `0.137`.
- Diagnostic gate: PASS; contact-mode F1 delta is `+0.076`, boundary-error delta is `-0.041`.
- Safety gate: PASS; unsafe impulse, jam, slip, latency, energy, calibration, and cost do not regress against the strongest non-oracle baseline.
- Pairwise gate: PASS; 10/10 utility seed wins against the strongest non-oracle baseline.
- Ablation gate: PASS; full method beats the best removed component by `0.020` success and `0.046` utility.
- Stress gate: PASS; maximum-stress utility margin is `0.140`.
- Fixed-risk gate: PASS; strict fixed-risk coverage is `0.932` and strict utility margin is `0.167`.
- Scope gate: FAIL; no real robot or independent high-fidelity validation.

ICLR main ready: NO. The correct terminal decision is STRONG_REVISE.
