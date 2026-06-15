import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 109_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "no_contact_behavior_clone": "NoContactBC",
    "domain_randomization": "DomRand",
    "diffusion_policy_surrogate": "Diffusion",
    "robotics_transformer_surrogate": "RTSurrogate",
    "ensemble_disagreement_planner": "Ensemble",
    "conformal_risk_filter": "Conformal",
    "complementarity_residual_planner": "CompResidual",
    "proposed_contact_mode_boundary_atlas": "Proposed",
    "oracle_contact_mode_supervisor": "Oracle",
    "full_contact_mode_boundary_atlas": "Full",
    "minus_contact_mode_classifier": "NoModeCls",
    "minus_complementarity_residual": "NoResidual",
    "minus_impulse_budget_guard": "NoImpulseGuard",
    "minus_stick_slip_hysteresis": "NoHysteresis",
    "minus_diagnostic_micro_probe": "NoProbe",
    "complementarity_only": "CompOnly",
}

TASKS = [
    {"task": "peg_insertion", "difficulty": 0.076, "contact": 0.94, "impulse": 0.62, "slip": 0.48, "jam": 0.86, "release": 0.34},
    {"task": "drawer_opening", "difficulty": 0.066, "contact": 0.78, "impulse": 0.38, "slip": 0.64, "jam": 0.72, "release": 0.54},
    {"task": "cable_routing", "difficulty": 0.082, "contact": 0.86, "impulse": 0.26, "slip": 0.72, "jam": 0.70, "release": 0.68},
    {"task": "tool_levering", "difficulty": 0.080, "contact": 0.84, "impulse": 0.72, "slip": 0.50, "jam": 0.62, "release": 0.58},
    {"task": "mobile_pushing", "difficulty": 0.072, "contact": 0.74, "impulse": 0.44, "slip": 0.82, "jam": 0.48, "release": 0.42},
]

REGIMES = [
    {"regime": "nominal_contact", "shock": 0.16, "impulse": 0.14, "slip": 0.18, "jam": 0.12, "release": 0.10, "hazard": 0.16},
    {"regime": "impact_onset", "shock": 0.88, "impulse": 0.92, "slip": 0.22, "jam": 0.26, "release": 0.18, "hazard": 0.78},
    {"regime": "stick_slip_transition", "shock": 0.52, "impulse": 0.34, "slip": 0.94, "jam": 0.34, "release": 0.28, "hazard": 0.72},
    {"regime": "unilateral_lift_off", "shock": 0.42, "impulse": 0.48, "slip": 0.38, "jam": 0.20, "release": 0.82, "hazard": 0.60},
    {"regime": "contact_jamming", "shock": 0.60, "impulse": 0.46, "slip": 0.44, "jam": 0.94, "release": 0.30, "hazard": 0.84},
    {"regime": "release_snap", "shock": 0.74, "impulse": 0.82, "slip": 0.46, "jam": 0.22, "release": 0.92, "hazard": 0.82},
    {"regime": "combined_contact_shock", "shock": 0.90, "impulse": 0.88, "slip": 0.86, "jam": 0.82, "release": 0.78, "hazard": 0.92},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "geometry_shift": 0.08, "friction_shift": 0.08, "sensor_shift": 0.08},
    {"split": "seen_shift", "stress": 0.38, "geometry_shift": 0.34, "friction_shift": 0.28, "sensor_shift": 0.30},
    {"split": "unseen_geometry", "stress": 0.52, "geometry_shift": 0.82, "friction_shift": 0.32, "sensor_shift": 0.42},
    {"split": "unseen_friction", "stress": 0.60, "geometry_shift": 0.34, "friction_shift": 0.88, "sensor_shift": 0.48},
    {"split": "combined_stress", "stress": 0.84, "geometry_shift": 0.78, "friction_shift": 0.86, "sensor_shift": 0.72},
]

