# 109 Non-Smooth Mechanics for Foundation Policies

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for ICLR main-conference development.

This rebuild replaces the v3 archive with a local contact-mode benchmark. The paper is still not ICLR-main-ready because it lacks real robot or independent high-fidelity benchmark validation, but the local evidence supports continuing rather than archiving.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 non-smooth regimes x 5 deployment splits x 9 methods.
- Seeds: 7 paired seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `complementarity_residual_planner`.
- Proposed: `proposed_contact_mode_boundary_atlas`.
- Combined-stress success: `0.540 +/- 0.004` proposed vs `0.463 +/- 0.007` strongest baseline.
- Contact-mode F1: `0.630` proposed vs `0.495` strongest baseline.
- Unsafe impulse: `0.064` proposed vs `0.079` strongest baseline.
- Pairwise wins: 7/7 seeds over the strongest baseline.
- Best removed-component ablation: `minus_diagnostic_micro_probe`; full method remains ahead by `0.027` success.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/109.pdf`
