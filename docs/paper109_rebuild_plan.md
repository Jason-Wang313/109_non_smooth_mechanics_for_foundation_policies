# Paper 109 Rebuild Plan: Non-Smooth Mechanics for Foundation Policies

Started: 2026-06-15 01:25:00 +0100

## Goal

Rebuild Paper 109 from a v3 archive into an evidence-backed ICLR-main-target submission candidate, or keep it archived if the evidence fails. The paper will not claim real-robot readiness. The honest target is `STRONG_REVISE` only if local contact-mode evidence shows a decisive, safety-preserving advantage over strong smooth-policy and risk-filter baselines.

## Core Claim To Test

Foundation robot policies fail in contact-rich manipulation when they smooth across non-smooth mechanics events: impact onset, stick-slip transitions, unilateral contact activation, jamming, release, and support changes. The proposed method will expose these events through a contact-mode boundary atlas and use that atlas to gate policy actions, select diagnostic micro-probes, and avoid invalid smooth interpolations.

## Proposed Method

`proposed_contact_mode_boundary_atlas`

The method combines:
- Contact-mode classifier over free, touch, stick, slip, jam, release, and impact modes.
- Complementarity-residual score that flags physically impossible smooth predictions.
- Impulse-budget guard that limits high-velocity actions near impact boundaries.
- Stick-slip hysteresis memory to avoid oscillating between incompatible contact modes.
- Diagnostic micro-probe selector for ambiguous contact states.

## Benchmark Design

Run a local contact-mode benchmark with:
- Five tasks: peg insertion, drawer opening, cable routing, tool levering, and mobile pushing.
- Seven non-smooth regimes: nominal, impact onset, stick-slip transition, unilateral lift-off, jamming, release snap, and combined contact shock.
- Five deployment splits: nominal, seen-shift, unseen-geometry, unseen-friction, and combined-stress.
- Nine methods: no-contact behavior clone, domain randomization, diffusion-policy surrogate, robotics-transformer surrogate, ensemble disagreement planner, conformal risk filter, complementarity residual planner, proposed method, and oracle contact-mode supervisor.
- Seven paired seeds with 84 episodes per task/regime/split/method.

## Primary Metrics

- Task success.
- Contact-mode F1.
- Boundary crossing error.
- Unsafe impulse rate.
- Jam rate.
- Slip overshoot.
- Intervention cost.
- Regret to oracle contact-mode supervisor.

## Decision Gates

Mark `STRONG_REVISE` only if all are true:
- Success margin over the strongest non-oracle baseline is at least 0.030 on combined stress.
- Contact-mode F1 improves by at least 0.050 or boundary crossing error falls by at least 0.050.
- Unsafe impulse, jam rate, slip overshoot, and intervention cost do not increase versus the strongest non-oracle baseline.
- Proposed method wins at least 5 of 7 paired seeds versus the strongest non-oracle baseline.
- Removing the core contact-mode atlas reduces success by at least 0.020.

Otherwise mark `KILL_ARCHIVE`.

## Manuscript Changes

- Replace archive framing with a full paper centered on the tested non-smooth mechanics mechanism.
- Add related work around implicit contact time stepping, complementarity/contact solvers, diffusion policies, and large-scale robot transformers.
- Include local evidence tables, stress curves, ablation figures, failure cases, and limitations.
- Keep the limitation explicit: no real robot or accepted external high-fidelity benchmark validation yet.

## Artifact Requirements

- Produce `C:/Users/wangz/Downloads/109.pdf` only.
- Do not copy a PDF to the visible Desktop.
- Update `README.md`, `child_status.md`, paper docs, and root reports after the terminal decision.
- Commit and push the public GitHub repo only after local audits pass.
