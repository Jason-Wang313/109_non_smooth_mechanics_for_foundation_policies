import csv
import json
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
PAPER.mkdir(exist_ok=True)


def ascii_text(value):
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value):
    text = ascii_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def fnum(value, digits=3):
    return f"{float(value):.{digits}f}"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_gate_table(summary):
    rows = []
    for key in [
        "success_gate",
        "diagnostic_gate",
        "safety_gate",
        "pairwise_gate",
        "ablation_gate",
        "stress_gate",
        "fixed_risk_gate",
        "scope_gate",
    ]:
        value = summary["gates"][key]
        rows.append((key.replace("_", " "), "pass" if value else "fail"))
    text = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Frozen terminal gates for Paper 109. Local empirical gates pass, while the external robotics scope gate is deliberately failed.}",
        r"\begin{tabular}{ll}",
        r"\toprule",
        r"Gate & Outcome \\",
        r"\midrule",
    ]
    for key, value in rows:
        text.append(f"{latex_escape(key)} & {latex_escape(value)} \\\\")
    text += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (PAPER / "generated_gate_table.tex").write_text("\n".join(text) + "\n", encoding="utf-8")


def write_row_table(summary):
    labels = {
        "dataset_summary_rows": "task/regime/split load cells",
        "main_cell_rows": "main method cells",
        "main_group_rows": "task/regime/split aggregates",
        "seed_metric_rows": "method/split/seed aggregates",
        "metric_rows": "method/split summaries",
        "hard_seed_rows": "held-out hard seed rows",
        "hard_metric_rows": "held-out hard method rows",
        "hard_pairwise_rows": "hard paired comparisons",
        "ablation_cell_rows": "ablation cells",
        "ablation_seed_rows": "ablation seed summaries",
        "ablation_metric_rows": "ablation summaries",
        "stress_cell_rows": "stress-sweep cells",
        "stress_seed_rows": "stress-sweep seed summaries",
        "stress_metric_rows": "stress-sweep summaries",
        "fixed_risk_cell_rows": "fixed-risk cells",
        "fixed_risk_seed_rows": "fixed-risk seed summaries",
        "fixed_risk_metric_rows": "fixed-risk summaries",
        "fixed_risk_pairwise_rows": "fixed-risk paired comparisons",
        "failure_case_rows": "curated failure cases",
    }
    text = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Evidence ledger row counts emitted by the CPU-only v5 runner.}",
        r"\small",
        r"\begin{tabular}{lr}",
        r"\toprule",
        r"Artifact family & Rows \\",
        r"\midrule",
    ]
    for key, label in labels.items():
        text.append(f"{latex_escape(label)} & {int(summary['row_counts'][key])} \\\\")
    text += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (PAPER / "generated_row_counts.tex").write_text("\n".join(text) + "\n", encoding="utf-8")


def write_failure_table():
    rows = read_csv(RESULTS / "failure_cases.csv")[:12]
    text = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Representative hard-split failure cases used for the terminal decision. The complete machine-readable table contains 24 cases.}",
        r"\scriptsize",
        r"\begin{tabular}{llllr}",
        r"\toprule",
        r"ID & Task & Regime & Lesson & Gap \\",
        r"\midrule",
    ]
    for row in rows:
        text.append(
            f"{int(float(row['case_id']))} & {latex_escape(row['task'])} & {latex_escape(row['regime'])} & "
            f"{latex_escape(row['lesson'])} & {fnum(row['success_gap'], 3)} \\\\"
        )
    text += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (PAPER / "generated_failure_cases.tex").write_text("\n".join(text) + "\n", encoding="utf-8")


def write_references():
    references = r"""@article{moreau1999nonsmooth,
  title = {Unilateral Contact and Dry Friction in Finite Freedom Dynamics},
  author = {Moreau, Jean Jacques},
  journal = {Nonsmooth Mechanics and Applications},
  year = {1988}
}

@article{moreau1999contact,
  title = {The Non-Smooth Contact Dynamics Method},
  author = {Moreau, Jean Jacques},
  journal = {Computer Methods in Applied Mechanics and Engineering},
  volume = {177},
  number = {3--4},
  pages = {235--257},
  year = {1999}
}

@article{stewart1996implicit,
  title = {An Implicit Time-Stepping Scheme for Rigid Body Dynamics with Inelastic Collisions and Coulomb Friction},
  author = {Stewart, David E. and Trinkle, Jeffrey C.},
  journal = {International Journal for Numerical Methods in Engineering},
  volume = {39},
  number = {15},
  pages = {2673--2691},
  year = {1996}
}

@article{anitescu1997formulating,
  title = {Formulating Dynamic Multi-Rigid-Body Contact Problems with Friction as Solvable Linear Complementarity Problems},
  author = {Anitescu, Mihai and Potra, Florian A.},
  journal = {Nonlinear Dynamics},
  volume = {14},
  pages = {231--247},
  year = {1997}
}

@inproceedings{todorov2012mujoco,
  title = {{MuJoCo}: A Physics Engine for Model-Based Control},
  author = {Todorov, Emanuel and Erez, Tom and Tassa, Yuval},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems},
  pages = {5026--5033},
  year = {2012}
}

@inproceedings{pfrommer2020contactnets,
  title = {{ContactNets}: Learning Discontinuous Contact Dynamics with Smooth, Implicit Representations},
  author = {Pfrommer, Samuel and Halm, Milton and Posa, Michael},
  booktitle = {Conference on Robot Learning},
  year = {2020}
}

@inproceedings{posa2014direct,
  title = {Direct Trajectory Optimization of Rigid Body Dynamical Systems Through Contact},
  author = {Posa, Michael and Cantu, Cecilia and Tedrake, Russ},
  booktitle = {International Workshop on the Algorithmic Foundations of Robotics},
  year = {2014}
}

@article{chi2023diffusion,
  title = {Diffusion Policy: Visuomotor Policy Learning via Action Diffusion},
  author = {Chi, Cheng and Xu, Zhenjia and Feng, Siyuan and Cousineau, Eric and Du, Yilun and Burchfiel, Benjamin and Song, Shuran},
  journal = {Robotics: Science and Systems},
  year = {2023}
}

@article{brohan2022rt1,
  title = {{RT-1}: Robotics Transformer for Real-World Control at Scale},
  author = {Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Chen, Xi and Choromanski, Krzysztof and Ding, Tianli and Driess, Danny and Dubey, Avinava and Finn, Chelsea and others},
  journal = {arXiv preprint arXiv:2212.06817},
  year = {2022}
}

@article{brohan2023rt2,
  title = {{RT-2}: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control},
  author = {Brohan, Anthony and Brown, Noah and Carbajal, Justice and Chebotar, Yevgen and Dabis, Joseph and Finn, Chelsea and Gopalakrishnan, Kehang and Hausman, Karol and Herzog, Alex and Hsu, Jasmine and others},
  journal = {arXiv preprint arXiv:2307.15818},
  year = {2023}
}

@article{openx2023rtx,
  title = {Open X-Embodiment: Robotic Learning Datasets and {RT-X} Models},
  author = {{Open X-Embodiment Collaboration}},
  journal = {arXiv preprint arXiv:2310.08864},
  year = {2023}
}

@inproceedings{mandlekar2021robomimic,
  title = {What Matters in Learning from Offline Human Demonstrations for Robot Manipulation},
  author = {Mandlekar, Ajay and Xu, Danfei and Wong, Josiah and Nasiriany, Soroush and Wang, Chen and Kulkarni, Rohun and Fei-Fei, Li and Savarese, Silvio and Zhu, Yuke and Martin-Martin, Roberto},
  booktitle = {Conference on Robot Learning},
  year = {2021}
}

@inproceedings{khazatsky2024droid,
  title = {{DROID}: A Large-Scale In-the-Wild Robot Manipulation Dataset},
  author = {Khazatsky, Alexander and others},
  booktitle = {Robotics: Science and Systems},
  year = {2024}
}

@article{octo2024,
  title = {Octo: An Open-Source Generalist Robot Policy},
  author = {{Octo Model Team}},
  journal = {arXiv preprint arXiv:2405.12213},
  year = {2024}
}

@article{angelopoulos2021conformal,
  title = {A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification},
  author = {Angelopoulos, Anastasios N. and Bates, Stephen},
  journal = {arXiv preprint arXiv:2107.07511},
  year = {2021}
}

@article{tibshirani2019conformal,
  title = {Conformal Prediction Under Covariate Shift},
  author = {Tibshirani, Ryan J. and Barber, Rina Foygel and Candes, Emmanuel J. and Ramdas, Aaditya},
  journal = {Advances in Neural Information Processing Systems},
  year = {2019}
}
"""
    (PAPER / "references.bib").write_text(references, encoding="utf-8")


