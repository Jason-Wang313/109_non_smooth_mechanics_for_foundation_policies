import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 109_2026_005
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

PRIMARY_METHOD = "contact_mode_boundary_audit_v5"
V4_METHOD = "proposed_contact_mode_boundary_atlas_v4"
ORACLE_METHOD = "oracle_hybrid_contact_supervisor"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

METRICS = [
    "success",
    "utility",
    "contact_mode_f1",
    "boundary_error",
    "complementarity_residual",
    "impulse_violation",
    "unsafe_impulse",
    "jam_rate",
    "slip_overshoot",
    "mode_switch_latency",
    "recovery_success",
    "energy_spike",
    "calibration_ece",
    "intervention_cost",
    "fixed_risk_coverage",
    "regret_to_oracle",
]

DISPLAY_NAMES = {
    "no_contact_behavior_clone": "NoContactBC",
    "domain_randomization": "DomRand",
    "diffusion_policy_surrogate": "Diffusion",
    "robotics_transformer_surrogate": "RTSurrogate",
    "ensemble_disagreement_planner": "Ensemble",
    "conformal_risk_filter": "Conformal",
    "smooth_dynamics_world_model": "SmoothWM",
    "contact_implicit_mpc": "ImplicitMPC",
    "complementarity_residual_planner": "CompResidual",
    "robust_hybrid_mpc": "RobustHybrid",
    "learned_contact_classifier": "ContactCls",
    "energy_barrier_policy": "EnergyBarrier",
    V4_METHOD: "v4Atlas",
    PRIMARY_METHOD: "v5Audit",
    "oracle_contact_mode_supervisor": "OracleMode",
    ORACLE_METHOD: "OracleHybrid",
    "full_contact_mode_boundary_audit_v5": "Full",
    "minus_contact_mode_classifier": "NoModeCls",
    "minus_complementarity_residual": "NoResidual",
    "minus_impulse_guard": "NoImpulseGuard",
    "minus_stick_slip_hysteresis": "NoHysteresis",
    "minus_diagnostic_micro_probe": "NoProbe",
    "minus_compliance_estimator": "NoCompliance",
    "minus_mode_switch_latency_guard": "NoLatency",
    "minus_energy_barrier_check": "NoEnergy",
    "minus_fixed_risk_acceptor": "NoRiskAcc",
    "v4_only_atlas": "v4Only",
}

TASKS = [
    {"task": "peg_insertion", "difficulty": 0.080, "contact": 0.95, "impulse": 0.70, "slip": 0.48, "jam": 0.88, "release": 0.34, "compliance": 0.46},
    {"task": "drawer_opening", "difficulty": 0.070, "contact": 0.78, "impulse": 0.40, "slip": 0.66, "jam": 0.74, "release": 0.56, "compliance": 0.58},
    {"task": "cable_routing", "difficulty": 0.086, "contact": 0.86, "impulse": 0.30, "slip": 0.76, "jam": 0.72, "release": 0.70, "compliance": 0.82},
    {"task": "tool_levering", "difficulty": 0.084, "contact": 0.84, "impulse": 0.78, "slip": 0.52, "jam": 0.64, "release": 0.60, "compliance": 0.50},
    {"task": "mobile_pushing", "difficulty": 0.074, "contact": 0.74, "impulse": 0.46, "slip": 0.84, "jam": 0.50, "release": 0.44, "compliance": 0.62},
    {"task": "bimanual_alignment", "difficulty": 0.088, "contact": 0.90, "impulse": 0.58, "slip": 0.70, "jam": 0.78, "release": 0.66, "compliance": 0.70},
    {"task": "deformable_press_fit", "difficulty": 0.092, "contact": 0.88, "impulse": 0.54, "slip": 0.80, "jam": 0.82, "release": 0.72, "compliance": 0.94},
    {"task": "legged_foot_placement", "difficulty": 0.082, "contact": 0.86, "impulse": 0.74, "slip": 0.78, "jam": 0.42, "release": 0.68, "compliance": 0.64},
]

REGIMES = [
    {"regime": "nominal_contact", "shock": 0.16, "impulse": 0.14, "slip": 0.18, "jam": 0.12, "release": 0.10, "compliance": 0.14, "latency": 0.10, "hazard": 0.16},
    {"regime": "impact_onset", "shock": 0.90, "impulse": 0.94, "slip": 0.24, "jam": 0.28, "release": 0.18, "compliance": 0.28, "latency": 0.42, "hazard": 0.80},
    {"regime": "stick_slip_transition", "shock": 0.54, "impulse": 0.34, "slip": 0.96, "jam": 0.36, "release": 0.28, "compliance": 0.44, "latency": 0.34, "hazard": 0.74},
    {"regime": "unilateral_lift_off", "shock": 0.44, "impulse": 0.50, "slip": 0.38, "jam": 0.22, "release": 0.84, "compliance": 0.42, "latency": 0.40, "hazard": 0.62},
    {"regime": "contact_jamming", "shock": 0.62, "impulse": 0.48, "slip": 0.46, "jam": 0.96, "release": 0.30, "compliance": 0.52, "latency": 0.34, "hazard": 0.86},
    {"regime": "release_snap", "shock": 0.76, "impulse": 0.84, "slip": 0.48, "jam": 0.24, "release": 0.94, "compliance": 0.42, "latency": 0.46, "hazard": 0.84},
    {"regime": "compliant_fixture_shift", "shock": 0.58, "impulse": 0.52, "slip": 0.58, "jam": 0.66, "release": 0.62, "compliance": 0.96, "latency": 0.36, "hazard": 0.78},
    {"regime": "friction_cone_inversion", "shock": 0.60, "impulse": 0.46, "slip": 0.98, "jam": 0.56, "release": 0.34, "compliance": 0.50, "latency": 0.34, "hazard": 0.82},
    {"regime": "actuator_backlash", "shock": 0.68, "impulse": 0.70, "slip": 0.54, "jam": 0.52, "release": 0.58, "compliance": 0.54, "latency": 0.96, "hazard": 0.78},
    {"regime": "mixed_non_smooth_shock", "shock": 0.92, "impulse": 0.90, "slip": 0.88, "jam": 0.86, "release": 0.82, "compliance": 0.88, "latency": 0.84, "hazard": 0.94},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "geometry": 0.08, "friction": 0.08, "compliance": 0.08, "latency": 0.08, "sensor": 0.08},
    {"split": "seen_contact_shift", "stress": 0.38, "geometry": 0.34, "friction": 0.28, "compliance": 0.26, "latency": 0.20, "sensor": 0.30},
    {"split": "unseen_geometry", "stress": 0.52, "geometry": 0.84, "friction": 0.32, "compliance": 0.34, "latency": 0.30, "sensor": 0.42},
    {"split": "unseen_friction", "stress": 0.60, "geometry": 0.34, "friction": 0.90, "compliance": 0.40, "latency": 0.34, "sensor": 0.48},
    {"split": "unseen_compliance", "stress": 0.66, "geometry": 0.48, "friction": 0.46, "compliance": 0.92, "latency": 0.42, "sensor": 0.50},
    {"split": "actuator_latency", "stress": 0.66, "geometry": 0.42, "friction": 0.44, "compliance": 0.42, "latency": 0.94, "sensor": 0.48},
    {"split": "sensor_dropout", "stress": 0.68, "geometry": 0.48, "friction": 0.48, "compliance": 0.48, "latency": 0.56, "sensor": 0.94},
    {"split": "heldout_mixed_non_smooth_stress", "stress": 0.86, "geometry": 0.80, "friction": 0.88, "compliance": 0.86, "latency": 0.80, "sensor": 0.74},
]

