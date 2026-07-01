#!/usr/bin/env python3
"""Fit all 445 SciPy/CODATA constants with BIP39 sparse monomials.

This is intentionally a fitting/diagnostic layer, not a proof layer.
Every catalog entry receives:

- a signed BIP39 sparse monomial approximation;
- relative/log error of that approximation;
- an exact target-specific calibration coefficient.

The exact calibrated column necessarily gives 445/445; it is included to make
the amount of required target-specific fitting visible.
"""

from __future__ import annotations

import csv
import json
import math
from bisect import bisect_left
from dataclasses import asdict, dataclass
from pathlib import Path

import scipy.constants as scipy_constants

from bip39_unification_search_v5 import bip39, feature_values, sparse_candidates


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


@dataclass
class Fit445Row:
    name: str
    value: float
    sign: int
    magnitude: float
    unit: str
    uncertainty: float
    is_dimensionless: bool
    sparse_signed_predicted: float
    sparse_magnitude_predicted: float
    sparse_relative_error_percent: float
    sparse_log10_error: float
    sparse_pass_1_percent: bool
    sparse_pass_0_1_percent: bool
    sparse_complexity: int
    sparse_formula: str
    exact_calibration_coefficient: float
    exact_calibrated_predicted: float
    exact_calibrated_relative_error_percent: float
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
    if predicted <= 0 or observed <= 0 or not math.isfinite(predicted) or not math.isfinite(observed):
        return float("inf")
    return abs(math.log10(predicted / observed))


def base_for_constant(name: str, unit: str) -> tuple[float, str]:
    # This is a diagnostic choice, not a unit theory. Most SI-dimensional
    # constants use raw magnitude base 1, which makes the fit unit-dependent.
    lower = name.lower()
    if unit == "":
        return 1.0, "1"
    if unit == "MeV" and "mass energy equivalent" in lower:
        return 0.51099895069, "m_e[MeV]"
    if unit == "J T^-1" and "mag. mom." in lower:
        return 9.2740100657e-24, "mu_B[J/T]"
    return 1.0, "1"


def catalog_all_445() -> list[tuple[str, float, str, float]]:
    rows = []
    for name, (value, unit, uncertainty) in scipy_constants.physical_constants.items():
        value = float(value)
        if math.isfinite(value):
            rows.append((name, value, unit, float(uncertainty)))
    return sorted(rows, key=lambda row: row[0].lower())


def build_candidate_index(candidates: list[tuple[float, int, str]]) -> dict[int, list[tuple[float, float, str]]]:
    by_complexity: dict[int, list[tuple[float, float, str]]] = {}
    for multiplier, complexity, formula in candidates:
        if multiplier <= 0 or not math.isfinite(multiplier):
            continue
        by_complexity.setdefault(complexity, []).append((math.log(multiplier), multiplier, formula))
    for values in by_complexity.values():
        values.sort(key=lambda item: item[0])
    return by_complexity


def best_sparse_for_magnitude(
    magnitude: float,
    base: float,
    candidate_index: dict[int, list[tuple[float, float, str]]],
) -> tuple[float, float, float, str, int]:
    best: tuple[float, float, float, str, int] | None = None
    target_log = math.log(magnitude / base)
    for complexity, values in candidate_index.items():
        logs = [item[0] for item in values]
        idx = bisect_left(logs, target_log)
        for near in {idx - 2, idx - 1, idx, idx + 1, idx + 2}:
            if near < 0 or near >= len(values):
                continue
            _log_multiplier, multiplier, formula = values[near]
            predicted = base * multiplier
            if predicted <= 0:
                continue
            log_err = log10_error(predicted, magnitude)
            rel = rel_error_percent(predicted, magnitude)
            objective = log_err + 0.01 * complexity
            if best is None or objective < best[1] + 0.01 * best[4]:
                best = (predicted, log_err, rel, formula, complexity)
    assert best is not None
    return best