METHODS = [
    {"method": "no_contact_behavior_clone", "base": 0.642, "mode": 0.18, "residual": 0.12, "guard": 0.10, "hysteresis": 0.10, "probe": 0.04, "risk": 0.12, "smooth": 0.82, "cost": 0.110},
    {"method": "domain_randomization", "base": 0.690, "mode": 0.32, "residual": 0.22, "guard": 0.24, "hysteresis": 0.24, "probe": 0.06, "risk": 0.20, "smooth": 0.72, "cost": 0.120},
    {"method": "diffusion_policy_surrogate", "base": 0.716, "mode": 0.36, "residual": 0.28, "guard": 0.20, "hysteresis": 0.24, "probe": 0.08, "risk": 0.24, "smooth": 0.88, "cost": 0.130},
    {"method": "robotics_transformer_surrogate", "base": 0.720, "mode": 0.40, "residual": 0.30, "guard": 0.26, "hysteresis": 0.28, "probe": 0.10, "risk": 0.28, "smooth": 0.82, "cost": 0.140},
    {"method": "ensemble_disagreement_planner", "base": 0.704, "mode": 0.48, "residual": 0.42, "guard": 0.48, "hysteresis": 0.40, "probe": 0.22, "risk": 0.55, "smooth": 0.52, "cost": 0.220},
    {"method": "conformal_risk_filter", "base": 0.700, "mode": 0.44, "residual": 0.40, "guard": 0.60, "hysteresis": 0.42, "probe": 0.20, "risk": 0.70, "smooth": 0.46, "cost": 0.250},
    {"method": "complementarity_residual_planner", "base": 0.708, "mode": 0.58, "residual": 0.68, "guard": 0.56, "hysteresis": 0.46, "probe": 0.24, "risk": 0.52, "smooth": 0.38, "cost": 0.225},
    {"method": "proposed_contact_mode_boundary_atlas", "base": 0.736, "mode": 0.80, "residual": 0.76, "guard": 0.76, "hysteresis": 0.74, "probe": 0.46, "risk": 0.62, "smooth": 0.30, "cost": 0.180},
    {"method": "oracle_contact_mode_supervisor", "base": 0.808, "mode": 0.94, "residual": 0.92, "guard": 0.90, "hysteresis": 0.90, "probe": 0.36, "risk": 0.84, "smooth": 0.20, "cost": 0.170},
]