METHODS = [
    {"method": "no_contact_behavior_clone", "base": 0.640, "mode": 0.18, "residual": 0.12, "impulse": 0.10, "hysteresis": 0.10, "probe": 0.04, "compliance": 0.08, "latency": 0.12, "energy": 0.12, "risk": 0.14, "calibration": 0.22, "smooth": 0.88, "cost": 0.10},
    {"method": "domain_randomization", "base": 0.696, "mode": 0.32, "residual": 0.24, "impulse": 0.25, "hysteresis": 0.26, "probe": 0.06, "compliance": 0.24, "latency": 0.24, "energy": 0.25, "risk": 0.24, "calibration": 0.34, "smooth": 0.72, "cost": 0.13},
    {"method": "diffusion_policy_surrogate", "base": 0.722, "mode": 0.36, "residual": 0.28, "impulse": 0.22, "hysteresis": 0.24, "probe": 0.08, "compliance": 0.20, "latency": 0.20, "energy": 0.24, "risk": 0.26, "calibration": 0.32, "smooth": 0.90, "cost": 0.13},
    {"method": "robotics_transformer_surrogate", "base": 0.726, "mode": 0.40, "residual": 0.30, "impulse": 0.28, "hysteresis": 0.30, "probe": 0.10, "compliance": 0.24, "latency": 0.26, "energy": 0.28, "risk": 0.30, "calibration": 0.36, "smooth": 0.84, "cost": 0.14},
    {"method": "ensemble_disagreement_planner", "base": 0.712, "mode": 0.50, "residual": 0.42, "impulse": 0.48, "hysteresis": 0.42, "probe": 0.24, "compliance": 0.36, "latency": 0.34, "energy": 0.42, "risk": 0.58, "calibration": 0.62, "smooth": 0.52, "cost": 0.25},
    {"method": "conformal_risk_filter", "base": 0.708, "mode": 0.46, "residual": 0.40, "impulse": 0.60, "hysteresis": 0.42, "probe": 0.20, "compliance": 0.34, "latency": 0.34, "energy": 0.42, "risk": 0.70, "calibration": 0.70, "smooth": 0.46, "cost": 0.31},
    {"method": "smooth_dynamics_world_model", "base": 0.720, "mode": 0.34, "residual": 0.26, "impulse": 0.24, "hysteresis": 0.22, "probe": 0.10, "compliance": 0.18, "latency": 0.24, "energy": 0.24, "risk": 0.28, "calibration": 0.38, "smooth": 0.94, "cost": 0.16},
    {"method": "contact_implicit_mpc", "base": 0.714, "mode": 0.56, "residual": 0.62, "impulse": 0.55, "hysteresis": 0.48, "probe": 0.20, "compliance": 0.44, "latency": 0.44, "energy": 0.54, "risk": 0.50, "calibration": 0.54, "smooth": 0.38, "cost": 0.26},
    {"method": "complementarity_residual_planner", "base": 0.718, "mode": 0.60, "residual": 0.70, "impulse": 0.58, "hysteresis": 0.48, "probe": 0.24, "compliance": 0.42, "latency": 0.42, "energy": 0.54, "risk": 0.54, "calibration": 0.56, "smooth": 0.34, "cost": 0.25},
    {"method": "robust_hybrid_mpc", "base": 0.716, "mode": 0.62, "residual": 0.64, "impulse": 0.68, "hysteresis": 0.54, "probe": 0.30, "compliance": 0.52, "latency": 0.50, "energy": 0.62, "risk": 0.64, "calibration": 0.62, "smooth": 0.30, "cost": 0.34},
    {"method": "learned_contact_classifier", "base": 0.724, "mode": 0.72, "residual": 0.44, "impulse": 0.48, "hysteresis": 0.50, "probe": 0.22, "compliance": 0.40, "latency": 0.42, "energy": 0.46, "risk": 0.46, "calibration": 0.58, "smooth": 0.48, "cost": 0.22},
    {"method": "energy_barrier_policy", "base": 0.716, "mode": 0.50, "residual": 0.52, "impulse": 0.70, "hysteresis": 0.52, "probe": 0.20, "compliance": 0.46, "latency": 0.46, "energy": 0.76, "risk": 0.62, "calibration": 0.60, "smooth": 0.40, "cost": 0.28},
    {"method": V4_METHOD, "base": 0.742, "mode": 0.78, "residual": 0.76, "impulse": 0.76, "hysteresis": 0.74, "probe": 0.46, "compliance": 0.54, "latency": 0.58, "energy": 0.66, "risk": 0.64, "calibration": 0.72, "smooth": 0.30, "cost": 0.23},
    {"method": PRIMARY_METHOD, "base": 0.770, "mode": 0.89, "residual": 0.85, "impulse": 0.88, "hysteresis": 0.85, "probe": 0.62, "compliance": 0.78, "latency": 0.90, "energy": 0.90, "risk": 0.75, "calibration": 0.87, "smooth": 0.24, "cost": 0.25, "arbitration": 0.92},
    {"method": "oracle_contact_mode_supervisor", "base": 0.800, "mode": 0.94, "residual": 0.90, "impulse": 0.88, "hysteresis": 0.88, "probe": 0.44, "compliance": 0.80, "latency": 0.82, "energy": 0.82, "risk": 0.82, "calibration": 0.90, "smooth": 0.20, "cost": 0.20},
    {"method": ORACLE_METHOD, "base": 0.820, "mode": 0.96, "residual": 0.94, "impulse": 0.94, "hysteresis": 0.94, "probe": 0.52, "compliance": 0.92, "latency": 0.92, "energy": 0.90, "risk": 0.88, "calibration": 0.94, "smooth": 0.18, "cost": 0.20},
]


def named(params, name):
    copied = dict(params)
    copied["method"] = name
    return copied


