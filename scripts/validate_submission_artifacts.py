import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS_PDF = Path.home() / "Downloads" / "109.pdf"
DESKTOP_PDF = Path.home() / "Desktop" / "109.pdf"
FACTORY_ROOT_PDF = ROOT.parent / "109.pdf"
CHILD_ROOT_PDF = ROOT / "109.pdf"

EXPECTED_ROWS = {
    "dataset_summary_rows": 640,
    "main_cell_rows": 102400,
    "main_group_rows": 10240,
    "seed_metric_rows": 1280,
    "metric_rows": 128,
    "hard_seed_rows": 160,
    "hard_metric_rows": 16,
    "hard_pairwise_rows": 15,
    "ablation_cell_rows": 8000,
    "ablation_seed_rows": 100,
    "ablation_metric_rows": 10,
    "stress_cell_rows": 48000,
    "stress_seed_rows": 600,
    "stress_metric_rows": 60,
    "fixed_risk_cell_rows": 51200,
    "fixed_risk_seed_rows": 640,
    "fixed_risk_metric_rows": 64,
    "fixed_risk_pairwise_rows": 60,
    "failure_case_rows": 24,
}

ROW_FILES = {
    "dataset_summary_rows": RESULTS / "dataset_summary.csv",
    "main_cell_rows": RESULTS / "cell_metrics.csv",
    "main_group_rows": RESULTS / "main_group_metrics.csv",
    "seed_metric_rows": RESULTS / "seed_metrics.csv",
    "metric_rows": RESULTS / "metrics.csv",
    "hard_seed_rows": RESULTS / "hard_seed_metrics.csv",
    "hard_metric_rows": RESULTS / "hard_aggregate_metrics.csv",
    "hard_pairwise_rows": RESULTS / "hard_pairwise_stats.csv",
    "ablation_cell_rows": RESULTS / "ablation_cell_metrics.csv",
    "ablation_seed_rows": RESULTS / "ablation_seed_metrics.csv",
    "ablation_metric_rows": RESULTS / "ablation_metrics.csv",
    "stress_cell_rows": RESULTS / "stress_sweep_cell_metrics.csv",
    "stress_seed_rows": RESULTS / "stress_sweep_seed_metrics.csv",
    "stress_metric_rows": RESULTS / "stress_sweep.csv",
    "fixed_risk_cell_rows": RESULTS / "fixed_risk_cell_metrics.csv",
    "fixed_risk_seed_rows": RESULTS / "fixed_risk_seed_metrics.csv",
    "fixed_risk_metric_rows": RESULTS / "fixed_risk_metrics.csv",
    "fixed_risk_pairwise_rows": RESULTS / "fixed_risk_pairwise_stats.csv",
    "failure_case_rows": RESULTS / "failure_cases.csv",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def page_count(path):
    try:
        from pypdf import PdfReader
    except Exception:
        from PyPDF2 import PdfReader
    return len(PdfReader(str(path)).pages)


def count_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def assert_finite_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row_index, row in enumerate(reader, start=1):
            for key, value in row.items():
                if value is None or value == "":
                    continue
                try:
                    number = float(value)
                except ValueError:
                    continue
                if not math.isfinite(number):
                    raise AssertionError(f"non-finite value in {path}:{row_index}:{key}")


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    if summary["terminal_decision"] != "STRONG_REVISE":
        raise AssertionError("terminal decision is not STRONG_REVISE")
    if summary["iclr_main_ready"]:
        raise AssertionError("ICLR main readiness must remain false")
    for gate in [
        "success_gate",
        "diagnostic_gate",
        "safety_gate",
        "pairwise_gate",
        "ablation_gate",
        "stress_gate",
        "fixed_risk_gate",
    ]:
        if not summary["gates"].get(gate):
            raise AssertionError(f"local gate failed: {gate}")
    if summary["gates"].get("scope_gate"):
        raise AssertionError("scope gate should fail without external robot evidence")

    for key, expected in EXPECTED_ROWS.items():
        actual = int(summary["row_counts"][key])
        if actual != expected:
            raise AssertionError(f"{key}: expected {expected}, got {actual}")
        counted = count_csv(ROW_FILES[key])
        if counted != expected:
            raise AssertionError(f"{ROW_FILES[key]} row count expected {expected}, got {counted}")
        assert_finite_csv(ROW_FILES[key])

    tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    if "citebordercolor={0 0.85 0.20}" not in tex or "pdfborder={0 0 1.5}" not in tex:
        raise AssertionError("bright boxed citation hyperref settings missing")
    if "ICLR main ready is \\textbf{no}" not in tex:
        raise AssertionError("scope-gate sentence missing")
    if "\\textbf{STRONG\\_REVISE}" not in tex:
        raise AssertionError("terminal decision missing from manuscript")

    paper_pdf = PAPER / "main.pdf"
    if not paper_pdf.exists():
        raise AssertionError("paper/main.pdf missing")
    if not DOWNLOADS_PDF.exists():
        raise AssertionError("Downloads/109.pdf missing")
    if DESKTOP_PDF.exists():
        raise AssertionError("visible Desktop 109.pdf must not exist")
    if FACTORY_ROOT_PDF.exists():
        raise AssertionError("factory-root 109.pdf must not exist")
    if CHILD_ROOT_PDF.exists():
        raise AssertionError("child-root 109.pdf must not exist")

    pages = page_count(paper_pdf)
    if pages < 25:
        raise AssertionError(f"paper is too short: {pages} pages")
    paper_hash = sha256(paper_pdf)
    downloads_hash = sha256(DOWNLOADS_PDF)
    if paper_hash != downloads_hash:
        raise AssertionError("Downloads PDF hash does not match paper/main.pdf")
    print(f"validated Paper 109 artifacts: pages={pages}, sha256={paper_hash}")


if __name__ == "__main__":
    main()
