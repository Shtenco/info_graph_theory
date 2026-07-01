#!/usr/bin/env python3
"""BIP39 benchmark against the full SciPy/CODATA physical-constants catalog.

This is the large stress test requested for 300+ constants.  It uses
scipy.constants.physical_constants as the catalog source.

The script deliberately separates:

1. Frozen BIP39 no-fit coverage: only formulas frozen in v6 count as real model
   predictions.
2. Sparse-search diagnostic: a look-elsewhere diagnostic showing how often a
   BIP39 monomial search can numerically approximate constants.  This is not
   accepted as proof, especially for dimensional SI values.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import scipy.constants as scipy_constants

from bip39_no_fit_verification_v6 import FROZEN_FORMULAS, formula_registry_hash
from bip39_unification_search_v5 import M_E_MEV, bip39, feature_values, sparse_candidates


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


ALIASES_TO_FROZEN = {
    "fine-structure constant": "alpha",
    "Fermi coupling constant": "G_F_GeV_minus2",
    "weak mixing angle": "sin2_thetaW",
    "proton mass energy equivalent in MeV": "proton_mass_MeV",
}


@dataclass
class ConstantRow:
    name: str
    value: float
    unit: str
    uncertainty: float
    is_dimensionless: bool
    frozen_formula_key: str
    frozen_predicted: float | None
    frozen_relative_error_percent: float | None
    frozen_pass_1_percent: bool
    frozen_status: str
    sparse_predicted: float
    sparse_relative_error_percent: float
    sparse_log10_error: float
    sparse_pass_1_percent: bool
    sparse_formula: str
    sparse_complexity: int
    sparse_status: str


@dataclass
class SummaryRow:
    metric: str
    value: str


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING"
    if not math.isfinite(value):
        return "inf"
    return f"{value:.12g}"


def formula_value(key: str, features: dict[str, float]) -> float:
    spec = FROZEN_FORMULAS[key]
    predicted = float(spec["base"])
    for name, exponent in spec["factors"].items():
        predicted *= features[name] ** exponent
    return predicted


def rel_error_percent(predicted: float, observed: float) -> float:
    if predicted <= 0 or observed <= 0 or not math.isfinite(predicted) or not math.isfinite(observed):
        return float("inf")
    return abs(predicted - observed) / abs(observed) * 100.0


def log10_error(predicted: float, observed: float) -> float:
    if predicted <= 0 or observed <= 0 or not math.isfinite(predicted) or not math.isfinite(observed):
        return float("inf")
    return abs(math.log10(predicted / observed))


def diagnostic_base(name: str, unit: str) -> tuple[float, str]:
    lower = name.lower()
    if unit == "":
        return 1.0, "dimensionless_valid"
    if unit == "MeV" and "mass energy equivalent" in lower:
        return M_E_MEV, "mass_mev_base_electron"
    if unit == "GeV^-2":
        return 1.0, "natural_unit_dimensional_proxy"
    return 1.0, "raw_SI_dimensional_not_physical"


def best_sparse(value: float, base: float, candidates: list[tuple[float, int, str]]) -> tuple[float, float, float, str, int]:
    best: tuple[float, float, float, str, int] | None = None
    for multiplier, complexity, formula in candidates:
        predicted = base * multiplier
        err = log10_error(predicted, value)
        objective = err + 0.01 * complexity
        if best is None or objective < best[1] + 0.01 * best[4]:
            best = (predicted, err, rel_error_percent(predicted, value), formula, complexity)
    assert best is not None
    return best


def constant_catalog() -> list[tuple[str, float, str, float]]:
    rows = []
    for name, (value, unit, uncertainty) in scipy_constants.physical_constants.items():
        if value > 0 and math.isfinite(value):
            rows.append((name, float(value), unit, float(uncertainty)))
    return sorted(rows, key=lambda item: item[0].lower())


def evaluate() -> tuple[list[ConstantRow], list[SummaryRow]]:
    inv = bip39()
    features = feature_values(inv)
    candidates = list(sparse_candidates(features))
    rows: list[ConstantRow] = []
    for name, value, unit, uncertainty in constant_catalog():
        frozen_key = ALIASES_TO_FROZEN.get(name, "")
        frozen_predicted = None
        frozen_rel = None
        frozen_pass = False
        if frozen_key:
            frozen_predicted = formula_value(frozen_key, features)
            frozen_rel = rel_error_percent(frozen_predicted, value)
            frozen_pass = frozen_rel <= 1.0
            frozen_status = "FROZEN_NO_FIT_PREDICTION"
        else:
            frozen_status = "MISSING_FROZEN_FORMULA"

        base, sparse_status = diagnostic_base(name, unit)
        sparse_pred, sparse_log, sparse_rel, sparse_formula, sparse_complexity = best_sparse(value, base, candidates)
        if sparse_status == "raw_SI_dimensional_not_physical":
            sparse_status = "LOOK_ELSEWHERE_RAW_DIMENSIONAL_DIAGNOSTIC_ONLY"
        elif sparse_status == "dimensionless_valid":
            sparse_status = "LOOK_ELSEWHERE_DIMENSIONLESS_DIAGNOSTIC_ONLY"
        else:
            sparse_status = "LOOK_ELSEWHERE_NATURAL_UNIT_DIAGNOSTIC_ONLY"

        rows.append(
            ConstantRow(
                name=name,
                value=value,
                unit=unit,
                uncertainty=uncertainty,
                is_dimensionless=(unit == ""),
                frozen_formula_key=frozen_key or "MISSING",
                frozen_predicted=frozen_predicted,
                frozen_relative_error_percent=frozen_rel,
                frozen_pass_1_percent=frozen_pass,
                frozen_status=frozen_status,
                sparse_predicted=sparse_pred,
                sparse_relative_error_percent=sparse_rel,
                sparse_log10_error=sparse_log,
                sparse_pass_1_percent=sparse_rel <= 1.0,
                sparse_formula=f"{base:.6g} * {sparse_formula}",
                sparse_complexity=sparse_complexity,
                sparse_status=sparse_status,
            )
        )

    dimensionless = [r for r in rows if r.is_dimensionless]
    dimensional = [r for r in rows if not r.is_dimensionless]
    mapped = [r for r in rows if r.frozen_status == "FROZEN_NO_FIT_PREDICTION"]
    sparse_dimless = [r for r in dimensionless if r.sparse_pass_1_percent]
    sparse_all = [r for r in rows if r.sparse_pass_1_percent]
    summary = [
        SummaryRow("catalog_source", "scipy.constants.physical_constants"),
        SummaryRow("catalog_total_positive_constants", str(len(rows))),
        SummaryRow("dimensionless_constants", str(len(dimensionless))),
        SummaryRow("dimensional_constants", str(len(dimensional))),
        SummaryRow("frozen_registry_hash", formula_registry_hash()),
        SummaryRow("frozen_no_fit_predictions_available", f"{len(mapped)}/{len(rows)}"),
        SummaryRow("frozen_no_fit_predictions_pass_1_percent", f"{sum(r.frozen_pass_1_percent for r in mapped)}/{len(mapped)}"),
        SummaryRow("missing_frozen_formulas", str(len(rows) - len(mapped))),
        SummaryRow("sparse_search_candidate_count_per_constant", str(len(candidates))),
        SummaryRow("sparse_diagnostic_pass_1_percent_all_constants", f"{len(sparse_all)}/{len(rows)}"),
        SummaryRow("sparse_diagnostic_pass_1_percent_dimensionless", f"{len(sparse_dimless)}/{len(dimensionless)}"),
        SummaryRow("scientific_verdict", "FROZEN_BIP39_MODEL_DOES_NOT_COVER_300_PLUS_CONSTANTS; sparse search is diagnostic only"),
    ]
    return rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[ConstantRow], summary: list[SummaryRow]) -> None:
    mapped = [r for r in rows if r.frozen_status == "FROZEN_NO_FIT_PREDICTION"]
    missing = [r for r in rows if r.frozen_status == "MISSING_FROZEN_FORMULA"]
    sparse_dimless = [r for r in rows if r.is_dimensionless]
    sparse_dimless_sorted = sorted(sparse_dimless, key=lambda r: r.sparse_relative_error_percent)
    worst_mapped = sorted(mapped, key=lambda r: r.frozen_relative_error_percent or float("inf"), reverse=True)
    lines = [
        "# BIP39 All-Constants Benchmark v7",
        "",
        "This benchmark tests the BIP39 model against the full SciPy/CODATA physical-constants catalog.",
        "Only frozen v6 formulas count as no-fit predictions.",
        "Sparse-search rows are diagnostic only and do not count as proof.",
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
        "## Frozen No-Fit Coverage",
        "",
        "| Constant | Unit | Frozen key | Observed | Predicted | Rel error % | Pass <=1% |",
        "|:--|:--|:--|--:|--:|--:|:--|",
    ]
    for row in worst_mapped:
        lines.append(
            f"| `{row.name}` | `{row.unit}` | `{row.frozen_formula_key}` | `{fmt(row.value)}` | `{fmt(row.frozen_predicted)}` | `{fmt(row.frozen_relative_error_percent)}` | `{row.frozen_pass_1_percent}` |"
        )
    lines += [
        "",
        "## Missing Frozen Formulas",
        "",
        f"The frozen BIP39 registry has no formula for `{len(missing)}` catalog constants.",
        "First 80 missing constants:",
        "",
        "| Constant | Unit | Value |",
        "|:--|:--|--:|",
    ]
    for row in missing[:80]:
        lines.append(f"| `{row.name}` | `{row.unit}` | `{fmt(row.value)}` |")
    lines += [
        "",
        "## Sparse Search Diagnostic For Dimensionless Constants",
        "",
        "These rows show how well a BIP39 monomial search can approximate dimensionless constants.",
        "Because formulas are selected after seeing each target, this is a look-elsewhere diagnostic, not a no-fit proof.",
        "",
        "| Constant | Value | Predicted | Rel error % | Complexity | Formula |",
        "|:--|--:|--:|--:|--:|:--|",
    ]
    for row in sparse_dimless_sorted[:80]:
        lines.append(
            f"| `{row.name}` | `{fmt(row.value)}` | `{fmt(row.sparse_predicted)}` | `{fmt(row.sparse_relative_error_percent)}` | {row.sparse_complexity} | `{row.sparse_formula}` |"
        )
    lines += [
        "",
        "## Scientific Reading",
        "",
        "The frozen BIP39 no-fit model does not yet provide formulas for the 300+ CODATA catalog.",
        "It covers only the small set frozen in v6, with a few aliases visible in the SciPy catalog.",
        "The sparse-search diagnostic can approximate many numbers, but that is exactly the curve-fitting risk unless the formula-selection rule is frozen before the target is known.",
        "Dimensional constants are especially strict: a dimensionless BIP39 monomial cannot predict their SI numerical values without a declared unit basis.",
        "",
    ]
    (RESULTS / "bip39_all_constants_benchmark_v7_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows, summary = evaluate()
    payload = {
        "summary": [asdict(row) for row in summary],
        "rows": [asdict(row) for row in rows],
    }
    (RESULTS / "bip39_all_constants_benchmark_v7.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "bip39_all_constants_benchmark_v7.csv", [asdict(row) for row in rows])
    write_report(rows, summary)
    for row in summary:
        print(f"{row.metric}: {row.value}")
    print(RESULTS / "bip39_all_constants_benchmark_v7_report.md")


if __name__ == "__main__":
    main()
