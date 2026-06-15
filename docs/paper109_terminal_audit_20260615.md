# Paper 109 Terminal Audit

Date: 2026-06-15

Paper: `109_non_smooth_mechanics_for_foundation_policies`

Terminal decision: STRONG_REVISE

ICLR main ready: no

## What Passed

- Plan-first execution document created before rerun.
- `src/run_experiment.py` compiles.
- Full experiment rerun completed.
- CSV row-count gate passed for primary metrics, task/regime seed metrics, split seed metrics, paired stats, ablations, stress sweep, and failure cases.
- Numeric sanity found zero NaN/Inf issues.
- Strongest non-oracle baseline is `complementarity_residual_planner`.
- Proposed method beats the strongest baseline by `0.076 +/- 0.007` paired success and wins `7/7` seeds.
- Contact-mode F1 improves from `0.495` to `0.630`.
- Boundary error drops from `0.294` to `0.246`.
- Unsafe impulse, jam rate, slip overshoot, and intervention cost are all lower than the strongest baseline.
- Full method remains above the best removed-component ablation by `0.027` success.
- Stress sweep at level `1.0` keeps proposed above diffusion, conformal, and complementarity baselines.
- Eight failure cases are documented.
- PDF rebuild passed and produced `C:/Users/wangz/Downloads/109.pdf`.
- PDF SHA256: `18B2B2A99CF5BD68DFADC6A4E087493841D3BDFA55520701DCA3A36F5DCC3C0D`.
- No `C:/Users/wangz/Desktop/109.pdf` copy exists.

## What Still Blocks Submission

- No real robot evidence.
- No independent high-fidelity simulator validation.
- No external trained diffusion/transformer policy checkpoints.
- No hardware videos or deployment logs.
- Oracle remains higher than proposed, indicating unresolved contact-mode headroom.

## Honest Outcome

This paper should continue as `STRONG_REVISE`, not be submitted to ICLR main. The next version needs external validation before the central claim can be treated as submission-ready evidence.
