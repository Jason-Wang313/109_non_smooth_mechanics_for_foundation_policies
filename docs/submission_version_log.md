# Submission Version Log

## v3

Decision: KILL_ARCHIVE

Reason: synthetic/template evidence and no real or high-fidelity validation.

## v4

Decision: STRONG_REVISE

Changes:
- Added contact-mode boundary atlas benchmark.
- Added diffusion, robotics-transformer, conformal, ensemble, and complementarity baselines.
- Added paired-seed success tests.
- Added safety/cost gates.
- Added ablations, stress sweep, failure cases, figures, and generated tables.
- Rewrote manuscript and docs around a narrow non-smooth contact-mode claim.

Remaining blocker: no real robot or independent high-fidelity validation.

## v4.1

Decision: STRONG_REVISE

Changes:
- Added a paper-specific ICLR submission-readiness execution plan before rerunning.
- Reran the full local benchmark under fixed single-threaded numeric settings.
- Expanded stress-sweep evidence from seed aggregates to 7350 task/regime/seed rows while preserving seed-level aggregate confidence intervals.
- Expanded documented failure cases from 4 to 8.
- Rechecked CSV row counts, numeric sanity, strongest baseline, paired seed wins, ablations, stress sweep, and artifact-location requirements.

Remaining blocker: no real robot or independent high-fidelity validation, no external trained policy checkpoints, and no hardware videos or deployment logs.