def best_sparse_for_magnitude_slow_reference(
    magnitude: float,
    base: float,
    candidates: list[tuple[float, int, str]],
) -> tuple[float, float, float, str, int]:
    best: tuple[float, float, float, str, int] | None = None
    for multiplier, complexity, formula in candidates:
        predicted = base * multiplier
        if predicted <= 0:
            continue
        log_err = log10_error(predicted, magnitude)
        rel = rel_error_percent(predicted, magnitude)
        objective = log_err + 0.01 * complexity
        if best is None or objective < best[1] + 0.01 * best[4]:
            best = (predicted, log_err, rel, formula, complexity)
    assert best is not None
    return best


def evaluate() -> tuple[list[Fit445Row], list[SummaryRow]]:
    inv = bip39()
    features = feature_values(inv)
    candidates = list(sparse_candidates(features))
    candidate_index = build_candidate_index(candidates)
    rows: list[Fit445Row] = []
    for name, value, unit, uncertainty in catalog_all_445():
        sign = -1 if value < 0 else 1
        magnitude = abs(value)
        base, base_text = base_for_constant(name, unit)
        sparse_mag, sparse_log, sparse_rel, sparse_formula, complexity = best_sparse_for_magnitude(magnitude, base, candidate_index)
        signed_pred = sign * sparse_mag
        coeff = magnitude / sparse_mag
        exact = sign * sparse_mag * coeff
        exact_rel = rel_error_percent(exact, value)
        if unit == "":
            status = "DIMENSIONLESS_LOOK_ELSEWHERE_FIT"
        else:
            status = "DIMENSIONAL_UNIT_DEPENDENT_LOOK_ELSEWHERE_FIT"
        rows.append(
            Fit445Row(
                name=name,
                value=value,
                sign=sign,
                magnitude=magnitude,
                unit=unit,
                uncertainty=uncertainty,
                is_dimensionless=(unit == ""),
                sparse_signed_predicted=signed_pred,
                sparse_magnitude_predicted=sparse_mag,
                sparse_relative_error_percent=sparse_rel,
                sparse_log10_error=sparse_log,
                sparse_pass_1_percent=sparse_rel <= 1.0,
                sparse_pass_0_1_percent=sparse_rel <= 0.1,
                sparse_complexity=complexity,
                sparse_formula=f"sign({sign}) * {base_text} * {sparse_formula}",
                exact_calibration_coefficient=coeff,
                exact_calibrated_predicted=exact,
                exact_calibrated_relative_error_percent=exact_rel,
                status=status,
            )
        )
    dimless = [row for row in rows if row.is_dimensionless]
    dimensional = [row for row in rows if not row.is_dimensionless]
    pass_1 = [row for row in rows if row.sparse_pass_1_percent]
    pass_01 = [row for row in rows if row.sparse_pass_0_1_percent]
    coeff_devs = [abs(row.exact_calibration_coefficient - 1.0) * 100.0 for row in rows]
    summary = [
        SummaryRow("catalog_source", "scipy.constants.physical_constants"),
        SummaryRow("catalog_total_constants", str(len(rows))),
        SummaryRow("negative_constants_included", str(sum(1 for row in rows if row.sign < 0))),
        SummaryRow("dimensionless_constants", str(len(dimless))),
        SummaryRow("dimensional_constants", str(len(dimensional))),
        SummaryRow("candidate_monomials_per_constant", str(len(candidates))),
        SummaryRow("sparse_fit_pass_1_percent", f"{len(pass_1)}/{len(rows)}"),
        SummaryRow("sparse_fit_pass_0_1_percent", f"{len(pass_01)}/{len(rows)}"),
        SummaryRow("sparse_fit_pass_1_percent_dimensionless", f"{sum(row.sparse_pass_1_percent for row in dimless)}/{len(dimless)}"),
        SummaryRow("target_calibrated_exact_pass", f"{sum(row.exact_calibrated_relative_error_percent < 1e-10 for row in rows)}/{len(rows)}"),
        SummaryRow("mean_sparse_relative_error_percent", fmt(sum(row.sparse_relative_error_percent for row in rows) / len(rows))),
        SummaryRow("median_sparse_relative_error_percent", fmt(sorted(row.sparse_relative_error_percent for row in rows)[len(rows) // 2])),
        SummaryRow("max_sparse_relative_error_percent", fmt(max(row.sparse_relative_error_percent for row in rows))),
        SummaryRow("mean_exact_calibration_deviation_percent", fmt(sum(coeff_devs) / len(coeff_devs))),
        SummaryRow("median_exact_calibration_deviation_percent", fmt(sorted(coeff_devs)[len(coeff_devs) // 2])),
        SummaryRow("scientific_verdict", "ALL_445_FITTED_DIAGNOSTICALLY; EXACT_445_REQUIRES_TARGET_SPECIFIC_COEFFICIENTS"),
    ]
    return rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[Fit445Row], summary: list[SummaryRow]) -> None:
    sorted_best = sorted(rows, key=lambda row: row.sparse_relative_error_percent)
    sorted_worst = sorted(rows, key=lambda row: row.sparse_relative_error_percent, reverse=True)
    lines = [
        "# BIP39 Fit All 445 Constants v8",
        "",
        "This report fits every SciPy/CODATA physical-constants entry with a signed BIP39 sparse monomial.",
        "It includes negative constants by fitting the magnitude and restoring the sign.",
        "Exact 445/445 agreement is obtained only by adding a target-specific calibration coefficient.",
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
        "## Best Sparse Fits",
        "",
        "| Constant | Unit | Value | Sparse predicted | Rel error % | Complexity | Formula |",
        "|:--|:--|--:|--:|--:|--:|:--|",
    ]
    for row in sorted_best[:80]:
        lines.append(
            f"| `{row.name}` | `{row.unit}` | `{fmt(row.value)}` | `{fmt(row.sparse_signed_predicted)}` | `{fmt(row.sparse_relative_error_percent)}` | {row.sparse_complexity} | `{row.sparse_formula}` |"
        )
    lines += [
        "",
        "## Worst Sparse Fits",
        "",
        "| Constant | Unit | Value | Sparse predicted | Rel error % | Complexity | Exact coefficient |",
        "|:--|:--|--:|--:|--:|--:|--:|",
    ]
    for row in sorted_worst[:80]:
        lines.append(
            f"| `{row.name}` | `{row.unit}` | `{fmt(row.value)}` | `{fmt(row.sparse_signed_predicted)}` | `{fmt(row.sparse_relative_error_percent)}` | {row.sparse_complexity} | `{fmt(row.exact_calibration_coefficient)}` |"
        )
    lines += [
        "",
        "## Calibration Meaning",
        "",
        "The column `exact_calibration_coefficient` in the CSV/JSON is the number that makes the sparse BIP39 formula exact.",
        "Therefore `target_calibrated_exact_pass = 445/445` is mathematically trivial after fitting and is not a physical proof.",
        "The useful result is the visible distribution of how much calibration each constant needs.",
        "",
        "## Scientific Status",
        "",
        "This v8 layer satisfies the request to fit all 445 catalog constants.",
        "It should be cited as a diagnostic fit table, not as a no-fit derivation of all constants.",
        "A proof-level version would need one frozen rule that selects the formula for a new constant before its value is known, plus a declared unit basis for dimensional constants.",
        "",
    ]
    (RESULTS / "bip39_fit_all_445_v8_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows, summary = evaluate()
    payload = {
        "summary": [asdict(row) for row in summary],
        "rows": [asdict(row) for row in rows],
    }
    (RESULTS / "bip39_fit_all_445_v8.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "bip39_fit_all_445_v8.csv", [asdict(row) for row in rows])
    write_report(rows, summary)
    for row in summary:
        print(f"{row.metric}: {row.value}")
    print(RESULTS / "bip39_fit_all_445_v8_report.md")


if __name__ == "__main__":
    main()
