#!/usr/bin/env python3
"""BIP39 symbolic approximator v11 for all 445 physical constants.

Two modes are separated:

1. exact_symbolic mode:
   O_i = P_i * C_i, C_i := O_i/P_i.  This gives exact 445/445 convergence by
   definition and is validated symbolically.

2. predictive_symbolic mode:
   A ridge readout tries to predict log(C_i) from symbolic descriptors only
   (unit, sector, sign, BIP39 formula complexity, sparse magnitude).  This is
   the honest estimate of predictive power.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import sympy as sp

from bip39_fit_all_445_v8 import Fit445Row, evaluate as evaluate_v8


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"

RIDGE_LAMBDA = 3.0


@dataclass
class ApproxRow:
    name: str
    unit: str
    sector: str
    split: str
    observed: float
    sparse_prediction: float
    exact_calibration_coefficient: float
    exact_prediction: float
    exact_relative_error_percent: float
    predicted_calibration_coefficient: float
    predictive_prediction: float
    predictive_relative_error_percent: float
    predictive_log10_error: float
    predictive_pass_1_percent: bool
    predictive_pass_10_percent: bool
    sparse_formula: str
    status: str


@dataclass
class SummaryRow:
    metric: str
    value: str


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return "inf"
    return f"{value:.12g}"


def rel_error_percent(predicted: float, observed: float) -> float:
    if predicted == 0 or observed == 0 or not math.isfinite(predicted) or not math.isfinite(observed):
        return float("inf")
    return abs(predicted - observed) / abs(observed) * 100.0


def log10_error(predicted: float, observed: float) -> float:
    if predicted == 0 or observed == 0 or not math.isfinite(predicted) or not math.isfinite(observed):
        return float("inf")
    return abs(math.log10(abs(predicted / observed)))


def symbolic_identity_passes() -> bool:
    observed, predicted = sp.symbols("O P", nonzero=True)
    calibration = observed / predicted
    return sp.simplify(predicted * calibration - observed) == 0


def sector_of(row: Fit445Row) -> str:
    name = row.name.lower()
    unit = row.unit
    if unit == "":
        return "dimensionless_ratio"
    if any(token in name for token in ["planck", "gravitational", "newtonian", "vacuum", "speed of light"]):
        return "relativity_gravity"
    if any(token in name for token in ["hartree", "bohr", "atomic unit", "rydberg", "electron volt", "compton"]):
        return "quantum_atomic"
    if any(token in name for token in ["mag.", "magn.", "magneton", "josephson", "klitzing", "charge", "impedance"]):
        return "electromagnetic_quantum"
    if any(token in name for token in ["boltzmann", "kelvin", "molar", "gas", "stefan", "temperature"]):
        return "thermodynamic_statistical"
    if any(token in name for token in ["proton", "neutron", "deuteron", "triton", "helion", "alpha particle", "nuclear"]):
        return "nuclear_particle"
    if any(token in name for token in ["muon", "tau", "electron"]):
        return "lepton_particle"
    return "general_dimensional"


def deterministic_split(name: str) -> str:
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 5
    return "test" if bucket == 0 else "train"


def feature_names(rows: list[Fit445Row]) -> list[str]:
    units = sorted({row.unit or "dimensionless" for row in rows})
    sectors = sorted({sector_of(row) for row in rows})
    return (
        ["bias", "is_negative", "is_dimensionless", "log_abs_sparse", "complexity_proxy"]
        + [f"unit::{unit}" for unit in units]
        + [f"sector::{sector}" for sector in sectors]
    )


def complexity_from_formula(formula: str) -> float:
    return float(sum(abs(int(exp)) for exp in re.findall(r"\^(-?\d+)", formula)))


def vectorize(row: Fit445Row, names: list[str]) -> list[float]:
    unit = row.unit or "dimensionless"
    sector = sector_of(row)
    values = {
        "bias": 1.0,
        "is_negative": 1.0 if row.sign < 0 else 0.0,
        "is_dimensionless": 1.0 if row.is_dimensionless else 0.0,
        "log_abs_sparse": math.log(abs(row.sparse_signed_predicted) + 1e-300),
        "complexity_proxy": complexity_from_formula(row.sparse_formula),
    }
    values.update({name: 0.0 for name in names if name.startswith("unit::") or name.startswith("sector::")})
    values[f"unit::{unit}"] = 1.0
    values[f"sector::{sector}"] = 1.0
    return [values.get(name, 0.0) for name in names]


def solve_linear_system(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [a[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) < 1e-12:
            aug[pivot][col] = 1e-12
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][i] - factor * aug[col][i] for i in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


def fit_ridge(rows: list[Fit445Row], names: list[str]) -> list[float]:
    train = [row for row in rows if deterministic_split(row.name) == "train"]
    x_rows = [vectorize(row, names) for row in train]
    y = [math.log(abs(row.exact_calibration_coefficient) + 1e-300) for row in train]
    p = len(names)
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    xty = [0.0 for _ in range(p)]
    for x, yi in zip(x_rows, y):
        for i in range(p):
            xty[i] += x[i] * yi
            for j in range(p):
                xtx[i][j] += x[i] * x[j]
    for i, name in enumerate(names):
        xtx[i][i] += 0.0 if name == "bias" else RIDGE_LAMBDA
    return solve_linear_system(xtx, xty)


def predict_coeff(row: Fit445Row, names: list[str], theta: list[float]) -> float:
    x = vectorize(row, names)
    log_coeff = sum(a * b for a, b in zip(theta, x))
    log_coeff = max(-700.0, min(700.0, log_coeff))
    return math.exp(log_coeff)


def evaluate() -> tuple[list[ApproxRow], list[SummaryRow], dict[str, object]]:
    v8_rows, _v8_summary = evaluate_v8()
    names = feature_names(v8_rows)
    theta = fit_ridge(v8_rows, names)
    identity_ok = symbolic_identity_passes()
    rows: list[ApproxRow] = []
    for row in v8_rows:
        split = deterministic_split(row.name)
        predicted_coeff = predict_coeff(row, names, theta)
        predictive = row.sparse_signed_predicted * predicted_coeff
        pred_rel = rel_error_percent(predictive, row.value)
        exact = row.sparse_signed_predicted * row.exact_calibration_coefficient
        exact_rel = rel_error_percent(exact, row.value)
        rows.append(
            ApproxRow(
                name=row.name,
                unit=row.unit,
                sector=sector_of(row),
                split=split,
                observed=row.value,
                sparse_prediction=row.sparse_signed_predicted,
                exact_calibration_coefficient=row.exact_calibration_coefficient,
                exact_prediction=exact,
                exact_relative_error_percent=exact_rel,
                predicted_calibration_coefficient=predicted_coeff,
                predictive_prediction=predictive,
                predictive_relative_error_percent=pred_rel,
                predictive_log10_error=log10_error(predictive, row.value),
                predictive_pass_1_percent=pred_rel <= 1.0,
                predictive_pass_10_percent=pred_rel <= 10.0,
                sparse_formula=row.sparse_formula,
                status="EXACT_SYMBOLIC_OK" if identity_ok and exact_rel < 1e-10 else "FAILED",
            )
        )

    train_rows = [row for row in rows if row.split == "train"]
    test_rows = [row for row in rows if row.split == "test"]
    exact_pass = sum(row.exact_relative_error_percent < 1e-10 for row in rows)
    summary = [
        SummaryRow("catalog_total_constants", str(len(rows))),
        SummaryRow("train_count", str(len(train_rows))),
        SummaryRow("test_count", str(len(test_rows))),
        SummaryRow("feature_count", str(len(names))),
        SummaryRow("exact_symbolic_convergence", f"{exact_pass}/{len(rows)}"),
        SummaryRow("sympy_identity_validation", f"{sum(row.status == 'EXACT_SYMBOLIC_OK' for row in rows)}/{len(rows)}"),
        SummaryRow("predictive_train_pass_1_percent", f"{sum(row.predictive_pass_1_percent for row in train_rows)}/{len(train_rows)}"),
        SummaryRow("predictive_test_pass_1_percent", f"{sum(row.predictive_pass_1_percent for row in test_rows)}/{len(test_rows)}"),
        SummaryRow("predictive_train_pass_10_percent", f"{sum(row.predictive_pass_10_percent for row in train_rows)}/{len(train_rows)}"),
        SummaryRow("predictive_test_pass_10_percent", f"{sum(row.predictive_pass_10_percent for row in test_rows)}/{len(test_rows)}"),
        SummaryRow("predictive_train_median_rel_error_percent", fmt(sorted(row.predictive_relative_error_percent for row in train_rows)[len(train_rows) // 2])),
        SummaryRow("predictive_test_median_rel_error_percent", fmt(sorted(row.predictive_relative_error_percent for row in test_rows)[len(test_rows) // 2])),
        SummaryRow("scientific_verdict", "PERFECT_SYMBOLIC_CONVERGENCE_IN_CALIBRATED_MODE; LIMITED_OUT_OF_SAMPLE_PREDICTIVE_POWER"),
    ]
    model = {"feature_names": names, "theta": theta, "ridge_lambda": RIDGE_LAMBDA}
    return rows, summary, model


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[ApproxRow], summary: list[SummaryRow], model: dict[str, object]) -> None:
    test_worst = sorted([row for row in rows if row.split == "test"], key=lambda row: row.predictive_relative_error_percent, reverse=True)
    test_best = sorted([row for row in rows if row.split == "test"], key=lambda row: row.predictive_relative_error_percent)
    lines = [
        "# BIP39 Symbolic Approximator v11",
        "",
        "This is a two-mode approximator for all 445 SciPy/CODATA constants.",
        "",
        "```text",
        "exact_symbolic: O_i = P_i * C_i, C_i := O_i/P_i",
        "predictive_symbolic: C_i is estimated from symbolic descriptors without seeing test O_i",
        "```",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|:--|:--|",
    ]
    for row in summary:
        lines.append(f"| `{row.metric}` | `{row.value}` |")
    lines += [
        "",
        "## Model",
        "",
        f"- `ridge_lambda = {model['ridge_lambda']}`",
        f"- `feature_count = {len(model['feature_names'])}`",
        "",
        "## Best Test Predictions",
        "",
        "| Constant | Sector | Unit | Observed | Predicted | Rel error % |",
        "|:--|:--|:--|--:|--:|--:|",
    ]
    for row in test_best[:60]:
        lines.append(
            f"| `{row.name}` | `{row.sector}` | `{row.unit}` | `{fmt(row.observed)}` | `{fmt(row.predictive_prediction)}` | `{fmt(row.predictive_relative_error_percent)}` |"
        )
    lines += [
        "",
        "## Worst Test Predictions",
        "",
        "| Constant | Sector | Unit | Observed | Predicted | Rel error % |",
        "|:--|:--|:--|--:|--:|--:|",
    ]
    for row in test_worst[:60]:
        lines.append(
            f"| `{row.name}` | `{row.sector}` | `{row.unit}` | `{fmt(row.observed)}` | `{fmt(row.predictive_prediction)}` | `{fmt(row.predictive_relative_error_percent)}` |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "The exact symbolic mode converges perfectly by definition because C_i is defined from O_i.",
        "The predictive mode is the honest test: it tries to estimate calibration coefficients on held-out constants.",
        "Therefore the theory can be symbolically complete while still having limited empirical predictive power.",
        "",
    ]
    (RESULTS / "bip39_symbolic_approximator_v11_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows, summary, model = evaluate()
    payload = {
        "summary": [asdict(row) for row in summary],
        "model": model,
        "rows": [asdict(row) for row in rows],
    }
    (RESULTS / "bip39_symbolic_approximator_v11.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "bip39_symbolic_approximator_v11.csv", [asdict(row) for row in rows])
    write_report(rows, summary, model)
    print("BIP39_SYMBOLIC_APPROXIMATOR_V11: OK")
    for row in summary:
        print(f"{row.metric}: {row.value}")
    print(RESULTS / "bip39_symbolic_approximator_v11_report.md")


if __name__ == "__main__":
    main()
