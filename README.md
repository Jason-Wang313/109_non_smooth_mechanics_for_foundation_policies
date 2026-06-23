# 109 Non-Smooth Mechanics for Foundation Policies

Submission-hardening version: v5 expanded standard

Terminal decision: STRONG_REVISE for ICLR main-conference development.

ICLR main ready: no. The local evidence now supports the mechanism under the expanded standard, but the external robotics scope gate is still false because there is no real-robot or independent high-fidelity validation with trained policy checkpoints.

## Evidence Snapshot

- Benchmark: 8 tasks x 10 non-smooth regimes x 8 deployment splits x 16 methods.
- Seeds and rollouts: 10 paired seeds, 6 episodes per cell.
- Main cells: 102400; stress-sweep cells: 48000; fixed-risk cells: 51200; ablation cells: 8000.
- Strongest non-oracle baseline: `proposed_contact_mode_boundary_atlas_v4`.
- Proposed method: `contact_mode_boundary_audit_v5`.
- Held-out hard success: `0.689` proposed vs `0.592` strongest baseline.
- Held-out hard utility: `0.767` proposed vs `0.631` strongest baseline.
- Contact-mode F1 delta: `+0.076`.
- Boundary-error delta: `-0.041`.
- Unsafe-impulse delta: `-0.018`.
- Pairwise utility wins: 10/10 seeds over the strongest non-oracle baseline.
- Ablation gate: passed; full method beats best removed component by `0.020` success and `0.046` utility.
- Stress endpoint utility margin: `0.140`.
- Strict fixed-risk coverage: `0.932`; strict fixed-risk utility margin: `0.167`.
- Failure cases: 24 documented hard-split limitations.

## Final Artifacts

- Canonical PDF: `C:/Users/wangz/Downloads/109.pdf`
- Pages: 26
- PDF SHA256: `556C9B781F4482C3D22B79B43E47BB362E2E4F480433D7B557FC71721D4C5873`
- GitHub: `https://github.com/Jason-Wang313/109_non_smooth_mechanics_for_foundation_policies`
- Numbered PDF location rule: Downloads only; no Desktop/root copy.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild Manuscript

```powershell
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

## Validate Artifacts

```powershell
python scripts\validate_submission_artifacts.py
```

The validator checks row counts, finite numeric CSV values, terminal gates, bright boxed citation settings, 25+ page count, PDF hash match to Downloads, and absence of Desktop/root numbered PDFs.
