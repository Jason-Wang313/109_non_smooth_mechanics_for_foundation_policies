# Final Audit

Paper: 109 non_smooth_mechanics_for_foundation_policies

Decision: STRONG_REVISE

ICLR main ready: no

The v5 expanded audit reran Paper 109 with 8 tasks, 10 non-smooth regimes, 8 splits, 16 methods, 10 paired seeds, stress sweeps, fixed-risk budgets, full component ablations, failure cases, generated LaTeX tables, figures, a 26-page ICLR-style manuscript, bright boxed clickable citations, and a validator.

## Gate Evidence

- Success gate: passed.
- Diagnostic gate: passed.
- Safety gate: passed.
- Pairwise gate: passed.
- Ablation gate: passed.
- Stress gate: passed.
- Fixed-risk gate: passed.
- Scope gate: failed by design due to missing external robotics validation.

## Key Metrics

- Hard success: `0.689` proposed vs `0.592` strongest non-oracle baseline.
- Hard utility: `0.767` proposed vs `0.631` strongest non-oracle baseline.
- Pairwise utility wins vs strongest non-oracle baseline: 10/10.
- Ablation margin vs best removed component: `0.020` success and `0.046` utility.
- Stress endpoint utility margin: `0.140`.
- Strict fixed-risk coverage: `0.932`.
- Strict fixed-risk utility margin: `0.167`.

## Artifact Evidence

- `paper/main.pdf` and `C:/Users/wangz/Downloads/109.pdf` match.
- Final PDF pages: 26.
- SHA256: `556C9B781F4482C3D22B79B43E47BB362E2E4F480433D7B557FC71721D4C5873`.
- `scripts/validate_submission_artifacts.py` passed.
- Visual PDF QA passed on pages 1, 2, 5, 15, and 26.

Remaining blocker: real robot or independent high-fidelity validation with trained external policy baselines, videos/logs, and calibrated contact-risk measurements.
