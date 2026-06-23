# Submission Version Log

## v3

Decision: KILL_ARCHIVE

Reason: synthetic/template evidence and no real or high-fidelity validation.

## v4

Decision: STRONG_REVISE

Changes:
- Added a contact-mode boundary atlas benchmark.
- Added diffusion, robotics-transformer, conformal, ensemble, and complementarity baselines.
- Added paired-seed success tests, safety/cost gates, ablations, stress sweep, failure cases, figures, and generated tables.

Remaining blocker: no real robot or independent high-fidelity validation.

## v4.1

Decision: STRONG_REVISE

Changes:
- Added a paper-specific ICLR submission-readiness execution plan before rerunning.
- Reran the full local benchmark.
- Expanded stress-sweep evidence and documented additional failure cases.

Remaining blocker: no real robot or independent high-fidelity validation, no external trained policy checkpoints, and no hardware videos or deployment logs.

## v5 Expanded Standard

Decision: STRONG_REVISE

Changes:
- Added frozen v5 plan before edits.
- Expanded benchmark to 8 tasks x 10 regimes x 8 splits x 16 methods.
- Added 102400 main cells, 48000 stress cells, 51200 fixed-risk cells, 8000 ablation cells, and 24 failure cases.
- Added coupled arbitration mechanism and corrected ablation semantics so removed components disable the joint arbitration path.
- Passed all local empirical gates while keeping `scope_gate=false`.
- Generated a 26-page ICLR-style PDF with bright boxed clickable citations.
- Added reproducible manuscript generator and artifact validator.

Remaining blocker: external robot/high-fidelity validation with trained policy baselines.