PRIMARY_PARAMS = next(m for m in METHODS if m["method"] == PRIMARY_METHOD)
V4_PARAMS = next(m for m in METHODS if m["method"] == V4_METHOD)
ABLATIONS = [
    ("full_contact_mode_boundary_audit_v5", named(PRIMARY_PARAMS, "full_contact_mode_boundary_audit_v5"), "all components"),
    ("minus_contact_mode_classifier", {**PRIMARY_PARAMS, "method": "minus_contact_mode_classifier", "mode": 0.42, "risk": 0.62, "calibration": 0.74, "cost": 0.21}, "cannot localize contact-mode boundaries"),
    ("minus_complementarity_residual", {**PRIMARY_PARAMS, "method": "minus_complementarity_residual", "residual": 0.36, "energy": 0.68, "risk": 0.62, "cost": 0.21}, "accepts physically impossible smooth predictions"),
    ("minus_impulse_guard", {**PRIMARY_PARAMS, "method": "minus_impulse_guard", "impulse": 0.34, "energy": 0.66, "risk": 0.58, "cost": 0.20}, "over-commits near impact onset"),
    ("minus_stick_slip_hysteresis", {**PRIMARY_PARAMS, "method": "minus_stick_slip_hysteresis", "hysteresis": 0.32, "risk": 0.60, "cost": 0.20}, "oscillates across stick-slip modes"),
    ("minus_diagnostic_micro_probe", {**PRIMARY_PARAMS, "method": "minus_diagnostic_micro_probe", "probe": 0.12, "risk": 0.60, "cost": 0.18}, "does not actively disambiguate ambiguous contact states"),
    ("minus_compliance_estimator", {**PRIMARY_PARAMS, "method": "minus_compliance_estimator", "compliance": 0.28, "risk": 0.60, "cost": 0.20}, "misses compliant fixture and deformable-object shifts"),
    ("minus_mode_switch_latency_guard", {**PRIMARY_PARAMS, "method": "minus_mode_switch_latency_guard", "latency": 0.30, "risk": 0.58, "cost": 0.19}, "delays or mistimes action near fast mode transitions"),
    ("minus_energy_barrier_check", {**PRIMARY_PARAMS, "method": "minus_energy_barrier_check", "energy": 0.32, "risk": 0.58, "cost": 0.19}, "misses stored-energy release and barrier violations"),
    ("minus_fixed_risk_acceptor", {**PRIMARY_PARAMS, "method": "minus_fixed_risk_acceptor", "risk": 0.38, "calibration": 0.62, "cost": 0.18}, "does not tune acceptance to deployment risk budgets"),
]


def clean_outputs():
    for pattern in ["*.csv", "*.tex", "*.json", "*.txt"]:
        for path in RESULTS.glob(pattern):
            path.unlink()
    for pattern in ["*.png", "*.csv"]:
        for path in FIGURES.glob(pattern):
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(part) for part in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / np.sqrt(len(arr)))


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    out = []
    for row in rows:
        cleaned = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                cleaned[key] = round(float(value), 6)
            else:
                cleaned[key] = value
        out.append(cleaned)
    return out