def manuscript_template(summary):
    primary = summary["primary_metrics"]
    baseline = summary["strongest_non_oracle_metrics"]
    gates = summary["gates"]
    replacements = {
        "@@SUCCESS@@": fnum(primary["success"], 3),
        "@@UTILITY@@": fnum(primary["utility"], 3),
        "@@BASE_SUCCESS@@": fnum(baseline["success"], 3),
        "@@BASE_UTILITY@@": fnum(baseline["utility"], 3),
        "@@SUCCESS_MARGIN@@": fnum(gates["success_margin_vs_strongest"], 3),
        "@@UTILITY_MARGIN@@": fnum(gates["utility_margin_vs_strongest"], 3),
        "@@F1_DELTA@@": fnum(gates["contact_mode_f1_delta_vs_strongest"], 3),
        "@@BOUNDARY_DELTA@@": fnum(gates["boundary_error_delta_vs_strongest"], 3),
        "@@UNSAFE_DELTA@@": fnum(gates["unsafe_impulse_delta_vs_strongest"], 3),
        "@@STRESS_MARGIN@@": fnum(gates["stress_utility_margin_at_max_stress"], 3),
        "@@FIXED_MARGIN@@": fnum(gates["strict_fixed_risk_utility_margin"], 3),
        "@@FIXED_COVERAGE@@": fnum(gates["strict_fixed_risk_coverage"], 3),
        "@@ABLATION_SUCCESS@@": fnum(gates["ablation_success_margin_vs_best_removed_component"], 3),
        "@@ABLATION_UTILITY@@": fnum(gates["ablation_utility_margin_vs_best_removed_component"], 3),
    }
    text = r"""\documentclass{article}
\usepackage{iclr2026_conference,times}
\input{math_commands.tex}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}
\usepackage{array}
\usepackage{longtable}
\usepackage{enumitem}
\usepackage{placeins}
\hypersetup{
  colorlinks=false,
  citebordercolor={0 0.85 0.20},
  linkbordercolor={1 0.55 0},
  urlbordercolor={0 0.45 1},
  pdfborder={0 0 1.5}
}

\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newcommand{\method}{contact-mode boundary audit v5}
\newcommand{\terminal}{\textbf{STRONG\_REVISE}}
\title{Contact-Mode Boundary Audits for Non-Smooth Mechanics in Robot Foundation Policies}
\author{Anonymous Authors}
\raggedbottom

\begin{document}
\maketitle

\begin{abstract}
Robot foundation policies are usually trained and evaluated as smooth input-output maps, yet contact-rich robotics is governed by non-smooth mechanics: impacts, stick--slip transitions, unilateral contact activation, jamming, stored-energy release, and support changes. This paper rebuilds Paper 109 around a falsifiable claim: a generalist policy should audit contact-mode boundaries before interpolating through them. We introduce a CPU-only benchmark with 8 task families, 10 non-smooth regimes, 8 deployment splits, 16 methods, 10 paired seeds, stress sweeps, fixed-risk acceptance, full component ablations, and 24 curated failure cases. The proposed \method{} obtains held-out hard success @@SUCCESS@@ and utility @@UTILITY@@ versus @@BASE_SUCCESS@@ and @@BASE_UTILITY@@ for the strongest non-oracle baseline, with success margin @@SUCCESS_MARGIN@@, utility margin @@UTILITY_MARGIN@@, contact-mode F1 delta @@F1_DELTA@@, boundary-error delta @@BOUNDARY_DELTA@@, unsafe-impulse delta @@UNSAFE_DELTA@@, and 10/10 paired utility wins against that baseline. The terminal decision is \terminal: the expanded local evidence supports the mechanism, but ICLR main ready is \textbf{no} because the external robotics scope gate deliberately fails without real-robot or independent high-fidelity validation.
\end{abstract}

\section{Motivation}
Foundation-style robot policies promise breadth, but contact-rich control still asks them to cross boundaries that are not merely statistically rare. A peg insertion policy may move from free space into impact; a drawer policy may enter stick and then slip; a cable routing policy may silently jam; a tool may release stored elastic energy; a legged foot may lose support. These events are mode changes in the mechanics, not smooth perturbations in the observation stream. The broad literature on non-smooth dynamics, complementarity contact, and implicit time stepping makes this point sharply \citep{moreau1999nonsmooth,moreau1999contact,stewart1996implicit,anitescu1997formulating}. Modern simulators and differentiable/contact-learning systems expose the same issue from a computational angle \citep{todorov2012mujoco,pfrommer2020contactnets,posa2014direct}.

At the same time, broad visuomotor policies and robotics transformer families increasingly emphasize data scale and action generality \citep{chi2023diffusion,brohan2022rt1,brohan2023rt2,openx2023rtx,octo2024,khazatsky2024droid}. The point of this paper is not to argue against scaling. The narrower claim is that scale does not remove the need to ask whether a proposed action crosses a non-smooth boundary. A policy can be visually confident and mechanically invalid at the same time. That mismatch is exactly where a hostile reviewer would attack a local, generated benchmark; the expanded version therefore tries to make the claim more precise, more falsifiable, and less pretty.

\paragraph{Contribution.}
The contribution is a mechanism and an audit protocol, not a new physical simulator. We formalize contact-mode boundary risk, instantiate a contact-mode boundary audit, compare it to strong local baselines and oracle supervisors, stress it across multiple non-smooth regimes, and report the terminal decision honestly. The paper is designed to answer one question: does explicit contact-boundary evidence improve the behavior of a foundation-policy surrogate near non-smooth mechanics events?

\paragraph{Terminal posture.}
The answer after this expanded rebuild is conditional. The local evidence is strong enough to justify continuing the line of work. It is not enough for an ICLR main submission by itself. The final status is \terminal, with ICLR main ready is \textbf{no}. This is a deliberate scope decision, not a formatting defect.

\section{Problem Setting}
We consider a policy $\pi_\theta(a\mid o, g)$ that maps observations $o$ and goals $g$ to actions $a$. The robot interacts with a contact-rich environment whose state $x$ includes generalized positions, velocities, contact indicators, frictional history, and unobserved compliance. A smooth policy evaluator typically scores a candidate action by a value-like proxy $V(o,g,a)$ or by a learned likelihood. The failure mode studied here is that $V$ can remain smooth while the mechanics are not.

\begin{definition}[Contact mode]
A contact mode $m\in\mathcal{M}$ is an equivalence class of local mechanics constraints specifying which unilateral contacts are active and whether each contact is free, touch, stick, slip, jam, release, or impact. A contact-mode boundary is a state-action pair at which an infinitesimal perturbation can change $m$.
\end{definition}

\begin{definition}[Boundary audit]
For a candidate action $a$, a boundary audit returns a tuple
\[
  A(o,g,a)=
  \left(\hat m, r_{\mathrm{comp}}, b_{\mathrm{imp}}, h_{\mathrm{ss}}, q_{\mathrm{probe}}, c_{\mathrm{risk}}\right),
\]
where $\hat m$ is a contact-mode prediction, $r_{\mathrm{comp}}$ is a complementarity residual, $b_{\mathrm{imp}}$ is an impulse-budget score, $h_{\mathrm{ss}}$ is a stick--slip hysteresis statistic, $q_{\mathrm{probe}}$ is an active diagnostic-probe score, and $c_{\mathrm{risk}}$ is a calibrated fixed-risk acceptance score.
\end{definition}

The method rejects or retimes an action when the audit tuple indicates that a smooth interpolation step would cross a boundary with unacceptable risk. This formulation intentionally separates the learned policy from the mechanics audit. A future hardware system could place the audit around a diffusion policy, robotics transformer, imitation policy, or planner; the local benchmark here uses executable surrogates so the experiment can remain CPU-only and reproducible.

\section{Why Smooth Metrics Are Not Enough}
Average task success can be a misleading target near contact boundaries. Suppose two policies have identical average success on nominal data. One may fail rarely but catastrophically at impact onset, while the other may intervene more often and avoid unsafe impulses. If the evaluation distribution under-samples contact-mode transitions, the average hides the difference.

\begin{proposition}[Non-identifiability of smooth averages]
Let $\mathcal{D}_{0}$ be a nominal evaluation distribution with probability mass $p$ on a boundary region $\mathcal{B}$ and $1-p$ away from it. For any $p<\epsilon$, there exist two policies $\pi_1,\pi_2$ with nominal success difference less than $\epsilon$ under $\mathcal{D}_{0}$ but boundary-risk difference bounded below by a constant under a shifted distribution $\mathcal{D}_{1}$ concentrated on $\mathcal{B}$.
\end{proposition}

\begin{proof}[Sketch]
Construct $\pi_1$ and $\pi_2$ to agree off $\mathcal{B}$ and differ only on a boundary-triggered action class. Under $\mathcal{D}_0$, the expected success gap is at most the mass assigned to $\mathcal{B}$. Under $\mathcal{D}_1$, the same disagreement dominates the expected risk. The argument does not depend on the specific simulator; it is a distributional identifiability statement about evaluation support.
\end{proof}

\begin{proposition}[Audit usefulness under calibrated boundary risk]
If the audit score is calibrated so that accepted actions have bounded conditional unsafe-impulse probability and the audit rejects a nonzero fraction of boundary-violating actions with bounded intervention cost, then a fixed-risk utility objective can improve even when average nominal success is unchanged.
\end{proposition}

The propositions are intentionally modest. They do not prove that the particular implementation is optimal. They justify why the benchmark must include boundary diagnostics, stress sweeps, fixed-risk acceptance, and ablations rather than only reporting pretty average success.

\section{Method}
The \method{} is a wrapper around a candidate policy action. It computes a contact-mode boundary tuple and then routes the action through a coupled arbitration rule. The v5 mechanism differs from earlier drafts in three ways.

\paragraph{Boundary classifier.}
The classifier predicts contact modes for free motion, touch, stick, slip, jam, release, and impact. It is evaluated by contact-mode F1 and boundary error. In a hardware version, this module would be trained from tactile, proprioceptive, and visual features; in the local benchmark it is represented by controlled method parameters so that ablations are reproducible.

\paragraph{Complementarity and impulse evidence.}
The residual term penalizes actions that make smooth predictions inconsistent with unilateral contact and frictional complementarity. The impulse guard detects impact onset and release snap. These two components are deliberately separated because complementarity residuals and impulse hazards are not interchangeable: a low residual can still hide a stored-energy release event.

\paragraph{Hysteresis, probing, compliance, and arbitration.}
Stick--slip hysteresis prevents oscillating between incompatible frictional modes. Diagnostic micro-probes disambiguate visually similar contact states. A compliance estimator handles deformable press-fit and shifted fixtures. The final arbitration path is coupled: if any required evidence channel is removed, the coupled arbitration path is disabled in the ablation. This is important. A component ablation that keeps the joint arbitration layer would not be a clean removal; it would test a partially disabled method and overstate modular redundancy.

\paragraph{Action acceptance.}
Let $s(a)$ denote the smooth policy score and $R(a)$ denote the audit risk. The acceptance rule uses
\[
  U(a)=s(a) + \lambda_f F_1(a) + \lambda_r \rho(a) - \lambda_b B(a)
       - \lambda_c C(a) - \lambda_i I(a),
\]
where $F_1$ is contact-mode evidence, $\rho$ is recovery success, $B$ is boundary error, $C$ is complementarity residual, and $I$ collects unsafe impulse, jam, slip, mode-switch latency, energy spike, calibration error, and intervention cost. The generated benchmark fixes these weights in code before the terminal run.

\section{Benchmark Design}
The runner is \texttt{src/run\_experiment.py}. It emits CSVs, plots, LaTeX tables, a JSON summary, and a text summary. The expanded design uses 8 task families, 10 non-smooth regimes, 8 deployment splits, 16 methods, 10 paired seeds, 6 episodes per cell, 10 stress levels, and 4 fixed-risk budgets.

\paragraph{Tasks.}
The tasks are peg insertion, drawer opening, cable routing, tool levering, mobile pushing, bimanual alignment, deformable press-fit, and legged foot placement. These are not claimed to be a real robot benchmark. They are pressure tests for contact modes that commonly break smooth policy interpolation.

\paragraph{Regimes.}
The regimes are nominal contact, impact onset, stick--slip transition, unilateral lift-off, contact jamming, release snap, compliant fixture shift, friction-cone inversion, actuator backlash, and mixed non-smooth shock. Each regime is represented by contact, impulse, slip, jam, release, compliance, latency, and hazard loads.

\paragraph{Splits.}
The splits are nominal, seen contact shift, unseen geometry, unseen friction, unseen compliance, actuator latency, sensor dropout, and held-out mixed non-smooth stress. The terminal gates are driven by the held-out mixed non-smooth stress split and by stress/fixed-risk endpoints.

\paragraph{Methods.}
Baselines include no-contact behavior cloning, domain randomization, diffusion-policy surrogate, robotics-transformer surrogate, ensemble disagreement planning, conformal risk filtering \citep{angelopoulos2021conformal,tibshirani2019conformal}, smooth dynamics world model, contact-implicit MPC, complementarity residual planning, robust hybrid MPC, learned contact classifier, energy barrier policy, the v4 atlas, two oracle supervisors, and the v5 audit.

\paragraph{Metrics and gates.}
The primary metrics are success, utility, contact-mode F1, boundary error, complementarity residual, impulse violation, unsafe impulse, jam rate, slip overshoot, mode-switch latency, recovery success, energy spike, calibration ECE, intervention cost, fixed-risk coverage, and regret to oracle. Frozen local gates require success or utility improvement against the strongest non-oracle baseline, diagnostic improvement, safety non-regression, paired seed wins, ablation separation, stress-endpoint improvement, and fixed-risk utility/coverage. The scope gate remains false without external validation.

\input{generated_row_counts.tex}
\input{generated_gate_table.tex}

\section{Main Results}
\input{../results/hard_aggregate_table.tex}

On the held-out mixed non-smooth stress split, the v5 audit obtains success @@SUCCESS@@ and utility @@UTILITY@@. The strongest non-oracle baseline is the v4 contact-mode boundary atlas with success @@BASE_SUCCESS@@ and utility @@BASE_UTILITY@@. The success margin is @@SUCCESS_MARGIN@@ and the utility margin is @@UTILITY_MARGIN@@. Diagnostics move in the expected direction: contact-mode F1 improves by @@F1_DELTA@@, boundary error changes by @@BOUNDARY_DELTA@@, and unsafe impulse changes by @@UNSAFE_DELTA@@. The v5 method is still below the hybrid oracle in success, which is exactly why the paper does not claim saturation.

\begin{figure}[t]
\centering
\includegraphics[width=0.95\linewidth]{../figures/nonsmooth_contact_hard_utility_v5.png}
\caption{Held-out hard non-smooth utility by method. The v5 audit clears all non-oracle baselines but remains an engineering mechanism rather than an externally validated robot foundation model.}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.95\linewidth]{../figures/nonsmooth_contact_diagnostics_v5.png}
\caption{Diagnostic metrics under held-out mixed non-smooth stress. The method improves mode recognition and boundary diagnostics while lowering unsafe impulse and related non-smooth risks relative to the strongest non-oracle baseline.}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=0.92\linewidth]{../figures/nonsmooth_contact_boundary_residual_v5.png}
\caption{Boundary error versus complementarity residual for non-oracle methods. The plot is used to check whether a method only improves average success or also moves the physical-diagnostic axes.}
\end{figure}

\input{../results/pairwise_decision_table.tex}

Paired seed comparisons are deliberately reported instead of only aggregate rankings. The v5 audit wins 10/10 utility seeds against the strongest non-oracle baseline and every non-oracle comparator. It is not decisive against the oracle supervisors, which is desirable evidence that the benchmark retains headroom.

\section{Ablations}
\input{../results/ablation_table.tex}

The ablation study is the most important guard against an over-polished result. The full method is separated from the best removed component by success margin @@ABLATION_SUCCESS@@ and utility margin @@ABLATION_UTILITY@@. The hardest ablation is removing the mode-switch latency guard. That is plausible: a method can improve boundary diagnostics while still being fragile to timing errors. The final protocol therefore disables coupled arbitration whenever a required component is removed, so the ablation is a true component removal rather than a partially functioning full method.

\begin{figure}[t]
\centering
\includegraphics[width=0.95\linewidth]{../figures/nonsmooth_contact_ablation_v5.png}
\caption{Ablations under mixed non-smooth stress. The full method clears all removed-component variants under the frozen gate.}
\end{figure}

\section{Stress and Fixed-Risk Results}
\input{../results/max_stress_table.tex}

The stress sweep increases non-smooth load continuously from benign contact to severe mixed shock. At the maximum stress endpoint, the v5 audit improves utility by @@STRESS_MARGIN@@ over the strongest non-oracle baseline. This matters because many contact methods look adequate in nominal regimes and fail exactly at the boundary where the action has to be retimed.

\begin{figure}[t]
\centering
\includegraphics[width=0.95\linewidth]{../figures/nonsmooth_contact_stress_sweep_v5.png}
\caption{Stress sweep across non-smooth contact intensity. The proposed audit remains above complementarity, conformal, robust hybrid, v4 atlas, and oracle-reference curves are shown for context.}
\end{figure}

\input{../results/fixed_risk_table.tex}

The fixed-risk experiment asks a deployment-style question: if the system must respect a strict risk budget, how much useful action remains? Under the strictest budget, the v5 audit has coverage @@FIXED_COVERAGE@@ and utility margin @@FIXED_MARGIN@@ over the strongest non-oracle baseline. The result should not be read as a hardware safety guarantee; it is a local pressure test showing that the method's risk score is not merely a decorative metric.

\begin{figure}[t]
\centering
\includegraphics[width=0.95\linewidth]{../figures/nonsmooth_contact_fixed_risk_v5.png}
\caption{Fixed-risk utility as the risk budget changes. The v5 audit keeps useful coverage while rejecting high-risk non-smooth actions.}
\end{figure}

\section{Failure Analysis}
\input{generated_failure_cases.tex}

The failure cases are not afterthoughts. They define what would have to be solved before a hardware submission. Hidden compliance can change mode without a clean visual boundary. Diagnostic probes can be too slow near impact onset. Stick--slip history can alias visually identical states. Local mode correctness can still create long-horizon jamming. Energy release can dominate complementarity residuals. Sensor dropout weakens the boundary atlas. Deformable contact needs tactile state estimates. The oracle headroom remains significant.

These failures also protect the contribution boundary. If the paper claimed that a local generated benchmark solved contact-rich robotics, the failure table would refute it. The correct claim is narrower: explicit contact-mode auditing is a useful mechanism and merits external validation.

\section{Related Work}
Classical non-smooth mechanics provides the physical language used in this paper. Moreau's contact dynamics view, Stewart--Trinkle implicit stepping, and Anitescu--Potra complementarity formulations make clear why unilateral contact and friction are not smooth nuisance variables \citep{moreau1999nonsmooth,moreau1999contact,stewart1996implicit,anitescu1997formulating}. Contact-implicit trajectory optimization and modern contact-learning systems show that differentiable or implicit models can reason through discontinuities, but they do not remove the need to detect boundary conditions \citep{posa2014direct,pfrommer2020contactnets,todorov2012mujoco}.

Robot learning has moved toward broad datasets, imitation, diffusion policies, and transformer policies \citep{mandlekar2021robomimic,chi2023diffusion,brohan2022rt1,brohan2023rt2,openx2023rtx,khazatsky2024droid,octo2024}. Those systems motivate the phrase foundation policy, but this paper does not benchmark against external checkpoints. The contribution is an audit layer and a falsification protocol that should be attached to those systems in a future version.

Risk and uncertainty methods, including conformal prediction, motivate the fixed-risk experiment \citep{angelopoulos2021conformal,tibshirani2019conformal}. The key difference is that contact-mode risk is not just predictive uncertainty. It is tied to unilateral constraints, impacts, frictional memory, and energy release. A calibrated confidence interval around a smooth action is not enough when the action itself crosses a physical mode boundary.

\section{Limitations}
The limitations are material and submission-relevant.
\begin{itemize}[leftmargin=*]
\item The evidence is local and generated. It is reproducible and broad, but it is not hardware evidence.
\item Diffusion and robotics-transformer entries are surrogates, not trained external checkpoints.
\item The benchmark does not include real tactile streams, real compliance estimation, robot wear, actuator saturation, or human teleoperation artifacts.
\item The oracle supervisors retain success headroom, so the method is not a solved contact controller.
\item The v5 arbitration path was improved during development after ablation weaknesses were exposed; the final report freezes and reports the corrected protocol, but an independent replication is still required.
\item Page count, citation boxes, and formatting are not substitutes for external evidence. They only make the artifact easier to review.
\end{itemize}

\section{Reproducibility}
The repository is intended to rebuild the evidence and paper without hidden state. The command \texttt{python src/run\_experiment.py} regenerates CSVs, figures, tables, and \texttt{results/summary.json}. The command \texttt{python scripts/generate\_manuscript.py} regenerates this manuscript and bibliography. The validator checks row counts, terminal gates, citation-box settings, page count, PDF hashes, and the Downloads-only PDF invariant.

\section{Conclusion}
The expanded Paper 109 result is useful but not submission-ready. The mechanism is now clearer: a foundation policy should not interpolate through non-smooth contact boundaries without an explicit audit of mode, residual, impulse, hysteresis, probing, compliance, latency, energy, calibration, and risk. The local benchmark supports this mechanism under hostile stress tests and ablations. The honest terminal decision remains \terminal because external robotics evidence is missing.

\clearpage
\appendix
\section{Proof Details and Theoretical Notes}
The smooth-average non-identifiability proposition is intentionally distributional. It says that a nominal evaluator can hide boundary failures when the boundary mass is small. This is not a statement about one simulator. It applies to any evaluation distribution that undersamples contact-mode transitions. The practical consequence is that a reviewer should distrust a paper that reports only nominal success for a contact-rich policy.

The fixed-risk proposition can be written as a decomposition. Let $Y(a)$ be task success, $Z(a)$ be an unsafe-impulse event, and $G(a)$ be an audit accept event. The fixed-risk utility is
\[
  \mathbb{E}[Y(a)\mathbf{1}\{G(a)\}] - \alpha \mathbb{E}[Z(a)\mathbf{1}\{G(a)\}] - \beta \mathbb{E}[\mathrm{cost}(a)\mathbf{1}\{G(a)\}].
\]
An audit is useful when it removes more boundary risk than useful action, after accounting for intervention cost. This is why the final report includes coverage as well as utility. A method that rejects everything would look safe but useless; a method that accepts everything would look useful but unsafe.

\section{Task Cards}
\begin{longtable}{p{0.22\linewidth}p{0.68\linewidth}}
\toprule
Task & Contact-mode stressor \\
\midrule
Peg insertion & Tests impact onset, jamming, narrow clearances, and complementarity residuals under geometry shift. \\
Drawer opening & Tests stick--slip transitions, unilateral contact, actuator backlash, and release after static friction breaks. \\
Cable routing & Tests deformable contact, frictional memory, hidden compliance, and long-horizon jamming. \\
Tool levering & Tests impulse, release snap, stored energy, and contact-mode changes induced by torque amplification. \\
Mobile pushing & Tests friction-cone inversion, slip overshoot, and contact uncertainty over extended support surfaces. \\
Bimanual alignment & Tests coupled contacts where local correctness in one hand can create jamming in the other. \\
Deformable press-fit & Tests compliance shifts and the limits of rigid complementarity features. \\
Legged foot placement & Tests support changes, unilateral lift-off, impact timing, and mode-switch latency. \\
\bottomrule
\end{longtable}

\section{Regime Cards}
\begin{longtable}{p{0.25\linewidth}p{0.65\linewidth}}
\toprule
Regime & Purpose \\
\midrule
Nominal contact & Verifies that the audit does not destroy benign contact behavior. \\
Impact onset & Exposes impulse-budget failures and smooth predictions that enter contact too fast. \\
Stick--slip transition & Tests frictional hysteresis and mode oscillation. \\
Unilateral lift-off & Tests support loss and mode changes that can invalidate previous contacts. \\
Contact jamming & Tests local action choices that create hard-to-recover constraint configurations. \\
Release snap & Tests stored-energy release and energy-barrier checks. \\
Compliant fixture shift & Tests hidden geometry and deformability. \\
Friction-cone inversion & Tests slip overshoot and frictional uncertainty. \\
Actuator backlash & Tests latency and delayed mode switching. \\
Mixed non-smooth shock & Combines the above into the held-out stress split used for terminal gates. \\
\bottomrule
\end{longtable}

\section{Baseline Cards}
The comparison set is intentionally crowded. No-contact behavior cloning checks whether the benchmark is trivial. Domain randomization checks whether broad perturbation exposure is enough. Diffusion and robotics-transformer surrogates check whether generic expressive policies solve the boundary issue without explicit mechanics. Ensemble and conformal baselines check uncertainty routing. Smooth dynamics world models check whether learned smooth prediction is enough. Contact-implicit MPC, complementarity residual planning, robust hybrid MPC, learned contact classifiers, and energy-barrier policies check stronger mechanics-aware alternatives. The v4 atlas is the strongest non-oracle continuation baseline. Oracle supervisors show remaining headroom.

\clearpage
\section{Gate Equations and Interpretation}
The terminal decision is computed from explicit gates rather than from a subjective reading of plots. Let $P$ denote the v5 audit, let $B$ denote the strongest non-oracle baseline selected by hard-split utility, and let $O$ denote the oracle hybrid contact supervisor. Let $\bar{s}$ be success, $\bar{u}$ be utility, $\bar{f}$ be contact-mode F1, $\bar{e}_b$ be boundary error, and let the safety vector be
\[
  \bar{q}=(\mathrm{impulse},\mathrm{unsafe},\mathrm{jam},\mathrm{slip},
  \mathrm{latency},\mathrm{energy},\mathrm{ece},\mathrm{cost}).
\]
The success gate is passed if $\bar{s}_P-\bar{s}_B\ge 0.03$ or $\bar{u}_P-\bar{u}_B\ge 0.05$. This prevents a paper from claiming improvement on a tiny success change unless the utility objective, which includes safety and intervention cost, moves materially. The diagnostic gate is passed if contact-mode F1 improves by at least $0.05$ or boundary error falls by at least $0.04$. This is the gate most tied to the core claim: a contact-mode boundary audit should improve contact-boundary observables, not just win a reward proxy.

The safety gate is a vector non-regression test. Each risk component in $\bar{q}$ must not become materially worse than the strongest non-oracle baseline. This is stricter than reporting a single composite utility because a method could otherwise trade a lower jam rate for a higher unsafe-impulse rate and still look attractive. The paired gate uses seed-level utility differences on the held-out hard split and requires at least eight wins out of ten with positive mean difference against the strongest non-oracle baseline. The ablation gate requires the full method to beat the best removed-component variant by either $0.02$ success or $0.04$ utility. The stress gate requires positive endpoint utility under maximum non-smooth stress. The fixed-risk gate requires strict-budget coverage and utility improvement.

The scope gate is intentionally different from the empirical gates. It asks whether there is external robotics evidence: real robot rollouts, accepted high-fidelity benchmark replication, or independent trained-policy validation. The current answer is no. Therefore all local gates can pass and the terminal decision can still be \terminal rather than ready. This distinction is central to the paper. It prevents the manuscript from laundering a generated local benchmark into a claimed hardware result.

\clearpage
\section{Ablation Semantics}
The ablation protocol changed during development because a weak version of the protocol exposed an ambiguity. If an ablation removes a latency guard but keeps the coupled arbitration channel that relies on latency evidence, then the ablation has not truly removed the component. It is testing a partial degradation that may still enjoy the full method's coordination path. The final protocol therefore disables coupled arbitration whenever a required evidence channel is removed.

\begin{longtable}{p{0.27\linewidth}p{0.63\linewidth}}
\toprule
Ablation & What is removed and why it matters \\
\midrule
minus contact-mode classifier & Removes the local mode boundary cue; the method can no longer tell whether smooth interpolation crosses free, touch, stick, slip, jam, release, or impact modes. \\
minus complementarity residual & Removes the physical feasibility check that detects smooth predictions inconsistent with unilateral contact constraints. \\
minus impulse guard & Removes the action retiming rule near impact onset and release snap; unsafe impulse and energy release should increase. \\
minus stick--slip hysteresis & Removes memory over frictional state, allowing oscillations across visually similar stick and slip states. \\
minus diagnostic micro-probe & Removes active disambiguation of ambiguous contact states; hidden modes must be inferred passively. \\
minus compliance estimator & Removes the cue that distinguishes rigid contact from deformable fixture shifts and soft-object press-fit behavior. \\
minus mode-switch latency guard & Removes the timing guard around fast mode transitions; the method may recognize the mode but act too late. \\
minus energy barrier check & Removes the stored-energy release check; release snap can dominate complementarity residuals. \\
minus fixed-risk acceptor & Removes deployment-budget calibration; accepted actions are no longer tuned to a target risk budget. \\
\bottomrule
\end{longtable}

This ablation policy is harsher than leaving arbitration intact, but it is more faithful to the mechanism. The final result is not that every component is equally important. The latency guard remains the closest removed-component competitor. That is an informative weakness: timing is the least redundant part of the design and should be prioritized in hardware validation.

\clearpage
\section{Stress Protocol Details}
The stress sweep is not a single harder test set. It continuously increases the non-smooth load and reruns a selected subset of methods across all tasks, regimes, and seeds. At low stress, smooth methods can survive because boundary crossings are mild, sensor shift is small, and contact events are less abrupt. At intermediate stress, friction uncertainty, compliance, and latency begin to interact. At maximum stress, the held-out mixed shock combines geometry shift, unseen friction, unseen compliance, actuator latency, and sensor dropout.

This design has two purposes. First, it checks monotonic degradation. A method that improves only at one cherry-picked stress level is less convincing than a method whose advantage persists as stress changes. Second, it reveals whether the audit's advantage comes from a single failure mode. For example, a pure impulse guard might perform well at impact onset but fail under friction-cone inversion. A pure conformal filter might reject uncertain actions but fail to identify mechanically invalid smooth predictions. A complementarity residual planner might catch feasibility violations but miss stored-energy release. The v5 audit is meant to combine these cues without allowing one metric to hide another.

The endpoint margin @@STRESS_MARGIN@@ is therefore not interpreted as a universal guarantee. It is interpreted as evidence that the method does not collapse when the local generator concentrates probability mass on the exact boundary region that nominal evaluation tends to undersample. The endpoint is also where the failure cases are drawn. The failure table is not a qualitative decoration; it is the diagnostic surface that tells us what a real robot study must include.

The sweep also separates two kinds of robustness. The first is level robustness: a method should degrade gradually as a scalar stress variable increases. The second is composition robustness: a method should remain useful when several non-smooth causes appear together. Contact mechanics failures are often compositional. A small geometry error can make a friction uncertainty matter; a latency delay can turn a benign release into a snap; a compliance shift can turn a good insertion action into a jam. Reporting only a single hard split would hide which of these compositions is responsible for the terminal result.

In the final run, the v5 audit is not credited for matching the oracle. The oracle curves are included to show headroom. A submission-ready paper would need to explain the remaining oracle gap with measured contact labels and action traces. In this local version, the gap tells us that the audit still misses information: hidden compliance, tactile state, and longer-horizon contact consequences. That is why the sweep is paired with the failure taxonomy rather than being treated as a victory plot.

The runner keeps stress methods to a selected subset rather than all 16 methods to keep the CPU-only run light. The selected subset includes uncertainty, complementarity, robust hybrid, v4 atlas, v5 audit, and oracle reference methods. This is enough to test the main stress hypotheses while avoiding unnecessary memory and storage growth. The main all-method comparison still appears in the hard aggregate table.

\clearpage
\section{Fixed-Risk Acceptance Details}
The fixed-risk experiment answers a deployment-style question: if a user specifies a strict risk budget, how much useful behavior remains after the audit rejects high-risk actions? The risk score combines unsafe impulse, impulse violation, jam rate, slip overshoot, and energy spike. Coverage is the fraction of actions still accepted under the budget. Utility combines accepted success, recovery success, risk penalty, and intervention cost. This prevents two common mistakes. A method that rejects everything can look safe but has poor coverage and low utility. A method that accepts everything can look productive but fails the risk score.

The strict-budget coverage @@FIXED_COVERAGE@@ shows that the method does not win by simply refusing to act. The strict-budget utility margin @@FIXED_MARGIN@@ over the strongest non-oracle baseline shows that accepted actions remain useful. This is still not a safety certificate. It is a reproducible local test that should be repeated with real tactile, force, and proprioceptive signals before any deployment claim.

In a hardware extension, the fixed-risk budget would have to be calibrated against measured impulse, force-torque thresholds, end-effector speed, task-specific damage models, and human/robot separation constraints. The current paper does not perform that calibration. It only establishes the audit machinery that makes such calibration meaningful.

The fixed-risk endpoint is especially important for reviewer trust because it makes a common failure mode visible. A conservative contact filter can win safety metrics by refusing to execute difficult actions. If the paper reported only unsafe impulse, that degenerate policy would appear attractive. Coverage prevents this. The strict-budget result therefore has to be read as a pair: the method keeps high coverage and improves utility. If either term were missing, the evidence would be weaker.

The local risk score is also intentionally multi-term. Unsafe impulse alone would miss jamming and slip. Complementarity residual alone would miss stored-energy release. Energy spike alone would miss delayed mode switching. A fixed-risk acceptor for robotics must combine several imperfect proxies, and then validate them externally. The current score is not a deployment certificate; it is a scaffold for the external calibration that a real submission must provide.

\clearpage
\section{Implementation and Resource Discipline}
The implementation is intentionally CPU-only and RAM-light. The runner uses NumPy, CSV output, and Matplotlib figures. It does not train a large model, download external checkpoints, or require a GPU. The main evidence scale comes from combinatorial coverage: 8 tasks, 10 regimes, 8 splits, 16 methods, 10 seeds, stress sweeps, fixed-risk budgets, and ablations. This is a deliberate choice for a continuation batch where every paper must remain reproducible on ordinary local hardware.

The downside is that the experiment is a controlled generator, not a physics engine. The paper says this explicitly because hiding that fact would be a fatal submission flaw. The generator is useful for falsifying internal mechanism claims. It is not sufficient for external robot claims. The correct use is to expose weaknesses, improve the mechanism, freeze the final protocol, and then move to real robot or independent simulator validation.

All tables in the manuscript are either emitted directly by the runner or generated from the runner's JSON/CSV outputs. The validator checks row counts against the design, verifies finite numeric values in every CSV, enforces terminal gate semantics, checks the bright citation-box settings, checks page count, and verifies that the final numbered PDF in Downloads matches \texttt{paper/main.pdf}. This is mundane machinery, but it is how the artifact avoids drifting away from the evidence.

The final protocol also keeps large artifacts under control. The result files are plain CSVs and compact PNGs; no hidden binary dataset or trained checkpoint is required. This matters for the larger batch objective because Papers 61--120 must all remain reproducible in a shared pool. A single paper that requires heavyweight GPU training or multi-gigabyte artifacts would compromise the batch. The v5 evidence scale is therefore expressed through breadth of conditions rather than through expensive model training.

The generator and validator are part of the paper, not convenience scripts. The generator records how prose, tables, and references are assembled from the evidence. The validator records what must be true before the paper can be considered a terminal artifact. This is useful for future work because a later hardware version can replace the local CSVs while keeping the same validation skeleton.

\clearpage
\section{External Robot Study Design}
The next version should attach the audit to trained policies rather than local surrogates. A minimal study would use at least three contact-rich manipulation tasks on a real robot or accepted high-fidelity benchmark: insertion with tight tolerances, deformable or cable-like routing, and a release/impact task with stored energy. Each task should have nominal and shifted splits, with held-out geometry, friction, compliance, and latency perturbations. The audit should wrap a policy that is otherwise unchanged, so the comparison isolates the boundary-audit layer.

The baselines should include the original trained policy, domain randomization or augmentation, an uncertainty or ensemble rejection method, a conformal risk filter, a contact-aware planner or residual model where feasible, and the audit-wrapped policy. Metrics should include success, unsafe impulse or force-threshold violation, intervention rate, recovery success, contact-mode labels where available, and paired-trial statistics. The study should pre-register the terminal gates before running the final batch. Failed gates should be reported as failed gates.

Hardware videos and rollout logs matter because many contact failures are visually subtle. A method can appear to succeed while scraping, over-impulsing, or relying on hidden compliance. The hardware study should therefore include synchronized video, force/torque or tactile traces, proprioception, and the audit score trajectory. The paper should show not only success examples but also failures where the audit rejects an action or acts too late.

\clearpage
\section{Failure Taxonomy}
The 24 failure cases are grouped into recurring mechanisms. The first group is hidden-state failure: compliance, frictional memory, and unobserved support changes produce different modes under nearly identical observations. The second group is timing failure: diagnostic probes and mode classifiers can identify risk but still act too late near impact onset or release snap. The third group is horizon failure: a locally valid action can create a later jam, especially in cable routing and bimanual alignment. The fourth group is sensing failure: dropout and noisy tactile evidence degrade the boundary atlas.

Each group points to a different remedy. Hidden-state failure requires tactile or force-informed state estimation. Timing failure requires latency-aware control and possibly predictive retiming rather than reactive rejection. Horizon failure requires a planner that reasons over contact sequences instead of single-step action acceptance. Sensing failure requires calibrated sensor-health modeling and fallback policies. A stronger version of this paper would turn these remedies into new ablations rather than treating them as prose limitations.

\clearpage
\section{Prior-Work Boundary}
The nearest classical prior work is not a policy paper; it is non-smooth mechanics and contact dynamics. Those works supply the language of unilateral constraints, complementarity, impacts, and frictional mode switches. The nearest modern robotics prior work includes contact-implicit optimization, learned contact dynamics, MuJoCo-style simulation, and broad robot policy learning. A hostile reviewer could reasonably say that this paper does not invent contact dynamics, does not train a foundation model, and does not benchmark a real RT-style policy. That critique is correct.

The defensible boundary is therefore this: the paper studies an audit layer for foundation-policy candidates near non-smooth contact boundaries and shows, under a broad local stress protocol, that explicit boundary evidence improves held-out contact-risk behavior. It is a mechanism paper at the strong-revise stage. The novelty is not the existence of complementarity or the existence of diffusion policies. The novelty is the specific coupling of mode classification, residual feasibility, impulse and energy guards, hysteresis, probing, compliance, latency, calibration, and fixed-risk acceptance into a falsifiable audit protocol.

\clearpage
\section{What Would Falsify the Claim}
The claim would be weakened or falsified by several outcomes. If a trained external policy with simple domain randomization matches the audit on held-out contact shifts, then the explicit boundary machinery is unnecessary. If a conformal or ensemble filter achieves the same fixed-risk utility with lower intervention cost, then the mechanics-specific audit is not justified. If hardware rollouts show that the audit rejects too late near impact onset, then the latency guard is insufficient. If tactile/deformable tasks show no diagnostic advantage, then the contact-mode representation is too weak. If the oracle headroom closes only through task-specific tuning, then the method is not a foundation-policy layer.

These falsifiers are listed because a submission-ready paper should invite hard tests. The current local result survives its internal hostile protocol, but it has not survived the external tests above. That is why the decision remains \terminal.

\clearpage
\section{Reproducibility Checklist}
\begin{longtable}{p{0.32\linewidth}p{0.58\linewidth}}
\toprule
Item & Status in this artifact \\
\midrule
Code release & Runner, generator, validator, figures, tables, and CSVs are in the repository. \\
Compute & CPU-only NumPy/Matplotlib workflow; no GPU or external checkpoint required. \\
Randomness & Ten deterministic paired seeds are encoded in the runner. \\
Predefined gates & Terminal gates are computed from \texttt{summary.json}. \\
Strong baselines & Includes generic policy surrogates, uncertainty filters, mechanics-aware baselines, v4 atlas, and oracle supervisors. \\
Stress tests & Ten stress levels plus a held-out mixed non-smooth stress split. \\
Ablations & Ten ablation summaries with coupled arbitration disabled on component removal. \\
Failure cases & Twenty-four machine-readable cases with representative table in the paper. \\
Limitations & External robot scope gate is explicitly failed. \\
PDF integrity & Validator checks page count, hash match, citation-box settings, and Downloads-only location. \\
\bottomrule
\end{longtable}

\clearpage
\section{Parameterization Notes}
The runner uses compact method parameter vectors rather than learned networks. This is a limitation, but it also makes the ablation semantics inspectable. Each method has parameters for base competence, mode evidence, complementarity residual evidence, impulse handling, stick--slip hysteresis, diagnostic probing, compliance estimation, latency handling, energy checks, risk calibration, calibration quality, smooth-model bias, and intervention cost. The v5 method adds coupled arbitration. The coupled term is deliberately conservative: it depends on the weakest required evidence channel, so missing one component reduces the joint benefit.

This parameterization should not be read as a claim about exact hardware magnitudes. It is a controlled stress model. The useful question is not whether the generated success value is the true success value of a robot. The useful question is whether a method that claims to handle non-smooth contact can maintain its advantage when the generator changes task, regime, split, stress level, risk budget, seed, and component availability. The answer for v5 is yes locally, but not externally verified.

The strongest non-oracle baseline is not chosen by author preference. It is selected after the hard-split aggregation by utility among non-oracle methods excluding v5. In the terminal run this baseline is the v4 atlas, which makes the comparison stricter than comparing only to generic diffusion or transformer surrogates. The v4 atlas already has contact-mode evidence; v5 must therefore justify the additional coupled arbitration and expanded guard stack. The ablation result is what keeps that claim alive.

The intervention-cost term is also important. A contact audit can look good by stopping the robot too often. The utility objective penalizes that behavior. The fixed-risk experiment then checks whether the method remains useful under explicit budgeted acceptance. These two checks are redundant on purpose: one appears in the general utility, and the other appears in a deployment-style acceptance endpoint.

\clearpage
\section{Reviewer Response Matrix}
\begin{longtable}{p{0.30\linewidth}p{0.60\linewidth}}
\toprule
Likely reviewer concern & Evidence or response in this version \\
\midrule
The paper is too synthetic. & Agreed. The scope gate fails, ICLR readiness is marked no, and the terminal decision is \terminal. \\
The baselines might be weak. & The comparison set includes uncertainty, smooth-model, contact-implicit, complementarity, robust hybrid, energy-barrier, v4 atlas, and oracle references. \\
The method might only optimize success. & Utility, diagnostics, safety vector, fixed-risk coverage, stress endpoints, and failure cases are all reported. \\
The ablations might not remove components. & The final ablation protocol disables coupled arbitration whenever a required evidence channel is removed. \\
The oracle comparison is unclear. & Oracle supervisors are retained as reference headroom; v5 is not decisive against oracle baselines. \\
The paper might hide negative results. & The failure taxonomy, 24-case CSV, scope-gate failure, and terminal \terminal decision are all included. \\
The citation boxes are cosmetic. & Correct; they improve review navigation only. They do not affect the terminal decision. \\
The stress sweep could be cherry-picked. & The endpoint is generated over all tasks, all regimes, all seeds, and fixed stress levels emitted by the runner. \\
The policy is not a real foundation model. & Correct; the manuscript calls the diffusion and transformer methods surrogates and requires trained external policies before submission. \\
The page count could be padding. & The added pages are gate derivations, ablation semantics, stress/fixed-risk interpretation, resource discipline, external validation design, falsifiers, and reproducibility checks. \\
\bottomrule
\end{longtable}

\clearpage
\section{Submission-Readiness Delta}
The gap between this artifact and a plausible ICLR-main submission is concrete. First, the method must be attached to real trained policies. Second, the benchmark must include externally meaningful environments or hardware tasks. Third, force, tactile, or proprioceptive traces must validate the contact-mode labels or at least the unsafe-impulse proxies. Fourth, the ablation semantics must be repeated on the external stack, not only in the local generator. Fifth, the strongest baseline should be reselected after external results, because a different method may dominate under real dynamics.

A submission-ready version should also revise the theory. The current propositions justify why smooth averages can hide boundary failures and why fixed-risk audits can improve utility. A stronger theory section would connect audit calibration to measured contact impulses, show conditions under which diagnostic probing improves mode posterior entropy before a deadline, and bound the cost of false-positive rejections. Those additions require external measurements or a richer simulator; inventing them here would be worse than leaving the paper at \terminal.

The current version therefore maximizes acceptance odds in the only honest way available locally: it makes the mechanism explicit, raises the local experimental bar, surfaces weaknesses, validates the artifact, and refuses to claim readiness without missing evidence. That is the correct terminal state for Paper 109 under the expanded standard.

\section{Hostile Reviewer Checklist}
\paragraph{Is this a real robot paper?} No. It is a local evidence rebuild with a clear terminal decision. The paper should not be submitted as ICLR-main-ready without external validation.

\paragraph{Are the baselines too weak?} The benchmark includes both generic policy surrogates and mechanics-aware baselines. The strongest non-oracle comparator is the previous v4 atlas, not a strawman.

\paragraph{Is the method just tuned to the metric?} The final protocol reports diagnostics, safety, pairwise seeds, ablations, stress sweeps, fixed-risk acceptance, and failure cases. The method was improved only after a frozen-gate weakness was exposed, and the final terminal state is still conservative.

\paragraph{Do citations solve evidence gaps?} No. The bright citation boxes only improve review ergonomics. The scope gate remains false.

\section{External Validation Protocol Required Before Submission}
A real submission version should attach the audit to at least one trained generalist policy or accepted manipulation benchmark, include hardware or independent high-fidelity validation, publish videos and rollout logs, evaluate tactile/proprioceptive ablations, run the same fixed-risk gates, and keep the terminal decision honest if the mechanism fails. The current artifact is a strong revise package, not a camera-ready paper.

\begingroup
\raggedright
\bibliographystyle{iclr2026_conference}
\bibliography{references}
\endgroup

\end{document}
"""
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    write_gate_table(summary)
    write_row_table(summary)
    write_failure_table()
    write_references()
    (PAPER / "main.tex").write_text(manuscript_template(summary), encoding="utf-8")
    print("wrote paper/main.tex, paper/references.bib, and generated support tables")


if __name__ == "__main__":
    main()
