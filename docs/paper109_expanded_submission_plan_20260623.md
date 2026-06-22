# Paper 109 Expanded Submission Plan - 2026-06-23

## Objective

Rebuild Paper 109, `non_smooth_mechanics_for_foundation_policies`, from the v4.1 six-page local diagnostic into a 25+ page ICLR-style expanded-standard artifact. The target is not cosmetic page count. The target is a hostile-review non-smooth mechanics audit with stronger theory, stronger baselines, broader stress tests, deeper ablations, fixed-risk reporting, failure analysis, reproducibility checks, and honest terminal decision.

## Frozen Scientific Claim

Foundation-style robot policies can fail near non-smooth contact boundaries because smooth interpolation across impacts, stick-slip transitions, unilateral contact activation, release snap, jamming, compliance changes, and friction-cone changes can produce physically invalid actions. A contact-mode boundary audit should improve local success, contact-mode diagnosis, impulse safety, jam/slip behavior, fixed-risk coverage, and utility when compared with strong non-oracle baselines.

## Non-Claim

This rebuild does not claim real robot state of the art. It does not claim a new contact solver. It does not claim ICLR-main readiness without external robot or accepted high-fidelity validation, trained checkpoints, deployment logs, and rollout videos.

## v5 Benchmark Design

- Task families: peg insertion, drawer opening, cable routing, tool levering, mobile pushing, bimanual alignment, deformable press-fit, and legged foot placement.
- Non-smooth regimes: nominal contact, impact onset, stick-slip transition, unilateral lift-off, contact jamming, release snap, compliant fixture shift, friction-cone inversion, actuator backlash, and mixed non-smooth shock.
- Splits: nominal, seen contact shift, unseen geometry, unseen friction, unseen compliance, actuator latency, sensor dropout, and held-out mixed non-smooth stress.
- Methods: no-contact BC, domain randomization, diffusion surrogate, robotics-transformer surrogate, ensemble disagreement, conformal risk filter, smooth dynamics world model, contact implicit MPC, complementarity residual planner, robust hybrid MPC, learned contact classifier, energy barrier policy, v4 contact-mode boundary atlas, v5 contact-mode boundary audit, oracle contact supervisor, and oracle hybrid controller.
- Seeds: 10 paired seeds.
- Episodes per cell: 6 to keep CPU/RAM light while preserving broad coverage.

Expected main evidence scale:

- dataset-summary rows: `640`
- main cell rows: `102400`
- main group rows: `10240`
- seed metric rows: `1280`
- metric rows: `128`
- hard seed rows: `160`
- hard metric rows: `16`
- hard pairwise rows: `15`
- ablation cell rows: `8000`
- stress cell rows: `48000`
- fixed-risk cell rows: `51200`
- failure cases: `24`

## Metrics

Primary metrics: success, utility, contact-mode F1, boundary error, complementarity residual, impulse violation, unsafe impulse, jam rate, slip overshoot, mode-switch latency, recovery success, energy spike, calibration ECE, intervention cost, fixed-risk coverage, and regret to oracle.

The manuscript must report success and safety together. It must not allow a method to win by abstaining, by hiding safety failures, or by relying only on average success.

## Frozen Gates

The final terminal decision is determined by predefined gates:

- Success gate: v5 must beat the strongest non-oracle baseline by at least `0.03` success or `0.05` utility on the hard aggregate.
- Diagnostic gate: v5 must improve contact-mode F1 by at least `0.05` or reduce boundary error by at least `0.04`.
- Safety gate: v5 must not increase impulse violation, unsafe impulse, jam rate, slip overshoot, mode-switch latency, energy spike, calibration ECE, intervention cost, or tail risk beyond frozen tolerances.
- Pairwise gate: v5 must win at least 8 of 10 paired seeds on success or utility against the strongest non-oracle baseline.
- Ablation gate: full v5 must beat the best removed-component ablation by at least `0.02` success or `0.04` utility.
- Stress gate: v5 must retain positive utility margin at maximum non-smooth stress.
- Fixed-risk gate: v5 must maintain useful strict-budget coverage and positive utility margin at fixed-risk budgets.
- Scope gate: fails unless external robot or accepted high-fidelity validation exists.

If local gates fail, the paper becomes KILL_ARCHIVE. If local gates pass but scope fails, it remains STRONG_REVISE. It cannot be marked ICLR-main-ready in this local rebuild.

## Ablations

Remove one mechanism at a time: contact-mode classifier, complementarity residual, impulse guard, stick-slip hysteresis, diagnostic micro-probe, compliance estimator, mode-switch latency guard, energy-barrier check, and fixed-risk acceptor. The v4 atlas remains a main strong baseline rather than a removed-component ablation, keeping the planned ablation table to 10 total variants including the full method.

## Stress And Fixed-Risk Protocols

Stress sweep: 10 non-smooth intensity levels, 6 key methods, 8 tasks, 10 regimes, 10 seeds.

Fixed-risk budgets: `0.08`, `0.12`, `0.16`, and `0.20`, evaluated across all methods/tasks/regimes/seeds.

## Manuscript Requirements

- 25+ page ICLR-style PDF.
- Bright boxed clickable citation links using `hyperref`.
- Theory section on why smooth average policy metrics do not identify non-smooth boundary risk.
- Formal problem setup for action validity across contact-mode transitions.
- Generated tables and figures from source.
- Failure-case appendix, fixed-risk appendix, external robot protocol appendix, safety appendix, and manual related-work checklist.
- Explicit terminal decision and scope-gate limitation.

## Artifact Rules

- Canonical numbered PDF: `C:/Users/wangz/Downloads/109.pdf`.
- No `109.pdf` on visible Desktop, factory root, or child repo root.
- Final validator must check row counts, finite CSV values, local gates, scope failure, bright citation boxes, page count, PDF hash equality, and numbered-PDF location.
- Public GitHub repo must be updated with the final v5 artifact.
- Final HEAD should use GitHub-attributed author/committer: `Jason-Wang313 <202470630+Jason-Wang313@users.noreply.github.com>`.

## Development Discipline

Use strong baselines and stress tests to expose weaknesses. Improve the method only when the weakness is mechanistically justified, then freeze and report all predefined results honestly. Do not optimize for pretty results. Optimize for a result that survives hostile review.