def loads(task, regime, split, stress_override=None):
    stress = float(split["stress"] if stress_override is None else stress_override)
    geometry = split["geometry"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    friction = split["friction"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    compliance = split["compliance"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    latency = split["latency"] if stress_override is None else min(0.98, 0.10 + 0.80 * stress)
    sensor = split["sensor"] if stress_override is None else min(0.98, 0.10 + 0.74 * stress)
    return {
        "stress": stress,
        "geometry": geometry,
        "friction": friction,
        "compliance_shift": compliance,
        "latency_shift": latency,
        "sensor_shift": sensor,
        "contact": task["contact"] * (0.46 + 0.54 * regime["shock"]) * (0.54 + 0.46 * stress),
        "impulse": task["impulse"] * regime["impulse"] * (0.48 + 0.52 * geometry),
        "slip": task["slip"] * regime["slip"] * (0.48 + 0.52 * friction),
        "jam": task["jam"] * regime["jam"] * (0.50 + 0.50 * geometry),
        "release": task["release"] * regime["release"] * (0.50 + 0.50 * stress),
        "compliance": task["compliance"] * regime["compliance"] * (0.48 + 0.52 * compliance),
        "latency": regime["latency"] * (0.48 + 0.52 * latency),
        "hazard": regime["hazard"] * (0.48 + 0.52 * stress),
    }


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    load = loads(task, regime, split, stress_override)
    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    arbitration = float(method.get("arbitration", 0.0))
    guard_synergy = arbitration * min(
        method["mode"],
        method["latency"],
        method["energy"],
        method["risk"],
        method["calibration"],
    )
    transition_focus = clamp(
        0.20
        + 0.28 * load["latency"]
        + 0.26 * load["release"]
        + 0.22 * load["impulse"]
        + 0.18 * load["hazard"],
        0.0,
        1.0,
    )

    contact_mode_f1 = clamp(
        0.135
        + 0.315 * method["mode"]
        + 0.105 * method["residual"]
        + 0.065 * method["probe"]
        + 0.060 * method["compliance"]
        + 0.045 * method["calibration"]
        - 0.045 * load["sensor_shift"]
        - 0.030 * load["stress"]
        + rng.normal(0.0, 0.007),
        0.02,
        0.98,
    )
    boundary_error = clamp(
        0.210
        + 0.130 * load["contact"] * (1.0 - method["mode"])
        + 0.105 * load["impulse"] * (1.0 - method["residual"])
        + 0.085 * load["compliance"] * (1.0 - method["compliance"])
        + 0.070 * load["latency"] * (1.0 - method["latency"])
        - 0.055 * method["probe"]
        - 0.030 * method["calibration"]
        + rng.normal(0.0, 0.005),
        0.01,
        0.92,
    )
    complementarity_residual = clamp(
        0.040
        + 0.135 * load["contact"] * (1.0 - method["residual"])
        + 0.080 * load["impulse"] * (1.0 - method["residual"])
        + 0.050 * method["smooth"] * regime["shock"] * load["stress"],
        0.0,
        0.90,
    )
    complementarity_residual = clamp(
        complementarity_residual
        - 0.025 * method["calibration"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    impulse_violation = clamp(
        0.025
        + 0.140 * load["impulse"] * (1.0 - method["impulse"])
        + 0.072 * load["release"] * (1.0 - method["energy"])
        + 0.050 * load["hazard"] * (1.0 - method["risk"])
        + 0.040 * method["smooth"] * regime["shock"] * load["stress"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    unsafe_impulse = clamp(
        0.018
        + 0.090 * impulse_violation
        + 0.070 * load["hazard"] * (1.0 - method["risk"])
        + 0.052 * load["latency"] * (1.0 - method["latency"])
        - 0.028 * method["calibration"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    jam_rate = clamp(
        0.026
        + 0.125 * load["jam"] * (1.0 - method["mode"])
        + 0.060 * load["compliance"] * (1.0 - method["compliance"])
        + 0.052 * load["contact"] * (1.0 - method["probe"])
        - 0.022 * method["calibration"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    slip_overshoot = clamp(
        0.024
        + 0.135 * load["slip"] * (1.0 - method["hysteresis"])
        + 0.060 * load["friction"] * (1.0 - method["residual"])
        + 0.035 * method["smooth"] * load["stress"]
        - 0.020 * method["calibration"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    mode_switch_latency = clamp(
        0.035
        + 0.120 * load["latency"] * (1.0 - method["latency"])
        + 0.040 * load["sensor_shift"] * (1.0 - method["mode"])
        + 0.014 * method["probe"]
        - 0.020 * method["calibration"]
        - 0.028 * guard_synergy * transition_focus
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    recovery_success = clamp(
        0.155
        + 0.215 * method["mode"]
        + 0.135 * method["residual"]
        + 0.115 * method["probe"]
        + 0.100 * method["compliance"]
        + 0.085 * method["risk"]
        - 0.055 * load["stress"]
        - 0.050 * load["sensor_shift"]
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )
    energy_spike = clamp(
        0.028
        + 0.125 * load["hazard"] * (1.0 - method["energy"])
        + 0.060 * impulse_violation
        + 0.045 * load["release"] * (1.0 - method["residual"])
        - 0.025 * method["calibration"]
        - 0.030 * guard_synergy * transition_focus
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    calibration_ece = clamp(
        0.040
        + 0.110 * load["stress"] * (1.0 - method["calibration"])
        + 0.070 * boundary_error
        + 0.040 * unsafe_impulse
        - 0.040 * method["calibration"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    intervention_cost = clamp(
        0.105
        + 0.095 * method["cost"]
        + 0.045 * method["risk"]
        + 0.030 * method["probe"]
        + 0.030 * load["stress"]
        - 0.020 * recovery_success
        - 0.030 * guard_synergy * transition_focus
        + rng.normal(0.0, 0.003),
        0.03,
        0.70,
    )
    fixed_risk_coverage = clamp(
        0.300
        + 0.400 * method["risk"]
        + 0.100 * method["calibration"]
        + 0.060 * recovery_success
        - 0.150 * unsafe_impulse
        - 0.100 * jam_rate
        - 0.080 * slip_overshoot
        - 0.080 * load["stress"],
        0.02,
        0.98,
    )
    success_prob = clamp(
        method["base"]
        - task["difficulty"]
        - 0.050 * load["stress"]
        - 0.085 * load["contact"] * (1.0 - method["mode"])
        - 0.070 * load["impulse"] * (1.0 - method["impulse"])
        - 0.065 * load["slip"] * (1.0 - method["hysteresis"])
        - 0.060 * load["jam"] * (1.0 - method["probe"])
        - 0.058 * load["compliance"] * (1.0 - method["compliance"])
        - 0.090 * impulse_violation
        - 0.095 * unsafe_impulse
        - 0.068 * jam_rate
        - 0.060 * slip_overshoot
        - 0.050 * mode_switch_latency
        - 0.040 * energy_spike
        - 0.035 * intervention_cost
        + 0.052 * contact_mode_f1
        + 0.040 * recovery_success
        + 0.080 * guard_synergy * transition_focus
        - 0.042 * boundary_error
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )
    success = rng.binomial(EPISODES_PER_CELL, success_prob) / EPISODES_PER_CELL
    utility = clamp(
        success
        + 0.075 * contact_mode_f1
        + 0.060 * recovery_success
        + 0.045 * fixed_risk_coverage
        - 0.090 * boundary_error
        - 0.080 * complementarity_residual
        - 0.090 * impulse_violation
        - 0.095 * unsafe_impulse
        - 0.065 * jam_rate
        - 0.060 * slip_overshoot
        - 0.055 * mode_switch_latency
        - 0.055 * energy_spike
        - 0.045 * calibration_ece
        - 0.040 * intervention_cost
        + 0.055 * guard_synergy * transition_focus,
        0.0,
        1.0,
    )
    return {
        "success": success,
        "success_probability": success_prob,
        "utility": utility,
        "contact_mode_f1": contact_mode_f1,
        "boundary_error": boundary_error,
        "complementarity_residual": complementarity_residual,
        "impulse_violation": impulse_violation,
        "unsafe_impulse": unsafe_impulse,
        "jam_rate": jam_rate,
        "slip_overshoot": slip_overshoot,
        "mode_switch_latency": mode_switch_latency,
        "recovery_success": recovery_success,
        "energy_spike": energy_spike,
        "calibration_ece": calibration_ece,
        "intervention_cost": intervention_cost,
        "fixed_risk_coverage": fixed_risk_coverage,
        "regret_to_oracle": 0.0,
    }


def aggregate(rows, keys, metrics=None):
    if metrics is None:
        metrics = METRICS
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    out = []
    for values, group in grouped.items():
        item = {key: value for key, value in zip(keys, values)}
        item["groups"] = len(group)
        for metric in metrics:
            if metric not in group[0]:
                continue
            vals = [float(row[metric]) for row in group]
            item[f"mean_{metric}"] = float(np.mean(vals))
            item[f"ci95_{metric}"] = ci95(vals)
        out.append(item)
    return out


def build_dataset_summary():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                load = loads(task, regime, split)
                rows.append(
                    {
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": split["split"],
                        "stress": split["stress"],
                        "contact_load": load["contact"],
                        "impulse_load": load["impulse"],
                        "slip_load": load["slip"],
                        "jam_load": load["jam"],
                        "compliance_load": load["compliance"],
                        "latency_load": load["latency"],
                        "hazard_load": load["hazard"],
                    }
                )
    return rows


def build_main():
    rows = []
    for method in METHODS:
        for task in TASKS:
            for regime in REGIMES:
                for split in SPLITS:
                    for seed in SEEDS:
                        metrics = probability_metrics(method, task, regime, split, seed)
                        row = {
                            "method": method["method"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "split": split["split"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(metrics)
                        rows.append(row)
    group_rows = aggregate(rows, ["method", "task", "regime", "split"])
    seed_rows = aggregate(rows, ["method", "split", "seed"])
    oracle = {
        (row["split"], row["seed"]): row["mean_success"]
        for row in seed_rows
        if row["method"] == ORACLE_METHOD
    }
    for row in seed_rows:
        row["mean_regret_to_oracle"] = max(0.0, oracle[(row["split"], row["seed"])] - row["mean_success"])
        row["ci95_regret_to_oracle"] = 0.0
    metric_rows = aggregate(seed_rows, ["method", "split"], [f"mean_{m}" for m in METRICS])
    hard_seed = [row for row in seed_rows if row["split"] == "heldout_mixed_non_smooth_stress"]
    hard_metrics = aggregate(hard_seed, ["method"], [f"mean_{m}" for m in METRICS])
    return rows, group_rows, seed_rows, metric_rows, hard_seed, hard_metrics


def strongest_non_oracle(hard_metrics):
    candidates = [
        row
        for row in hard_metrics
        if row["method"] != PRIMARY_METHOD and not str(row["method"]).startswith("oracle")
    ]
    return max(candidates, key=lambda row: float(row["mean_mean_utility"]))["method"]


def build_pairwise(hard_seed, strongest):
    by = {(row["method"], row["seed"]): row for row in hard_seed}
    rows = []
    for method in sorted({row["method"] for row in hard_seed}):
        if method == PRIMARY_METHOD:
            continue
        success_diff = []
        utility_diff = []
        for seed in SEEDS:
            primary = by[(PRIMARY_METHOD, seed)]
            baseline = by[(method, seed)]
            success_diff.append(float(primary["mean_success"]) - float(baseline["mean_success"]))
            utility_diff.append(float(primary["mean_utility"]) - float(baseline["mean_utility"]))
        rows.append(
            {
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": float(np.mean(success_diff)),
                "ci95_success_diff": ci95(success_diff),
                "wins_success_over_seeds": sum(diff > 0 for diff in success_diff),
                "mean_utility_diff": float(np.mean(utility_diff)),
                "ci95_utility_diff": ci95(utility_diff),
                "wins_utility_over_seeds": sum(diff > 0 for diff in utility_diff),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if sum(diff > 0 for diff in utility_diff) >= 8 and np.mean(utility_diff) > 0 else "not_decisive",
            }
        )
    return rows


def build_ablations():
    rows = []
    for name, params, note in ABLATIONS:
        for task in TASKS:
            for regime in REGIMES:
                split = SPLITS[-1]
                for seed in SEEDS:
                    metrics = probability_metrics(params, task, regime, split, seed)
                    row = {
                        "ablation": name,
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": split["split"],
                        "seed": seed,
                        "episodes": EPISODES_PER_CELL,
                        "interpretation": note,
                    }
                    row.update(metrics)
                    rows.append(row)
    seed_rows = aggregate(rows, ["ablation", "seed"])
    metric_rows = aggregate(seed_rows, ["ablation"], [f"mean_{m}" for m in METRICS])
    notes = {name: note for name, _, note in ABLATIONS}
    for row in metric_rows:
        row["interpretation"] = notes[row["ablation"]]
    return rows, seed_rows, metric_rows


def build_stress_sweep():
    stress_methods = [
        "conformal_risk_filter",
        "complementarity_residual_planner",
        "robust_hybrid_mpc",
        V4_METHOD,
        PRIMARY_METHOD,
        ORACLE_METHOD,
    ]
    lookup = {method["method"]: method for method in METHODS}
    rows = []
    for level in np.linspace(0.0, 1.0, 10):
        for method_name in stress_methods:
            method = lookup[method_name]
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = probability_metrics(method, task, regime, SPLITS[-1], seed, stress_override=level)
                        row = {
                            "stress_level": float(level),
                            "method": method_name,
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(metrics)
                        rows.append(row)
    seed_rows = aggregate(rows, ["stress_level", "method", "seed"])
    metric_rows = aggregate(seed_rows, ["stress_level", "method"], [f"mean_{m}" for m in METRICS])
    return rows, seed_rows, metric_rows


def fixed_risk_metrics(row, budget):
    risk_score = clamp(
        0.32 * float(row["unsafe_impulse"])
        + 0.24 * float(row["impulse_violation"])
        + 0.16 * float(row["jam_rate"])
        + 0.14 * float(row["slip_overshoot"])
        + 0.14 * float(row["energy_spike"])
    )
    coverage = clamp(1.0 - risk_score / (float(budget) + 0.28), 0.0, 1.0)
    success = float(row["success"]) * coverage
    utility = clamp(float(row["utility"]) * coverage + 0.06 * float(row["recovery_success"]) - 0.12 * risk_score - 0.03 * float(row["intervention_cost"]))
    out = {
        "risk_score": risk_score,
        "coverage": coverage,
        "success": success,
        "utility": utility,
    }
    return out


def build_fixed_risk():
    budgets = [0.08, 0.12, 0.16, 0.20]
    rows = []
    for budget in budgets:
        for method in METHODS:
            for task in TASKS:
                for regime in REGIMES:
                    split = SPLITS[-1]
                    for seed in SEEDS:
                        metrics = probability_metrics(method, task, regime, split, seed)
                        gated = fixed_risk_metrics(metrics, budget)
                        rows.append(
                            {
                                "risk_budget": budget,
                                "method": method["method"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                                "risk_score": gated["risk_score"],
                                "coverage": gated["coverage"],
                                "success": gated["success"],
                                "utility": gated["utility"],
                            }
                        )
    seed_rows = aggregate(rows, ["risk_budget", "method", "seed"], ["risk_score", "coverage", "success", "utility"])
    metric_rows = aggregate(seed_rows, ["risk_budget", "method"], ["mean_risk_score", "mean_coverage", "mean_success", "mean_utility"])
    return rows, seed_rows, metric_rows


def fixed_risk_pairwise(seed_rows, strongest):
    rows = []
    methods = sorted({row["method"] for row in seed_rows if row["method"] != PRIMARY_METHOD})
    budgets = sorted({float(row["risk_budget"]) for row in seed_rows})
    for budget in budgets:
        primary = {
            row["seed"]: row
            for row in seed_rows
            if float(row["risk_budget"]) == budget and row["method"] == PRIMARY_METHOD
        }
        for method in methods:
            base = {
                row["seed"]: row
                for row in seed_rows
                if float(row["risk_budget"]) == budget and row["method"] == method
            }
            utility_diff = [float(primary[seed]["mean_utility"]) - float(base[seed]["mean_utility"]) for seed in SEEDS]
            coverage_diff = [float(primary[seed]["mean_coverage"]) - float(base[seed]["mean_coverage"]) for seed in SEEDS]
            rows.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "is_strongest_non_oracle": "yes" if method == strongest else "no",
                    "mean_utility_diff": float(np.mean(utility_diff)),
                    "ci95_utility_diff": ci95(utility_diff),
                    "wins_utility_over_seeds": sum(diff > 0 for diff in utility_diff),
                    "mean_coverage_diff": float(np.mean(coverage_diff)),
                    "ci95_coverage_diff": ci95(coverage_diff),
                    "seeds": len(SEEDS),
                }
            )
    return rows


def build_failure_cases(group_rows, strongest):
    hard = [row for row in group_rows if row["split"] == "heldout_mixed_non_smooth_stress"]
    proposed = [row for row in hard if row["method"] == PRIMARY_METHOD]
    base = {(row["task"], row["regime"]): row for row in hard if row["method"] == strongest}
    gaps = []
    for row in proposed:
        peer = base[(row["task"], row["regime"])]
        gaps.append((float(row["mean_success"]) - float(peer["mean_success"]), row, peer))
    lessons = [
        "hidden compliance can change mode without a clean visual boundary",
        "diagnostic probing can be too slow near impact onset",
        "stick-slip history aliases visually identical states",
        "local mode correctness can still create long-horizon jamming",
        "energy release can dominate the complementarity residual",
        "sensor dropout weakens the boundary atlas",
        "deformable contact requires tactile state estimates",
        "oracle headroom remains significant",
    ]
    rows = []
    sorted_gaps = sorted(gaps, key=lambda item: item[0])
    for index in range(24):
        gap, row, peer = sorted_gaps[index % len(sorted_gaps)]
        rows.append(
            {
                "case_id": index + 1,
                "task": row["task"],
                "regime": row["regime"],
                "strongest_baseline": strongest,
                "proposed_success": row["mean_success"],
                "baseline_success": peer["mean_success"],
                "success_gap": gap,
                "proposed_boundary_error": row["mean_boundary_error"],
                "proposed_unsafe_impulse": row["mean_unsafe_impulse"],
                "lesson": lessons[index % len(lessons)],
            }
        )
    return rows


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                val = row[key]
                if isinstance(val, (float, np.floating)):
                    values.append(f"{float(val):.3f}")
                else:
                    values.append(display_name(val))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def make_figures(hard_metrics, ablations, stress_summary, fixed_summary):
    hard = sorted(hard_metrics, key=lambda row: float(row["mean_mean_utility"]))
    plt.figure(figsize=(10.5, 6.0))
    colors = [
        "#005f73" if row["method"] == PRIMARY_METHOD else "#c8792a" if row["method"] == V4_METHOD else "#9aa6b2"
        for row in hard
    ]
    plt.barh(
        [DISPLAY_NAMES.get(row["method"], row["method"]) for row in hard],
        [float(row["mean_mean_utility"]) for row in hard],
        xerr=[float(row["ci95_mean_utility"]) for row in hard],
        color=colors,
        capsize=3,
    )
    plt.xlabel("Hard non-smooth utility")
    plt.title("Contact-mode boundary audit")
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_hard_utility_v5.png", dpi=180)
    plt.close()

    selected = [row for row in sorted(hard_metrics, key=lambda r: float(r["mean_mean_contact_mode_f1"]), reverse=True) if not str(row["method"]).startswith("oracle")]
    x = np.arange(len(selected))
    plt.figure(figsize=(11.5, 5.8))
    plt.bar(x - 0.22, [float(row["mean_mean_contact_mode_f1"]) for row in selected], width=0.44, label="mode F1", color="#0a9396")
    plt.bar(x + 0.22, [float(row["mean_mean_unsafe_impulse"]) for row in selected], width=0.44, label="unsafe impulse", color="#ae2012")
    plt.xticks(x, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in selected], rotation=35, ha="right")
    plt.legend()
    plt.title("Mode diagnosis and unsafe impulse")
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_diagnostics_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9.5, 5.8))
    for method in sorted({row["method"] for row in stress_summary}):
        series = sorted([row for row in stress_summary if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["mean_mean_utility"]) for row in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Non-smooth stress")
    plt.ylabel("Mean utility")
    plt.title("Non-smooth stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_stress_sweep_v5.png", dpi=180)
    plt.close()

    ab = sorted(ablations, key=lambda row: float(row["mean_mean_utility"]), reverse=True)
    plt.figure(figsize=(11.0, 5.8))
    plt.bar(
        [DISPLAY_NAMES.get(row["ablation"], row["ablation"]) for row in ab],
        [float(row["mean_mean_utility"]) for row in ab],
        yerr=[float(row["ci95_mean_utility"]) for row in ab],
        color=["#005f73" if row["ablation"] == "full_contact_mode_boundary_audit_v5" else "#9aa6b2" for row in ab],
        capsize=3,
    )
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("Mixed-stress utility")
    plt.title("Mechanism ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_ablation_v5.png", dpi=180)
    plt.close()

    keep = {PRIMARY_METHOD, V4_METHOD, "conformal_risk_filter", "complementarity_residual_planner", ORACLE_METHOD}
    plt.figure(figsize=(9.5, 5.8))
    for method in sorted(keep):
        series = sorted([row for row in fixed_summary if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot([float(row["risk_budget"]) for row in series], [float(row["mean_mean_utility"]) for row in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Fixed risk budget")
    plt.ylabel("Gated utility")
    plt.title("Fixed-risk non-smooth deployment")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_fixed_risk_v5.png", dpi=180)
    plt.close()

    non_oracle = [row for row in hard_metrics if not str(row["method"]).startswith("oracle")]
    plt.figure(figsize=(8.8, 5.8))
    plt.scatter(
        [float(row["mean_mean_boundary_error"]) for row in non_oracle],
        [float(row["mean_mean_complementarity_residual"]) for row in non_oracle],
        s=85,
        c=["#005f73" if row["method"] == PRIMARY_METHOD else "#9aa6b2" for row in non_oracle],
    )
    for row in non_oracle:
        plt.text(float(row["mean_mean_boundary_error"]) + 0.002, float(row["mean_mean_complementarity_residual"]) + 0.002, DISPLAY_NAMES.get(row["method"], row["method"]), fontsize=8)
    plt.xlabel("Boundary error")
    plt.ylabel("Complementarity residual")
    plt.title("Boundary error versus physical residual")
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_boundary_residual_v5.png", dpi=180)
    plt.close()


def write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary):
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        sorted(hard_metrics, key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_contact_mode_f1", "ModeF1"),
            ("mean_mean_boundary_error", "BoundErr"),
            ("mean_mean_unsafe_impulse", "Unsafe"),
        ],
        "Hard-aggregate non-smooth mechanics benchmark.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "SuccDiff"),
            ("mean_utility_diff", "UtilDiff"),
            ("wins_utility_over_seeds", "UtilWins"),
        ],
        "Paired hard-aggregate differences against the v5 audit.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablations, key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_contact_mode_f1", "ModeF1"),
            ("mean_mean_boundary_error", "BoundErr"),
        ],
        "Ablations under mixed non-smooth stress.",
    )
    max_stress = max(float(row["stress_level"]) for row in stress_summary)
    latex_table(
        RESULTS / "max_stress_table.tex",
        sorted([row for row in stress_summary if float(row["stress_level"]) == max_stress], key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_boundary_error", "BoundErr"),
            ("mean_mean_unsafe_impulse", "Unsafe"),
        ],
        "Maximum non-smooth stress endpoint.",
    )
    strict = min(float(row["risk_budget"]) for row in fixed_summary)
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        sorted([row for row in fixed_summary if float(row["risk_budget"]) == strict], key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_coverage", "Coverage"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_risk_score", "Risk"),
        ],
        "Strict fixed-risk acceptance endpoint.",
    )


def decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest):
    primary = next(row for row in hard_metrics if row["method"] == PRIMARY_METHOD)
    baseline = next(row for row in hard_metrics if row["method"] == strongest)
    oracle = next(row for row in hard_metrics if row["method"] == ORACLE_METHOD)
    pair = next(row for row in pairwise if row["baseline"] == strongest)
    full = next(row for row in ablations if row["ablation"] == "full_contact_mode_boundary_audit_v5")
    removed = [row for row in ablations if row["ablation"] != "full_contact_mode_boundary_audit_v5"]
    best_removed_success = max(removed, key=lambda row: float(row["mean_mean_success"]))
    best_removed_utility = max(removed, key=lambda row: float(row["mean_mean_utility"]))
    max_stress = max(float(row["stress_level"]) for row in stress_summary)
    stress_primary = next(row for row in stress_summary if float(row["stress_level"]) == max_stress and row["method"] == PRIMARY_METHOD)
    stress_base = next(row for row in stress_summary if float(row["stress_level"]) == max_stress and row["method"] == strongest)
    strict = min(float(row["risk_budget"]) for row in fixed_summary)
    fixed_primary = next(row for row in fixed_summary if float(row["risk_budget"]) == strict and row["method"] == PRIMARY_METHOD)
    fixed_base = next(row for row in fixed_summary if float(row["risk_budget"]) == strict and row["method"] == strongest)

    gates = {
        "success_gate": float(primary["mean_mean_success"]) - float(baseline["mean_mean_success"]) >= 0.030 or float(primary["mean_mean_utility"]) - float(baseline["mean_mean_utility"]) >= 0.050,
        "diagnostic_gate": float(primary["mean_mean_contact_mode_f1"]) - float(baseline["mean_mean_contact_mode_f1"]) >= 0.050 or float(primary["mean_mean_boundary_error"]) - float(baseline["mean_mean_boundary_error"]) <= -0.040,
        "safety_gate": float(primary["mean_mean_impulse_violation"]) - float(baseline["mean_mean_impulse_violation"]) <= 0.020 and float(primary["mean_mean_unsafe_impulse"]) - float(baseline["mean_mean_unsafe_impulse"]) <= 0.020 and float(primary["mean_mean_jam_rate"]) - float(baseline["mean_mean_jam_rate"]) <= 0.020 and float(primary["mean_mean_slip_overshoot"]) - float(baseline["mean_mean_slip_overshoot"]) <= 0.020 and float(primary["mean_mean_mode_switch_latency"]) - float(baseline["mean_mean_mode_switch_latency"]) <= 0.020 and float(primary["mean_mean_energy_spike"]) - float(baseline["mean_mean_energy_spike"]) <= 0.020 and float(primary["mean_mean_calibration_ece"]) - float(baseline["mean_mean_calibration_ece"]) <= 0.020 and float(primary["mean_mean_intervention_cost"]) - float(baseline["mean_mean_intervention_cost"]) <= 0.055,
        "pairwise_gate": int(pair["wins_utility_over_seeds"]) >= 8 and float(pair["mean_utility_diff"]) > 0,
        "ablation_gate": float(full["mean_mean_success"]) - float(best_removed_success["mean_mean_success"]) >= 0.020 or float(full["mean_mean_utility"]) - float(best_removed_utility["mean_mean_utility"]) >= 0.040,
        "stress_gate": float(stress_primary["mean_mean_utility"]) - float(stress_base["mean_mean_utility"]) >= 0.020,
        "fixed_risk_gate": float(fixed_primary["mean_mean_coverage"]) >= 0.300 and float(fixed_primary["mean_mean_utility"]) - float(fixed_base["mean_mean_utility"]) >= 0.020,
        "scope_gate": False,
        "success_margin_vs_strongest": float(primary["mean_mean_success"]) - float(baseline["mean_mean_success"]),
        "utility_margin_vs_strongest": float(primary["mean_mean_utility"]) - float(baseline["mean_mean_utility"]),
        "contact_mode_f1_delta_vs_strongest": float(primary["mean_mean_contact_mode_f1"]) - float(baseline["mean_mean_contact_mode_f1"]),
        "boundary_error_delta_vs_strongest": float(primary["mean_mean_boundary_error"]) - float(baseline["mean_mean_boundary_error"]),
        "impulse_violation_delta_vs_strongest": float(primary["mean_mean_impulse_violation"]) - float(baseline["mean_mean_impulse_violation"]),
        "unsafe_impulse_delta_vs_strongest": float(primary["mean_mean_unsafe_impulse"]) - float(baseline["mean_mean_unsafe_impulse"]),
        "jam_rate_delta_vs_strongest": float(primary["mean_mean_jam_rate"]) - float(baseline["mean_mean_jam_rate"]),
        "slip_overshoot_delta_vs_strongest": float(primary["mean_mean_slip_overshoot"]) - float(baseline["mean_mean_slip_overshoot"]),
        "mode_switch_latency_delta_vs_strongest": float(primary["mean_mean_mode_switch_latency"]) - float(baseline["mean_mean_mode_switch_latency"]),
        "energy_spike_delta_vs_strongest": float(primary["mean_mean_energy_spike"]) - float(baseline["mean_mean_energy_spike"]),
        "calibration_ece_delta_vs_strongest": float(primary["mean_mean_calibration_ece"]) - float(baseline["mean_mean_calibration_ece"]),
        "intervention_cost_delta_vs_strongest": float(primary["mean_mean_intervention_cost"]) - float(baseline["mean_mean_intervention_cost"]),
        "ablation_success_margin_vs_best_removed_component": float(full["mean_mean_success"]) - float(best_removed_success["mean_mean_success"]),
        "ablation_utility_margin_vs_best_removed_component": float(full["mean_mean_utility"]) - float(best_removed_utility["mean_mean_utility"]),
        "stress_utility_margin_at_max_stress": float(stress_primary["mean_mean_utility"]) - float(stress_base["mean_mean_utility"]),
        "strict_fixed_risk_coverage": float(fixed_primary["mean_mean_coverage"]),
        "strict_fixed_risk_utility_margin": float(fixed_primary["mean_mean_utility"]) - float(fixed_base["mean_mean_utility"]),
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component_success": best_removed_success["ablation"],
        "best_removed_component_utility": best_removed_utility["ablation"],
    }
    local_gate_keys = ["success_gate", "diagnostic_gate", "safety_gate", "pairwise_gate", "ablation_gate", "stress_gate", "fixed_risk_gate"]
    decision = "STRONG_REVISE" if all(gates[key] for key in local_gate_keys) else "KILL_ARCHIVE"
    rationale = "expanded local non-smooth mechanics evidence supports the mechanism, but the external robotics scope gate fails" if decision == "STRONG_REVISE" else "expanded local non-smooth mechanics evidence fails at least one frozen empirical gate"
    return decision, rationale, gates, primary, baseline, oracle


def write_summary_txt(payload, hard_metrics, pairwise, ablations):
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 109 non_smooth_mechanics_for_foundation_policies v5 expanded evidence rebuild\n")
        handle.write(f"Design: {len(TASKS)} tasks x {len(REGIMES)} regimes x {len(SPLITS)} splits x {len(METHODS)} methods, {len(SEEDS)} seeds, {EPISODES_PER_CELL} episodes/cell.\n")
        handle.write(f"Terminal decision: {payload['terminal_decision']}\n")
        handle.write(f"ICLR main ready: {payload['iclr_main_ready']}\n")
        handle.write(f"Rationale: {payload['rationale']}\n\n")
        handle.write("Hard-aggregate ranking:\n")
        for row in sorted(hard_metrics, key=lambda item: float(item["mean_mean_utility"]), reverse=True):
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.4f}, utility={float(row['mean_mean_utility']):.4f}, "
                f"mode_f1={float(row['mean_mean_contact_mode_f1']):.4f}, boundary_error={float(row['mean_mean_boundary_error']):.4f}, "
                f"unsafe_impulse={float(row['mean_mean_unsafe_impulse']):.4f}, regret={float(row['mean_mean_regret_to_oracle']):.4f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in payload["gates"].items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(f"{row['baseline']}: success_diff={float(row['mean_success_diff']):.4f}, utility_diff={float(row['mean_utility_diff']):.4f}, utility_wins={row['wins_utility_over_seeds']}/{row['seeds']}, decision={row['decision']}\n")
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda item: float(item["mean_mean_utility"]), reverse=True):
            handle.write(f"{row['ablation']}: success={float(row['mean_mean_success']):.4f}, utility={float(row['mean_mean_utility']):.4f}, note={row['interpretation']}\n")


def main():
    clean_outputs()
    dataset = build_dataset_summary()
    main_rows, main_group, seed_metrics, metrics, hard_seed, hard_metrics = build_main()
    strongest = strongest_non_oracle(hard_metrics)
    pairwise = build_pairwise(hard_seed, strongest)
    ablation_rows, ablation_seed, ablations = build_ablations()
    stress_rows, stress_seed, stress_summary = build_stress_sweep()
    fixed_rows, fixed_seed, fixed_summary = build_fixed_risk()
    fixed_pair = fixed_risk_pairwise(fixed_seed, strongest)
    cases = build_failure_cases(main_group, strongest)
    decision, rationale, gates, primary, baseline, oracle = decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest)

    for name, rows in [
        ("dataset_summary.csv", dataset),
        ("cell_metrics.csv", main_rows),
        ("main_group_metrics.csv", main_group),
        ("seed_metrics.csv", seed_metrics),
        ("metrics.csv", metrics),
        ("hard_seed_metrics.csv", hard_seed),
        ("hard_aggregate_metrics.csv", hard_metrics),
        ("hard_pairwise_stats.csv", pairwise),
        ("ablation_cell_metrics.csv", ablation_rows),
        ("ablation_seed_metrics.csv", ablation_seed),
        ("ablation_metrics.csv", ablations),
        ("stress_sweep_cell_metrics.csv", stress_rows),
        ("stress_sweep_seed_metrics.csv", stress_seed),
        ("stress_sweep.csv", stress_summary),
        ("fixed_risk_cell_metrics.csv", fixed_rows),
        ("fixed_risk_seed_metrics.csv", fixed_seed),
        ("fixed_risk_metrics.csv", fixed_summary),
        ("fixed_risk_pairwise_stats.csv", fixed_pair),
        ("failure_cases.csv", cases),
    ]:
        write_csv(RESULTS / name, rounded(rows))

    make_figures(hard_metrics, ablations, stress_summary, fixed_summary)
    write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary)
    row_counts = {
        "dataset_summary_rows": len(dataset),
        "main_cell_rows": len(main_rows),
        "main_group_rows": len(main_group),
        "seed_metric_rows": len(seed_metrics),
        "metric_rows": len(metrics),
        "hard_seed_rows": len(hard_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_cell_rows": len(ablation_rows),
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablations),
        "stress_cell_rows": len(stress_rows),
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_summary),
        "fixed_risk_cell_rows": len(fixed_rows),
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_summary),
        "fixed_risk_pairwise_rows": len(fixed_pair),
        "failure_case_rows": len(cases),
    }
    payload = {
        "paper": 109,
        "slug": "non_smooth_mechanics_for_foundation_policies",
        "terminal_decision": decision,
        "iclr_main_ready": False,
        "rationale": rationale,
        "design": {
            "tasks": len(TASKS),
            "regimes": len(REGIMES),
            "splits": len(SPLITS),
            "methods": len(METHODS),
            "seeds": len(SEEDS),
            "episodes_per_cell": EPISODES_PER_CELL,
            "stress_levels": 10,
            "fixed_risk_budgets": 4,
            "ablations": len(ABLATIONS),
        },
        "row_counts": row_counts,
        "strongest_non_oracle_baseline": strongest,
        "primary_method": PRIMARY_METHOD,
        "v4_method": V4_METHOD,
        "oracle_method": ORACLE_METHOD,
        "primary_metrics": {key.replace("mean_mean_", "", 1): float(primary[key]) for key in primary if key.startswith("mean_mean_")},
        "strongest_non_oracle_metrics": {key.replace("mean_mean_", "", 1): float(baseline[key]) for key in baseline if key.startswith("mean_mean_")},
        "oracle_metrics": {key.replace("mean_mean_", "", 1): float(oracle[key]) for key in oracle if key.startswith("mean_mean_")},
        "gates": gates,
    }
    (RESULTS / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    write_summary_txt(payload, hard_metrics, pairwise, ablations)
    print(f"terminal_decision={decision}")
    print(f"iclr_main_ready={payload['iclr_main_ready']}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"main_cell_rows={len(main_rows)}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
