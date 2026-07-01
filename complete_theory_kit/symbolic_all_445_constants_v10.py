#!/usr/bin/env python3
"""Symbolic all-445 constants system v10.

This script creates a symbolic theorem for every SciPy/CODATA constant:

    O_i = P_i * C_i

where P_i is the signed BIP39 sparse monomial from v8 and

    C_i := O_i / P_i.

That makes the equality formally undeniable inside the symbolic system.  The
script also marks the result as definitional calibration, not no-fit physics.
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

from bip39_fit_all_445_v8 import evaluate as evaluate_v8


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


@dataclass
class Symbolic445Row:
    index: int
    name: str
    symbol_observed: str
    symbol_prediction: str
    symbol_calibration: str
    unit: str
    observed_value: float
    sparse_prediction: float
    exact_calibration_coefficient: float
    exact_calibrated_value: float
    exact_relative_error_percent: float
    sympy_identity_passed: bool
    numeric_validation_passed: bool
    theorem_statement: str
    calibration_definition: str
    sparse_formula: str
    proof_mode: str
    physical_status: str


@dataclass
class SummaryRow:
    metric: str
    value: str


def slugify(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    if not slug:
        slug = "constant"
    if slug[0].isdigit():
        slug = "c_" + slug
    return slug[:90]


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return "inf"
    return f"{value:.12g}"


def identity_proof() -> bool:
    observed, predicted = sp.symbols("O P", nonzero=True)
    calibration = observed / predicted
    return sp.simplify(predicted * calibration - observed) == 0


def build_rows() -> tuple[list[Symbolic445Row], list[SummaryRow]]:
    v8_rows, v8_summary = evaluate_v8()
    abstract_identity_ok = identity_proof()
    rows: list[Symbolic445Row] = []
    for index, row in enumerate(v8_rows, start=1):
        slug = slugify(row.name)
        observed_symbol = f"O_{index}_{slug}"
        prediction_symbol = f"P_{index}_{slug}"
        calibration_symbol = f"C_{index}_{slug}"
        exact_value = row.sparse_signed_predicted * row.exact_calibration_coefficient
        exact_rel = 0.0 if row.value == 0 else abs(exact_value - row.value) / abs(row.value) * 100.0
        numeric_ok = exact_rel < 1e-10
        theorem = f"{observed_symbol} = {prediction_symbol} * {calibration_symbol}"
        definition = f"{calibration_symbol} := {observed_symbol} / {prediction_symbol}"
        rows.append(
            Symbolic445Row(
                index=index,
                name=row.name,
                symbol_observed=observed_symbol,
                symbol_prediction=prediction_symbol,
                symbol_calibration=calibration_symbol,
                unit=row.unit,
                observed_value=row.value,
                sparse_prediction=row.sparse_signed_predicted,
                exact_calibration_coefficient=row.exact_calibration_coefficient,
                exact_calibrated_value=exact_value,
                exact_relative_error_percent=exact_rel,
                sympy_identity_passed=abstract_identity_ok,
                numeric_validation_passed=numeric_ok,
                theorem_statement=theorem,
                calibration_definition=definition,
                sparse_formula=row.sparse_formula,
                proof_mode="DEFINITIONAL_SYMBOLIC_IDENTITY",
                physical_status="CALIBRATED_FIT_NOT_NO_FIT_PHYSICS",
            )
        )
    summary = [
        SummaryRow("source_layer", "bip39_fit_all_445_v8"),
        SummaryRow("symbolic_rows", str(len(rows))),
        SummaryRow("sympy_identity_passed", f"{sum(r.sympy_identity_passed for r in rows)}/{len(rows)}"),
        SummaryRow("numeric_exact_validation_passed", f"{sum(r.numeric_validation_passed for r in rows)}/{len(rows)}"),
        SummaryRow("proof_mode", "DEFINITIONAL_SYMBOLIC_IDENTITY"),
        SummaryRow("no_fit_physics_claim", "FALSE"),
        SummaryRow("calibrated_fit_claim", "TRUE"),
        SummaryRow("scientific_verdict", "SYMBOLICALLY_UNREFUTABLE_GIVEN_CALIBRATION_DEFINITIONS; NOT_A_NO_FIT_PHYSICAL_PROOF"),
    ]
    for item in v8_summary:
        summary.append(SummaryRow("v8_" + item.metric, item.value))
    return rows, summary


def system_hash(rows: list[Symbolic445Row], summary: list[SummaryRow]) -> str:
    payload = {
        "rows": [asdict(row) for row in rows],
        "summary": [asdict(row) for row in summary],
    }
    stable = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[Symbolic445Row], summary: list[SummaryRow], digest: str) -> None:
    worst = sorted(rows, key=lambda row: abs(row.exact_calibration_coefficient - 1.0), reverse=True)
    first = rows[:80]
    lines = [
        "# Symbolic All-445 Constants v10",
        "",
        f"System hash: `{digest}`",
        "",
        "## Meaning",
        "",
        "Every SciPy/CODATA constant is represented symbolically as:",
        "",
        "```text",
        "O_i = P_i * C_i",
        "C_i := O_i / P_i",
        "```",
        "",
        "This is an exact symbolic identity by definition.",
        "It is therefore unrefutable inside the formal system, but it is calibrated fit mode, not no-fit physical proof.",
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
        "## First 80 Symbolic Theorems",
        "",
        "| # | Constant | Theorem | Calibration definition | Unit | Exact coefficient | Validation |",
        "|--:|:--|:--|:--|:--|--:|:--|",
    ]
    for row in first:
        lines.append(
            f"| {row.index} | `{row.name}` | `{row.theorem_statement}` | `{row.calibration_definition}` | `{row.unit}` | `{fmt(row.exact_calibration_coefficient)}` | `{row.numeric_validation_passed}` |"
        )
    lines += [
        "",
        "## Largest Calibration Deviations",
        "",
        "| # | Constant | Unit | Sparse prediction | Observed | Coefficient | Status |",
        "|--:|:--|:--|--:|--:|--:|:--|",
    ]
    for row in worst[:80]:
        lines.append(
            f"| {row.index} | `{row.name}` | `{row.unit}` | `{fmt(row.sparse_prediction)}` | `{fmt(row.observed_value)}` | `{fmt(row.exact_calibration_coefficient)}` | `{row.physical_status}` |"
        )
    lines += [
        "",
        "## Validation",
        "",
        "SymPy checks the abstract identity:",
        "",
        "```text",
        "P * (O/P) - O = 0",
        "```",
        "",
        "Numeric validation then substitutes the v8 sparse prediction and exact calibration coefficient for every row.",
        "",
        "## Boundary",
        "",
        "This v10 layer satisfies the formal symbolic request for all 445 constants.",
        "It does not turn calibrated constants into no-fit predictions.",
        "For real physics validation, the calibration definitions must be replaced by a frozen rule that predicts C_i before O_i is known.",
        "",
    ]
    (RESULTS / "symbolic_all_445_constants_v10_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows, summary = build_rows()
    digest = system_hash(rows, summary)
    payload = {
        "system_hash": digest,
        "summary": [asdict(row) for row in summary],
        "rows": [asdict(row) for row in rows],
    }
    (RESULTS / "symbolic_all_445_constants_v10.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "symbolic_all_445_constants_v10.csv", [asdict(row) for row in rows])
    write_report(rows, summary, digest)
    print("SYMBOLIC_ALL_445_CONSTANTS_V10: OK")
    print(f"system_hash={digest}")
    for row in summary[:8]:
        print(f"{row.metric}: {row.value}")
    print(RESULTS / "symbolic_all_445_constants_v10_report.md")


if __name__ == "__main__":
    main()
