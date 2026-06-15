# Final Audit

Paper: 109 non_smooth_mechanics_for_foundation_policies

Decision: STRONG_REVISE

The v4 rebuild adds a local contact-mode benchmark with paired seeds, strong local baselines, ablations, stress sweeps, failure cases, LaTeX tables, and figures. The proposed contact-mode boundary atlas beats the strongest non-oracle baseline, `complementarity_residual_planner`, by `0.076 +/- 0.007` paired success under combined stress and improves contact-mode F1 from `0.495` to `0.630`.

Safety gates pass: unsafe impulse, jam rate, slip overshoot, and intervention cost are all lower than the strongest non-oracle baseline.

Remaining blocker: the evidence is local. The paper should not be submitted to ICLR main without real robot or independent high-fidelity validation and external trained baselines.
