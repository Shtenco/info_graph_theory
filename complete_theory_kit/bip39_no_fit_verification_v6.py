#!/usr/bin/env python3
"""Frozen no-fit verification for the BIP39 sparse formulas.

v5 was a search layer.  This v6 layer is different: it disables search and
verifies a frozen formula registry.  The target-calibrated branch is audited
only to demonstrate why exact coefficients are not a proof.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from bip39_unification_search_v5 import (
    M_E_MEV,
    Target,
    bip39,
    feature_values,
    log10_error,
    targets,
)


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


FROZEN_FORMULAS = {
    "alpha": {
        "base": 1.0,
        "factors": {"K": -1, "lnDict": -1, "U": -1},
        "text": "K^-1 * lnDict^-1 * U^-1",
    },
    "alpha_s_mZ": {
        "base": 1.0,
        "factors": {"K": -1, "bits": -1, "bip_density": -1},
        "text": "K^-1 * bits^-1 * bip_density^-1",
    },
    "g_I_squared": {
        "base": 1.0,
        "factors": {"K": 1, "lnDict": -1},
        "text": "K * lnDict^-1",
    },
    "infoton_mass_micro_eV": {
        "base": M_E_MEV * 1e12,
        "factors": {"dict": -2, "entropy": -2, "U": 1},
        "text": "m_e[micro-eV] * dict^-2 * entropy^-2 * U",
    },
    "proton_mass_MeV": {
        "base": M_E_MEV,
        "factors": {"pi": 1, "words": 2},
        "text": "m_e * pi * words^2",
    },
    "W_mass_GeV": {
        "base": M_E_MEV / 1000.0,
        "factors": {"K": 1, "entropy": 1, "f1": 1},
        "text": "m_e[GeV] * K * entropy * f1",
    },
    "Z_mass_GeV": {
        "base": M_E_MEV / 1000.0,
        "factors": {"dict": 1, "total_bits": 1, "U": -1},
        "text": "m_e[GeV] * dict * total_bits / U",
    },
    "H_mass_GeV": {
        "base": M_E_MEV / 1000.0,
        "factors": {"bits": 2, "dict": 1},
        "text": "m_e[GeV] * bits^2 * dict",
    },
    "sin2_thetaW": {
        "base": 1.0,
        "factors": {"checksum": -1, "lnK": 1},
        "text": "lnK / checksum",
    },
    "G_F_GeV_minus2": {
        "base": 1.0,
        "factors": {"pi": -1, "total_bits": -1, "f1": -1},
        "text": "1 / (pi * total_bits * f1)",
    },
    "Lambda_QCD_GeV": {
        "base": 1.0,
        "factors": {"lnK": -1, "U": 1, "bip_density": 1},
        "text": "U * bip_density / lnK",
    },
}


@dataclass
class FrozenRow:
    target: str
    observed: float
    predicted: float
    absolute_error: float
    relative_error_percent: float
    log10_error: float
    readme_tolerance_log10: float
    pass_readme_tolerance: bool
    pass_one_percent: bool
    pass_half_percent: bool
    pass_tenth_percent: bool
    formula: str
    coefficient_needed_for_exact_fit: float
    coefficient_deviation_percent: float
    no_fit_status: str


@dataclass
class ThresholdSummary:
    threshold: str
    pass_count: int
    target_count: int


def formula_registry_hash() -> str:
    stable = json.dumps(FROZEN_FORMULAS, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()


def evaluate_formula(target: Target, features: dict[str, float]) -> FrozenRow:
    spec = FROZEN_FORMULAS[target.name]
    predicted = float(spec["base"])
    complexity = 0
    for name, exponent in spec["factors"].items():
        predicted *= features[name] ** exponent
        complexity += abs(exponent)
    err = log10_error(predicted, target.observed)
    rel_percent = abs(predicted - target.observed) / abs(target.observed) * 100.0
    coeff = target.observed / predicted
    coeff_dev = abs(coeff - 1.0) * 100.0
    no_fit_status = "NO_FIT_VERIFIED"
    if complexity > 5:
        no_fit_status = "NO_FIT_VERIFIED_HIGH_COMPLEXITY"
    return FrozenRow(
        target=target.name,
        observed=target.observed,
        predicted=predicted,
        absolute_error=abs(predicted - target.observed),
        relative_error_percent=rel_percent,
        log10_error=err,
        readme_tolerance_log10=target.tolerance_log10,
        pass_readme_tolerance=err <= target.tolerance_log10,
        pass_one_percent=rel_percent <= 1.0,
        pass_half_percent=rel_percent <= 0.5,
        pass_tenth_percent=rel_percent <= 0.1,
        formula=str(spec["text"]),
        coefficient_needed_for_exact_fit=coeff,
        coefficient_deviation_percent=coeff_dev,
        no_fit_status=no_fit_status,
    )


def summaries(rows: list[FrozenRow]) -> list[ThresholdSummary]:
    return [
        ThresholdSummary("README log tolerance", sum(r.pass_readme_tolerance for r in rows), len(rows)),
        ThresholdSummary("relative <= 1%", sum(r.pass_one_percent for r in rows), len(rows)),
        ThresholdSummary("relative <= 0.5%", sum(r.pass_half_percent for r in rows), len(rows)),
        ThresholdSummary("relative <= 0.1%", sum(r.pass_tenth_percent for r in rows), len(rows)),
    ]


def final_verdict(rows: list[FrozenRow]) -> str:
    if not all(r.pass_readme_tolerance for r in rows):
        return "FAIL_NO_FIT: at least one frozen BIP39 formula misses README tolerance"
    if sum(r.pass_one_percent for r in rows) < len(rows):
        return "PASS_README_TOLERANCE_ONLY: no fitting, but not all constants are within 1%"
    if sum(r.pass_half_percent for r in rows) < len(rows):
        return "PASS_NO_FIT_1_PERCENT: no fitting, all constants within 1%, not all within 0.5%"
    return "STRONG_NUMERIC_NO_FIT_HIT: no fitting, all constants within 0.5%; still requires future blind targets"


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return "inf"
    return f"{value:.12g}"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[FrozenRow], threshold_rows: list[ThresholdSummary], verdict: str, registry_hash: str) -> None:
    mean_rel = sum(r.relative_error_percent for r in rows) / len(rows)
    max_rel = max(r.relative_error_percent for r in rows)
    mean_coeff_dev = sum(r.coefficient_deviation_percent for r in rows) / len(rows)
    lines = [
        "# BIP39 No-Fit Verification v6",
        "",
        f"Final verdict: `{verdict}`",
        "",
        "## What Changed From v5",
        "",
        "v5 searched formula space. v6 does not search.",
        "v6 uses a frozen registry of the 11 sparse BIP39 formulas and only recomputes their predictions.",
        "Target-calibrated coefficients are not used for prediction; they are reported only as an audit of how much exact fitting would change each result.",
        "",
        f"Frozen formula registry SHA256: `{registry_hash}`",
        "",
        "## Precision Summary",
        "",
        f"- `mean_relative_error_percent = {fmt(mean_rel)}`",
        f"- `max_relative_error_percent = {fmt(max_rel)}`",
        f"- `mean_exact_fit_coefficient_deviation_percent = {fmt(mean_coeff_dev)}`",
        "",
        "| Threshold | Pass |",
        "|:--|--:|",
    ]
    for row in threshold_rows:
        lines.append(f"| `{row.threshold}` | {row.pass_count}/{row.target_count} |")
    lines += [
        "",
        "## Frozen No-Fit Formulas",
        "",
        "| Target | Formula | Observed | Predicted | Rel error % | log10 error | README pass | <=1% | <=0.5% | <=0.1% | Exact-fit coefficient |",
        "|:--|:--|--:|--:|--:|--:|:--|:--|:--|:--|--:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row.target}` | `{row.formula}` | `{fmt(row.observed)}` | `{fmt(row.predicted)}` | `{fmt(row.relative_error_percent)}` | `{fmt(row.log10_error)}` | `{row.pass_readme_tolerance}` | `{row.pass_one_percent}` | `{row.pass_half_percent}` | `{row.pass_tenth_percent}` | `{fmt(row.coefficient_needed_for_exact_fit)}` |"
        )
    lines += [
        "",
        "## Calibration Audit",
        "",
        "The branch `BIP39_TARGET_CALIBRATED` can force 11/11 by multiplying each row by a target-specific coefficient.",
        "v6 rejects that as proof. The coefficient column above shows how close such exact-fit constants would be to 1, but they are not used.",
        "",
        "## Scientific Status",
        "",
        "This is the strongest current BIP39 result in the package: frozen formulas, no fitted coefficients, no search during verification.",
        "It is still not a final physical proof because the formulas were discovered before this freeze.",
        "The next gate is future blind prediction with this exact registry hash unchanged.",
        "",
    ]
    (RESULTS / "bip39_no_fit_verification_v6_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    inv = bip39()
    features = feature_values(inv)
    rows = [evaluate_formula(target, features) for target in targets()]
    threshold_rows = summaries(rows)
    verdict = final_verdict(rows)
    registry_hash = formula_registry_hash()
    payload = {
        "verdict": verdict,
        "registry_hash_sha256": registry_hash,
        "formula_registry": FROZEN_FORMULAS,
        "bip39": asdict(inv),
        "features": features,
        "thresholds": [asdict(row) for row in threshold_rows],
        "rows": [asdict(row) for row in rows],
    }
    (RESULTS / "bip39_no_fit_verification_v6.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "bip39_no_fit_verification_v6.csv", [asdict(row) for row in rows])
    write_report(rows, threshold_rows, verdict, registry_hash)
    print(verdict)
    for row in threshold_rows:
        print(f"{row.threshold}: {row.pass_count}/{row.target_count}")
    print(RESULTS / "bip39_no_fit_verification_v6_report.md")


if __name__ == "__main__":
    main()
