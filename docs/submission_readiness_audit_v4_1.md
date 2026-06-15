# Submission Readiness Audit v4.1

Paper: 109 non_smooth_mechanics_for_foundation_policies

Date: 2026-06-15

Decision: STRONG_REVISE

ICLR main ready: no

## Rerun

- Command: `python -m py_compile src/run_experiment.py`
- Command: `python src/run_experiment.py`
- Log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/109_non_smooth_mechanics_for_foundation_policies_continuation_rerun_20260615.log`
- Numeric sanity: zero NaN/Inf issues across CSV outputs.
- PDF: `C:/Users/wangz/Downloads/109.pdf`
- PDF SHA256: `18B2B2A99CF5BD68DFADC6A4E087493841D3BDFA55520701DCA3A36F5DCC3C0D`
- PDF size: 406461 bytes.
- Desktop PDF copy: absent.

## Coverage

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1575 rows.
- `seed_task_regime_metrics.csv`: 11025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1715 rows.
- `stress_sweep.csv`: 30 rows.
- `stress_sweep_seed_metrics.csv`: 7350 rows.
- `failure_cases.csv`: 8 rows.

## Gate Evidence

- Strongest non-oracle baseline: `complementarity_residual_planner`.
- Combined-stress success: `0.540 +/- 0.004` proposed vs `0.463 +/- 0.007` strongest baseline.
- Contact-mode F1: `0.630` proposed vs `0.495` strongest baseline.
- Boundary error: `0.246` proposed vs `0.294` strongest baseline.
- Unsafe impulse: `0.064` proposed vs `0.079` strongest baseline.
- Jam rate: `0.092` proposed vs `0.112` strongest baseline.
- Slip overshoot: `0.057` proposed vs `0.076` strongest baseline.
- Intervention cost: `0.217` proposed vs `0.264` strongest baseline.
- Paired success gain: `0.076 +/- 0.007`, with `7/7` seed wins.
- Best removed-component ablation: `minus_diagnostic_micro_probe`; full method remains ahead by `0.027` success.
- Max stress level `1.0`: proposed success `0.5153 +/- 0.0072`; complementarity residual planner `0.4389 +/- 0.0031`; conformal risk filter `0.4118 +/- 0.0060`; diffusion policy surrogate `0.3881 +/- 0.0037`; oracle `0.6203 +/- 0.0071`.

## Terminal Assessment

The local evidence supports continuing the paper as a strong-revise candidate: the method beats the strongest non-oracle baseline, improves diagnostics, lowers safety/cost metrics, wins paired seeds, survives ablations, and remains above core baselines through the stress sweep.

The paper is still not ICLR-main-ready. The blocker is external validity: no real robot validation, no independent high-fidelity simulator validation, no external trained policy checkpoints, and no hardware videos or deployment logs.
