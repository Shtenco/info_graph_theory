#!/usr/bin/env python3
"""Attempt to obtain full predictive victory for the 445-constant SIGT/BIP39 set.

The script compares several increasingly powerful engines:

1. HONEST_BIP39_PRIOR
   Uses the v8 BIP39 sparse prior directly.

2. TRAINED_GLOBAL_CALIBRATION
   Learns one global calibration coefficient from train only.

3. TRAINED_UNIT_SECTOR_CALIBRATION
   Learns calibration medians by unit and sector from train only.

4. ORACLE_CATALOG_LOOKUP
   Uses each target's own exact coefficient. This reaches 100%, but is marked
   as target leakage and does not count as physical prediction.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from bip39_fit_all_445_v8 import Fit445Row, evaluate as evaluate_v8
from bip39_symbolic_approximator_v11 import deterministic_split, sector_of


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


@dataclass
class VictoryRow:
    engine: str
    name: str
    split: str
    unit: str
    sector: str
    observed: float
    predicted: float
    relative_error_percent: float
    pass_1_percent: bool
    pass_0_1_percent: bool
    leakage_status: str


@dataclass
class VictorySummary:
    engine: str
    train_pass_1_percent: str
    test_pass_1_percent: str
    test_pass_0_1_percent: str
    test_median_relative_error_percent: float
    test_max_relative_error_percent: float
    victory_claim: str
    verdict: str


def rel_error_percent(predicted: float, observed: float) -> float:
    if observed == 0 or not math.isfinite(predicted):
        return float("inf")
    return abs(predicted - observed) / abs(observed) * 100.0


def safe_median(values: list[float], default: float = 1.0) -> float:
    finite = [v for v in values if math.isfinite(v) and v > 0]
    if not finite:
        return default
    return float(np.median(finite))


def calibration_maps(train: list[Fit445Row]) -> tuple[float, dict[str, float], dict[str, float], dict[tuple[str, str], float]]:
    coeffs = [row.exact_calibration_coefficient for row in train]
    global_coeff = safe_median(coeffs)
    by_unit: dict[str, float] = {}
    by_sector: dict[str, float] = {}
    by_pair: dict[tuple[str, str], float] = {}
    units = sorted({row.unit for row in train})
    sectors = sorted({sector_of(row) for row in train})
    for unit in units:
        by_unit[unit] = safe_median([row.exact_calibration_coefficient for row in train if row.unit == unit], global_coeff)
    for sector in sectors:
        by_sector[sector] = safe_median([row.exact_calibration_coefficient for row in train if sector_of(row) == sector], global_coeff)
    for unit in units:
        for sector in sectors:
            vals = [row.exact_calibration_coefficient for row in train if row.unit == unit and sector_of(row) == sector]
            if vals:
                by_pair[(unit, sector)] = safe_median(vals, global_coeff)
    return global_coeff, by_unit, by_sector, by_pair


def predict(row: Fit445Row, engine: str, maps: tuple[float, dict[str, float], dict[str, float], dict[tuple[str, str], float]]) -> tuple[float, str]:
    global_coeff, by_unit, by_sector, by_pair = maps
    sector = sector_of(row)
    if engine == "HONEST_BIP39_PRIOR":
        return row.sparse_signed_predicted, "NO_TARGET_VALUE"
    if engine == "TRAINED_GLOBAL_CALIBRATION":
        return row.sparse_signed_predicted * global_coeff, "TRAIN_ONLY_GLOBAL"
    if engine == "TRAINED_UNIT_SECTOR_CALIBRATION":
        coeff = by_pair.get((row.unit, sector), by_unit.get(row.unit, by_sector.get(sector, global_coeff)))
        return row.sparse_signed_predicted * coeff, "TRAIN_ONLY_UNIT_SECTOR"
    if engine == "ORACLE_CATALOG_LOOKUP":
        return row.sparse_signed_predicted * row.exact_calibration_coefficient, "TARGET_LEAKAGE_EXACT_COEFFICIENT"
    raise ValueError(engine)


def evaluate_engine(rows: list[Fit445Row], engine: str, maps: tuple[float, dict[str, float], dict[str, float], dict[tuple[str, str], float]]) -> tuple[list[VictoryRow], VictorySummary]:
    out: list[VictoryRow] = []
    for row in rows:
        pred, leakage = predict(row, engine, maps)
        err = rel_error_percent(pred, row.value)
        out.append(
            VictoryRow(
                engine=engine,
                name=row.name,
                split=deterministic_split(row.name),
                unit=row.unit,
                sector=sector_of(row),
                observed=row.value,
                predicted=pred,
                relative_error_percent=err,
                pass_1_percent=err <= 1.0,
                pass_0_1_percent=err <= 0.1,
                leakage_status=leakage,
            )
        )
    train = [r for r in out if r.split == "train"]
    test = [r for r in out if r.split == "test"]
    test_errors = [r.relative_error_percent for r in test]
    train_pass = sum(r.pass_1_percent for r in train)
    test_pass = sum(r.pass_1_percent for r in test)
    test_pass_01 = sum(r.pass_0_1_percent for r in test)
    if engine == "ORACLE_CATALOG_LOOKUP":
        victory = "FULL_NUMERIC_VICTORY"
        verdict = "REJECT_AS_PREDICTION: uses each target exact coefficient"
    elif test_pass == len(test):
        victory = "FULL_HONEST_TEST_VICTORY"
        verdict = "SUPPORTED_ON_CURRENT_SPLIT"
    else:
        victory = "NO_FULL_TEST_VICTORY"
        verdict = "FULL_PREDICTIVE_VICTORY_NOT_ACHIEVED"
    return out, VictorySummary(
        engine=engine,
        train_pass_1_percent=f"{train_pass}/{len(train)}",
        test_pass_1_percent=f"{test_pass}/{len(test)}",
        test_pass_0_1_percent=f"{test_pass_01}/{len(test)}",
        test_median_relative_error_percent=float(np.median(test_errors)),
        test_max_relative_error_percent=max(test_errors),
        victory_claim=victory,
        verdict=verdict,
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return "inf"
    return f"{value:.12g}"


def write_report(all_rows: list[VictoryRow], summaries: list[VictorySummary]) -> None:
    lines = [
        "# SIGT Predictive Victory Attempt v13",
        "",
        "This report attempts to force full predictive victory while separating honest prediction from leakage.",
        "",
        "## Leaderboard",
        "",
        "| Engine | Train <=1% | Test <=1% | Test <=0.1% | Test median rel error % | Test max rel error % | Victory | Verdict |",
        "|:--|--:|--:|--:|--:|--:|:--|:--|",
    ]
    for s in summaries:
        lines.append(
            f"| `{s.engine}` | {s.train_pass_1_percent} | {s.test_pass_1_percent} | {s.test_pass_0_1_percent} | `{fmt(s.test_median_relative_error_percent)}` | `{fmt(s.test_max_relative_error_percent)}` | `{s.victory_claim}` | `{s.verdict}` |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "Full 80/80 test victory is possible only in `ORACLE_CATALOG_LOOKUP`, which uses each held-out target's exact coefficient.",
        "That is calibrated symbolic closure, not predictive physics.",
        "The honest engines do not achieve full held-out victory on the current 445-constant benchmark.",
        "",
        "## Worst Honest Engine Test Rows",
        "",
        "| Constant | Unit | Sector | Observed | Predicted | Rel error % |",
        "|:--|:--|:--|--:|--:|--:|",
    ]
    honest_test = [
        row for row in all_rows
        if row.engine == "TRAINED_UNIT_SECTOR_CALIBRATION" and row.split == "test"
    ]
    for row in sorted(honest_test, key=lambda r: r.relative_error_percent, reverse=True)[:80]:
        lines.append(
            f"| `{row.name}` | `{row.unit}` | `{row.sector}` | `{fmt(row.observed)}` | `{fmt(row.predicted)}` | `{fmt(row.relative_error_percent)}` |"
        )
    lines += [
        "",
        "## Final Status",
        "",
        "The system has perfect calibrated symbolic convergence.",
        "It does not yet have full honest predictive victory.",
        "",
    ]
    (RESULTS / "sigt_predictive_victory_attempt_v13_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    v8_rows, _ = evaluate_v8()
    train_rows = [row for row in v8_rows if deterministic_split(row.name) == "train"]
    maps = calibration_maps(train_rows)
    engines = [
        "HONEST_BIP39_PRIOR",
        "TRAINED_GLOBAL_CALIBRATION",
        "TRAINED_UNIT_SECTOR_CALIBRATION",
        "ORACLE_CATALOG_LOOKUP",
    ]
    all_rows: list[VictoryRow] = []
    summaries: list[VictorySummary] = []
    for engine in engines:
        rows, summary = evaluate_engine(v8_rows, engine, maps)
        all_rows.extend(rows)
        summaries.append(summary)
    payload = {
        "summaries": [asdict(s) for s in summaries],
        "rows": [asdict(row) for row in all_rows],
    }
    (RESULTS / "sigt_predictive_victory_attempt_v13.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "sigt_predictive_victory_attempt_v13.csv", [asdict(row) for row in all_rows])
    write_report(all_rows, summaries)
    print("SIGT_PREDICTIVE_VICTORY_ATTEMPT_V13: OK")
    for s in summaries:
        print(f"{s.engine}: {s.test_pass_1_percent}; {s.victory_claim}; {s.verdict}")
    print(RESULTS / "sigt_predictive_victory_attempt_v13_report.md")


if __name__ == "__main__":
    main()
