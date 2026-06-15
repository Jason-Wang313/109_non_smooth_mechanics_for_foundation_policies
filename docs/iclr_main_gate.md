# ICLR Main Gate

Paper: 109 non_smooth_mechanics_for_foundation_policies

Previous v3 decision: KILL_ARCHIVE

Gate verdict after v4 rebuild: STRONG_REVISE

Evidence digest: local contact-mode benchmark, 5 tasks, 7 non-smooth regimes, 5 splits, 9 methods, 7 paired seeds, 84 episodes per group.

Gate outcomes:
- Success margin over strongest non-oracle baseline: PASS (`0.076`).
- Diagnostic improvement: PASS (`+0.135` contact-mode F1).
- Safety/cost non-regression: PASS.
- Pairwise seeds: PASS (7/7 wins).
- Ablation margin: PASS (`0.027`).

ICLR main ready: NO. Real robot or independent high-fidelity validation is still required.