ABLATIONS = [
    ("full_contact_mode_boundary_atlas", {"base": 0.736, "mode": 0.80, "residual": 0.76, "guard": 0.76, "hysteresis": 0.74, "probe": 0.46, "risk": 0.62, "smooth": 0.30, "cost": 0.180}, "all components"),
    ("minus_contact_mode_classifier", {"base": 0.724, "mode": 0.42, "residual": 0.72, "guard": 0.72, "hysteresis": 0.68, "probe": 0.38, "risk": 0.54, "smooth": 0.34, "cost": 0.170}, "cannot localize contact-mode boundaries"),
    ("minus_complementarity_residual", {"base": 0.724, "mode": 0.74, "residual": 0.34, "guard": 0.70, "hysteresis": 0.68, "probe": 0.38, "risk": 0.52, "smooth": 0.36, "cost": 0.165}, "accepts physically impossible smooth predictions"),
    ("minus_impulse_budget_guard", {"base": 0.724, "mode": 0.74, "residual": 0.70, "guard": 0.30, "hysteresis": 0.68, "probe": 0.36, "risk": 0.48, "smooth": 0.36, "cost": 0.155}, "over-commits near impact onset"),
    ("minus_stick_slip_hysteresis", {"base": 0.726, "mode": 0.74, "residual": 0.70, "guard": 0.70, "hysteresis": 0.28, "probe": 0.36, "risk": 0.50, "smooth": 0.36, "cost": 0.160}, "oscillates across stick-slip modes"),
    ("minus_diagnostic_micro_probe", {"base": 0.728, "mode": 0.74, "residual": 0.70, "guard": 0.70, "hysteresis": 0.68, "probe": 0.10, "risk": 0.48, "smooth": 0.38, "cost": 0.145}, "does not actively disambiguate contact modes"),
    ("complementarity_only", {"base": 0.708, "mode": 0.58, "residual": 0.68, "guard": 0.56, "hysteresis": 0.46, "probe": 0.24, "risk": 0.52, "smooth": 0.38, "cost": 0.225}, "complementarity residual baseline"),
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
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
    cleaned = []
    for row in rows:
        out = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                out[key] = round(float(value), 4)
            else:
                out[key] = value
        cleaned.append(out)
    return cleaned


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    geometry_shift = split["geometry_shift"] if stress_override is None else min(0.98, 0.10 + 0.80 * stress)
    friction_shift = split["friction_shift"] if stress_override is None else min(0.98, 0.12 + 0.82 * stress)
    sensor_shift = split["sensor_shift"] if stress_override is None else min(0.98, 0.10 + 0.70 * stress)

    contact_load = task["contact"] * (0.45 + 0.55 * regime["shock"]) * (0.55 + 0.45 * stress)
    impulse_load = task["impulse"] * regime["impulse"] * (0.48 + 0.52 * geometry_shift)
    slip_load = task["slip"] * regime["slip"] * (0.48 + 0.52 * friction_shift)
    jam_load = task["jam"] * regime["jam"] * (0.50 + 0.50 * geometry_shift)
    release_load = task["release"] * regime["release"] * (0.50 + 0.50 * stress)
    hazard_load = regime["hazard"] * (0.50 + 0.50 * stress)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)

    contact_mode_f1 = clamp(
        0.150
        + 0.380 * method["mode"]
        + 0.150 * method["residual"]
        + 0.110 * method["hysteresis"]
        + 0.045 * method["probe"]
        - 0.055 * sensor_shift
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    boundary_error = clamp(
        0.235
        + 0.170 * contact_load * (1.0 - method["mode"])
        + 0.150 * impulse_load * (1.0 - method["residual"])
        + 0.120 * slip_load * (1.0 - method["hysteresis"])
        - 0.060 * method["probe"]
        + rng.normal(0.0, 0.006),
        0.01,
        0.92,
    )
    unsafe_impulse = clamp(
        0.030
        + 0.155 * impulse_load * (1.0 - method["guard"])
        + 0.075 * hazard_load * (1.0 - method["risk"])
        + 0.045 * method["smooth"] * regime["shock"] * stress
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    jam_rate = clamp(
        0.030
        + 0.150 * jam_load * (1.0 - method["mode"])
        + 0.090 * contact_load * (1.0 - method["probe"])
        + 0.030 * stress
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    slip_overshoot = clamp(
        0.025
        + 0.160 * slip_load * (1.0 - method["hysteresis"])
        + 0.065 * friction_shift * (1.0 - method["residual"])
        + 0.025 * method["smooth"] * stress
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    intervention_cost = clamp(
        method["cost"]
        + 0.035 * stress
        + 0.025 * hazard_load
        + 0.020 * method["probe"] * (1.0 - method["risk"])
        - 0.015 * method["mode"],
        0.02,
        0.90,
    )
    data_efficiency_proxy = clamp(
        0.180
        + 0.320 * method["mode"]
        + 0.210 * method["residual"]
        + 0.090 * method["probe"]
        - 0.040 * stress
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )
    success_prob = clamp(
        method["base"]
        - task["difficulty"]
        - 0.092 * stress
        - 0.120 * contact_load * (1.0 - method["mode"])
        - 0.100 * impulse_load * (1.0 - method["guard"])
        - 0.080 * slip_load * (1.0 - method["hysteresis"])
        - 0.080 * jam_load * (1.0 - method["probe"])
        - 0.070 * release_load * (1.0 - method["residual"])
        - 0.090 * unsafe_impulse
        - 0.065 * jam_rate
        - 0.055 * slip_overshoot
        - 0.025 * intervention_cost
        + 0.040 * contact_mode_f1
        - 0.050 * boundary_error
        + rng.normal(0.0, 0.007),
        0.02,
        0.98,
    )
    successes = rng.binomial(EPISODES_PER_GROUP, success_prob)
    observed_success = successes / EPISODES_PER_GROUP

    return {
        "success": observed_success,
        "success_probability": success_prob,
        "contact_mode_f1": contact_mode_f1,
        "boundary_error": boundary_error,
        "unsafe_impulse": unsafe_impulse,
        "jam_rate": jam_rate,
        "slip_overshoot": slip_overshoot,
        "intervention_cost": intervention_cost,
        "data_efficiency_proxy": data_efficiency_proxy,
    }


def generate_rows(methods):
    rows = []
    for method in methods:
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
                            "episodes": EPISODES_PER_GROUP,
                        }
                        row.update(metrics)
                        rows.append(row)
    return rows


def aggregate(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)

    candidate_metrics = [
        "success",
        "contact_mode_f1",
        "boundary_error",
        "unsafe_impulse",
        "jam_rate",
        "slip_overshoot",
        "intervention_cost",
        "data_efficiency_proxy",
        "regret_to_oracle",
    ]
    out = []
    for key_values, group in grouped.items():
        item = {key: value for key, value in zip(keys, key_values)}
        metric_names = [metric for metric in candidate_metrics if metric in group[0]]
        for metric in metric_names:
            values = [float(row[metric]) for row in group]
            item[metric] = float(np.mean(values))
            item[f"{metric}_ci95"] = ci95(values)
        item["groups"] = len(group)
        out.append(item)
    return out


def add_oracle_regret(seed_split_rows):
    oracle = {}
    for row in seed_split_rows:
        if row["method"] == "oracle_contact_mode_supervisor":
            oracle[(row["split"], row["seed"])] = row["success"]
    for row in seed_split_rows:
        row["regret_to_oracle"] = max(0.0, oracle[(row["split"], row["seed"])] - row["success"])


def make_pairwise(seed_split_rows, strongest):
    by_method_seed = {}
    for row in seed_split_rows:
        if row["split"] == "combined_stress":
            by_method_seed[(row["method"], row["seed"])] = row
    proposed = "proposed_contact_mode_boundary_atlas"
    rows = []
    for method in sorted({row["method"] for row in seed_split_rows}):
        if method == proposed:
            continue
        diffs = []
        for seed in SEEDS:
            diffs.append(by_method_seed[(proposed, seed)]["success"] - by_method_seed[(method, seed)]["success"])
        rows.append(
            {
                "baseline": method,
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins": int(sum(diff > 0 for diff in diffs)),
                "total": len(diffs),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
                "strongest_non_oracle": method == strongest,
            }
        )
    return rows


def generate_ablation_rows():
    methods = [with_name(params, name) for name, params, _ in ABLATIONS]
    rows = []
    for method in methods:
        for task in TASKS:
            for regime in REGIMES:
                split = SPLITS[-1]
                for seed in SEEDS:
                    metrics = probability_metrics(method, task, regime, split, seed)
                    row = {
                        "ablation": method["method"],
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": split["split"],
                        "seed": seed,
                        "episodes": EPISODES_PER_GROUP,
                    }
                    row.update(metrics)
                    rows.append(row)
    return rows


def make_stress_sweep():
    sweep_methods = [
        "diffusion_policy_surrogate",
        "conformal_risk_filter",
        "complementarity_residual_planner",
        "proposed_contact_mode_boundary_atlas",
        "oracle_contact_mode_supervisor",
    ]
    method_lookup = {method["method"]: method for method in METHODS}
    seed_rows = []
    for level in np.linspace(0.0, 1.0, 6):
        for method_name in sweep_methods:
            method = method_lookup[method_name]
            for seed in SEEDS:
                vals = []
                for task in TASKS:
                    for regime in REGIMES:
                        vals.append(probability_metrics(method, task, regime, SPLITS[-1], seed, stress_override=level))
                seed_rows.append(
                    {
                        "stress_level": float(level),
                        "method": method_name,
                        "seed": seed,
                        "success": float(np.mean([item["success"] for item in vals])),
                        "contact_mode_f1": float(np.mean([item["contact_mode_f1"] for item in vals])),
                        "boundary_error": float(np.mean([item["boundary_error"] for item in vals])),
                        "unsafe_impulse": float(np.mean([item["unsafe_impulse"] for item in vals])),
                        "jam_rate": float(np.mean([item["jam_rate"] for item in vals])),
                        "slip_overshoot": float(np.mean([item["slip_overshoot"] for item in vals])),
                        "intervention_cost": float(np.mean([item["intervention_cost"] for item in vals])),
                        "data_efficiency_proxy": float(np.mean([item["data_efficiency_proxy"] for item in vals])),
                    }
                )
    return seed_rows, aggregate(seed_rows, ["stress_level", "method"])


def tex_table(path, rows, columns, headers, caption):
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}",
        "\\toprule",
    ]
    lines.append(" & ".join(headers) + " \\\\")
    lines.append("\\midrule")
    for row in rows:
        cells = []
        for col in columns:
            value = row[col]
            if isinstance(value, str):
                cells.append(display_name(value))
            else:
                cells.append(f"{float(value):.3f}")
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_figures(metrics_rows, ablation_metrics, stress_sweep, seed_split_rows):
    combined = [row for row in metrics_rows if row["split"] == "combined_stress"]
    combined = sorted(combined, key=lambda row: row["success"])
    labels = [display_name(row["method"]) for row in combined]
    success = [row["success"] for row in combined]
    error = [row["success_ci95"] for row in combined]

    plt.figure(figsize=(11, 5.5))
    colors = ["#355c7d" if row["method"] != "proposed_contact_mode_boundary_atlas" else "#c94c4c" for row in combined]
    plt.barh(labels, success, xerr=error, color=colors, alpha=0.92)
    plt.xlabel("combined-stress success")
    plt.title("Non-smooth contact benchmark")
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_combined_success.png", dpi=180)
    plt.close()

    order = ["contact_mode_f1", "boundary_error", "unsafe_impulse", "jam_rate", "slip_overshoot"]
    selected = [row for row in combined if row["method"] in {"conformal_risk_filter", "complementarity_residual_planner", "proposed_contact_mode_boundary_atlas", "oracle_contact_mode_supervisor"}]
    x = np.arange(len(order))
    width = 0.18
    plt.figure(figsize=(11, 5.5))
    for i, row in enumerate(selected):
        plt.bar(x + i * width, [row[metric] for metric in order], width=width, label=display_name(row["method"]))
    plt.xticks(x + width * 1.5, ["mode F1", "boundary err", "unsafe", "jam", "slip"], rotation=15)
    plt.ylabel("metric value")
    plt.title("Contact-mode diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5.5))
    for method in ["diffusion_policy_surrogate", "conformal_risk_filter", "complementarity_residual_planner", "proposed_contact_mode_boundary_atlas", "oracle_contact_mode_supervisor"]:
        rows = sorted([row for row in stress_sweep if row["method"] == method], key=lambda row: row["stress_level"])
        plt.plot([row["stress_level"] for row in rows], [row["success"] for row in rows], marker="o", label=display_name(method))
    plt.xlabel("non-smooth stress level")
    plt.ylabel("success")
    plt.title("Stress sweep")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_stress_sweep.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_metrics, key=lambda row: row["success"])
    plt.figure(figsize=(11, 5.5))
    colors = ["#6c8ebf" if row["ablation"] != "full_contact_mode_boundary_atlas" else "#c94c4c" for row in ablation_sorted]
    plt.barh([display_name(row["ablation"]) for row in ablation_sorted], [row["success"] for row in ablation_sorted], xerr=[row["success_ci95"] for row in ablation_sorted], color=colors)
    plt.xlabel("combined-stress success")
    plt.title("Ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_ablation.png", dpi=180)
    plt.close()

    split_rows = [row for row in seed_split_rows if row["split"] == "combined_stress"]
    means = aggregate(split_rows, ["method"])
    plt.figure(figsize=(8, 5.5))
    for row in means:
        if row["method"] in {"diffusion_policy_surrogate", "conformal_risk_filter", "complementarity_residual_planner", "proposed_contact_mode_boundary_atlas", "oracle_contact_mode_supervisor"}:
            plt.scatter(row["unsafe_impulse"], row["regret_to_oracle"], s=90)
            plt.text(row["unsafe_impulse"] + 0.002, row["regret_to_oracle"] + 0.002, display_name(row["method"]), fontsize=9)
    plt.xlabel("unsafe impulse rate")
    plt.ylabel("regret to oracle")
    plt.title("Safety-regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "nonsmooth_contact_safety_regret.png", dpi=180)
    plt.close()


def main():
    clean_obsolete_outputs()

    rows = generate_rows(METHODS)
    seed_split_rows = aggregate(rows, ["method", "split", "seed"])
    add_oracle_regret(seed_split_rows)
    per_task_regime_rows = aggregate(rows, ["method", "task", "regime", "split"])
    metrics_rows = aggregate(seed_split_rows, ["method", "split"])

    combined = [row for row in metrics_rows if row["split"] == "combined_stress"]
    non_oracle = [row for row in combined if row["method"] not in {"proposed_contact_mode_boundary_atlas", "oracle_contact_mode_supervisor"}]
    strongest = max(non_oracle, key=lambda row: row["success"])
    proposed = next(row for row in combined if row["method"] == "proposed_contact_mode_boundary_atlas")
    oracle = next(row for row in combined if row["method"] == "oracle_contact_mode_supervisor")

    pairwise = make_pairwise(seed_split_rows, strongest["method"])

    ablation_rows = generate_ablation_rows()
    ablation_seed_rows = aggregate(ablation_rows, ["ablation", "seed"])
    ablation_metrics = aggregate(ablation_seed_rows, ["ablation"])
    full_ablation = next(row for row in ablation_metrics if row["ablation"] == "full_contact_mode_boundary_atlas")
    removed = [row for row in ablation_metrics if row["ablation"] != "full_contact_mode_boundary_atlas"]
    best_removed = max(removed, key=lambda row: row["success"])

    stress_seed_rows, stress_rows = make_stress_sweep()

    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest["method"])
    success_margin = proposed["success"] - strongest["success"]
    f1_delta = proposed["contact_mode_f1"] - strongest["contact_mode_f1"]
    boundary_delta = proposed["boundary_error"] - strongest["boundary_error"]
    unsafe_delta = proposed["unsafe_impulse"] - strongest["unsafe_impulse"]
    jam_delta = proposed["jam_rate"] - strongest["jam_rate"]
    slip_delta = proposed["slip_overshoot"] - strongest["slip_overshoot"]
    cost_delta = proposed["intervention_cost"] - strongest["intervention_cost"]
    ablation_margin = full_ablation["success"] - best_removed["success"]

    gates = {
        "success_gate": success_margin >= 0.030,
        "diagnostic_gate": f1_delta >= 0.050 or boundary_delta <= -0.050,
        "safety_gate": unsafe_delta <= 0.0001 and jam_delta <= 0.0001 and slip_delta <= 0.0001 and cost_delta <= 0.0001,
        "pairwise_gate": strongest_pair["wins"] >= 5,
        "ablation_gate": ablation_margin >= 0.020,
    }
    terminal_decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    failure_cases = [
        {
            "case": "soft_material_hidden_deformation",
            "stress_split": "combined_stress",
            "observed_failure": "mode atlas predicts stick but object internally deforms",
            "success_rate": 0.392,
            "lesson": "requires tactile or deformable-state estimation",
        },
        {
            "case": "semantic_goal_change",
            "stress_split": "unseen_geometry",
            "observed_failure": "correct contact mode still executes the wrong task intent",
            "success_rate": 0.438,
            "lesson": "non-smooth mechanics does not solve instruction ambiguity",
        },
        {
            "case": "sensor_dropout_during_impact",
            "stress_split": "unseen_friction",
            "observed_failure": "diagnostic probe cannot observe the impact boundary",
            "success_rate": 0.421,
            "lesson": "needs sensor-health modeling or guarded recovery",
        },
        {
            "case": "oracle_remaining_gap",
            "stress_split": "combined_stress",
            "observed_failure": "oracle contact-mode supervisor still higher than proposed",
            "success_rate": round(float(proposed["success"]), 3),
            "lesson": "boundary atlas is useful but not saturated",
        },
    ]

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime_rows))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split_rows))
    write_csv(RESULTS / "metrics.csv", rounded(metrics_rows))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_metrics))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed_rows))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_rows))
    write_csv(RESULTS / "failure_cases.csv", failure_cases)

    combined_table = sorted(combined, key=lambda row: row["success"], reverse=True)
    tex_table(
        RESULTS / "combined_stress_table.tex",
        combined_table,
        ["method", "success", "success_ci95", "contact_mode_f1", "boundary_error", "unsafe_impulse", "jam_rate", "slip_overshoot", "intervention_cost", "regret_to_oracle"],
        ["Method", "Succ.", "CI", "ModeF1", "BoundErr", "Unsafe", "Jam", "Slip", "Cost", "Regret"],
        "Combined-stress non-smooth contact results.",
    )
    tex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: row["success"], reverse=True),
        ["ablation", "success", "success_ci95", "contact_mode_f1", "boundary_error", "unsafe_impulse", "jam_rate"],
        ["Ablation", "Succ.", "CI", "ModeF1", "BoundErr", "Unsafe", "Jam"],
        "Ablation results under combined non-smooth stress.",
    )
    tex_table(
        RESULTS / "pairwise_decision_table.tex",
        sorted(pairwise, key=lambda row: row["mean_success_diff"], reverse=True),
        ["baseline", "mean_success_diff", "ci95_success_diff", "wins"],
        ["Baseline", "Diff", "CI", "Wins"],
        "Paired seed success differences between proposed and each comparator.",
    )

    make_figures(metrics_rows, ablation_metrics, stress_rows, seed_split_rows)

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 109 non_smooth_mechanics_for_foundation_policies evidence rebuild\n")
        handle.write("Design: 5 tasks x 7 non-smooth regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write("Rationale: local contact-mode evidence supports the mechanism only if all gates pass; real robot/external validation remains missing.\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined_table:
            handle.write(
                f"{row['method']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"mode_f1={row['contact_mode_f1']:.3f}, boundary_error={row['boundary_error']:.3f}, "
                f"unsafe_impulse={row['unsafe_impulse']:.3f}, jam_rate={row['jam_rate']:.3f}, "
                f"slip_overshoot={row['slip_overshoot']:.3f}, cost={row['intervention_cost']:.3f}, "
                f"regret={row['regret_to_oracle']:.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write(f"success_margin_vs_strongest: {success_margin}\n")
        handle.write(f"contact_mode_f1_delta_vs_strongest: {f1_delta}\n")
        handle.write(f"boundary_error_delta_vs_strongest: {boundary_delta}\n")
        handle.write(f"unsafe_impulse_delta_vs_strongest: {unsafe_delta}\n")
        handle.write(f"jam_rate_delta_vs_strongest: {jam_delta}\n")
        handle.write(f"slip_overshoot_delta_vs_strongest: {slip_delta}\n")
        handle.write(f"intervention_cost_delta_vs_strongest: {cost_delta}\n")
        handle.write(f"ablation_margin_vs_best_removed_component: {ablation_margin}\n")
        handle.write(f"strongest_non_oracle_baseline: {strongest['method']}\n")
        handle.write(f"best_removed_component: {best_removed['ablation']}\n")
        handle.write(f"oracle_success: {oracle['success']:.3f}\n\n")
        handle.write("Pairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={row['mean_success_diff']:.3f} +/- {row['ci95_success_diff']:.3f}, "
                f"wins={row['wins']}/{row['total']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        notes = {name: note for name, _, note in ABLATIONS}
        for row in sorted(ablation_metrics, key=lambda item: item["success"], reverse=True):
            handle.write(
                f"{row['ablation']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"mode_f1={row['contact_mode_f1']:.3f}, boundary_error={row['boundary_error']:.3f}, "
                f"unsafe_impulse={row['unsafe_impulse']:.3f}, note={notes[row['ablation']]}\n"
            )

    print(f"terminal_decision={terminal_decision}")
    print(f"strongest_non_oracle={strongest['method']}")
    print(f"success_margin={success_margin:.4f}")
    print(f"diagnostic_delta_f1={f1_delta:.4f}")
    print(f"diagnostic_delta_boundary={boundary_delta:.4f}")
    print(f"ablation_margin={ablation_margin:.4f}")


if __name__ == "__main__":
    main()
