# Final Audit

Paper: 109 non_smooth_mechanics_for_foundation_policies

Decision: STRONG_REVISE

The v4.1 continuation audit reran the local contact-mode benchmark with paired seeds, strong local baselines, ablations, stress sweeps, failure cases, LaTeX tables, and figures. The proposed contact-mode boundary atlas beats the strongest non-oracle baseline, `complementarity_residual_planner`, by `0.076 +/- 0.007` paired success under combined stress and improves contact-mode F1 from `0.495` to `0.630`.

Safety gates pass: unsafe impulse, jam rate, slip overshoot, and intervention cost are all lower than the strongest non-oracle baseline.

Coverage gates pass: 45 aggregate metric rows, 1575 per-task/regime rows, 11025 seed-task/regime rows, 315 seed-split rows, 8 pairwise rows, 7 ablation rows, 49 ablation-seed rows, 1715 ablation task/regime/seed rows, 30 stress-sweep rows, 7350 stress-sweep task/regime/seed rows, and 8 failure cases. Numeric sanity found zero NaN/Inf issues.

Remaining blocker: the evidence is local. The paper should not be submitted to ICLR main without real robot or independent high-fidelity validation and external trained baselines.
