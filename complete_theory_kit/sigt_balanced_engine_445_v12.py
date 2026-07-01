#!/usr/bin/env python3
"""SIGT balanced falsification engine for all 445 constants.

This is the user's controlled-hypothesis-space sketch scaled to the full
SciPy/CODATA catalog.

Two modes are evaluated:

1. LEAKY_VALUE_ENGINE
   x is the observed constant itself.  The identity hypothesis x therefore
   wins with zero error.  This is a leakage demonstration, not prediction.

2. BIP39_PRIOR_ENGINE
   x is the BIP39 sparse prior prediction from v8.  The target value is not
   passed as x.  This is the honest balanced falsification score.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from bip39_fit_all_445_v8 import Fit445Row, evaluate as evaluate_v8


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


@dataclass
class Constant:
    name: str
    value: float
    train: bool
    unit: str
    x_leaky: float
    x_bip39_prior: float


@dataclass
class FitRow:
    engine: str
    name: str
    split: str
    unit: str
    model_id: int
    model_name: str
    x_value: float
    observed: float
    predicted: float
    absolute_error: float
    relative_error_percent: float
    complexity: float
    mdl_score: float
    leakage_flag: bool


@dataclass
class SummaryRow:
    engine: str
    avg_test_abs_error: float
    median_test_relative_error_percent: float
    pass_1_percent_test: int
    test_count: int
    complexity_penalty: float
    collapse_penalty: float
    final_score: float
    registry_size: int
    unique_model_ids: int
    verdict: str


def deterministic_train(name: str) -> bool:
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 5 != 0


def constants_from_v8() -> list[Constant]:
    rows, _summary = evaluate_v8()
    constants: list[Constant] = []
    for row in rows:
        constants.append(
            Constant(
                name=row.name,
                value=row.value,
                train=deterministic_train(row.name),
                unit=row.unit,
                x_leaky=row.value,
                x_bip39_prior=row.sparse_signed_predicted,
            )
        )
    return constants


def hypothesis_space(x: float) -> list[tuple[str, float]]:
    """Controlled expressive family: finite and intentionally small."""
    ax = abs(x)
    safe_log = math.log(ax + 1e-300)
    safe_sqrt = math.sqrt(ax)
    safe_exp = math.exp(-min(ax, 700.0))
    return [
        ("x", x),
        ("x^2", math.copysign(ax * ax, x)),
        ("sqrt(abs(x))", safe_sqrt),
        ("log(abs(x)+eps)", safe_log),
        ("exp(-abs(x))", safe_exp),
        ("x/(1+abs(x))", x / (1.0 + ax)),
        ("-x", -x),
        ("1/x", 1.0 / x if x != 0 else float("inf")),
        ("sign(x)", 1.0 if x >= 0 else -1.0),
    ]


def complexity(idx: int) -> float:
    return 1.0 + 0.3 * idx


def mdl(error: float, comp: float) -> float:
    return math.log1p(error) + comp


def rel_error_percent(predicted: float, observed: float) -> float:
    if observed == 0 or not math.isfinite(predicted) or not math.isfinite(observed):
        return float("inf")
    return abs(predicted - observed) / abs(observed) * 100.0


def fit_constant(c: Constant, engine: str) -> FitRow:
    x = c.x_leaky if engine == "LEAKY_VALUE_ENGINE" else c.x_bip39_prior
    candidates = hypothesis_space(x)
    best: tuple[int, str, float, float, float] | None = None
    best_score = float("inf")
    for idx, (name, pred) in enumerate(candidates):
        if not math.isfinite(pred):
            continue
        error = abs(pred - c.value)
        comp = complexity(idx)
        score = mdl(error, comp)
        if score < best_score:
            best_score = score
            best = (idx, name, pred, error, comp)
    assert best is not None
    idx, name, pred, error, comp = best
    return FitRow(
        engine=engine,
        name=c.name,
        split="train" if c.train else "test",
        unit=c.unit,
        model_id=idx,
        model_name=name,
        x_value=x,
        observed=c.value,
        predicted=pred,
        absolute_error=error,
        relative_error_percent=rel_error_percent(pred, c.value),
        complexity=comp,
        mdl_score=best_score,
        leakage_flag=(engine == "LEAKY_VALUE_ENGINE"),
    )


class Registry:
    def __init__(self) -> None:
        self.map: dict[str, list[int]] = {}
        self.model_counts: dict[int, int] = {}

    def add(self, name: str, model_id: int) -> None:
        self.map.setdefault(name, []).append(model_id)
        self.model_counts[model_id] = self.model_counts.get(model_id, 0) + 1

    def uniqueness_penalty(self) -> float:
        return 0.01 * sum(len(v) for v in self.map.values())

    def collapse_penalty(self) -> float:
        repeated = sum(max(0, count - 1) for count in self.model_counts.values())
        return 0.02 * repeated


def evaluate_engine(constants: list[Constant], engine: str) -> tuple[list[FitRow], SummaryRow]:
    registry = Registry()
    rows = [fit_constant(c, engine) for c in constants]
    for row in rows:
        if row.split == "train":
            registry.add(row.name, row.model_id)

    test_rows = [row for row in rows if row.split == "test"]
    avg_error = float(np.mean([row.absolute_error for row in test_rows]))
    median_rel = float(np.median([row.relative_error_percent for row in test_rows]))
    pass_1 = sum(row.relative_error_percent <= 1.0 for row in test_rows)
    complexity_pen = registry.uniqueness_penalty()
    collapse_pen = registry.collapse_penalty()
    final_score = math.log1p(avg_error) + complexity_pen + collapse_pen
    unique_ids = len({row.model_id for row in rows})
    if engine == "LEAKY_VALUE_ENGINE":
        verdict = "TRIVIAL_TARGET_LEAKAGE: identity hypothesis sees the answer"
    elif pass_1 == len(test_rows):
        verdict = "PASS_BALANCED_TEST"
    else:
        verdict = "FAIL_BALANCED_TEST: finite hypothesis space does not predict held-out constants"
    return rows, SummaryRow(
        engine=engine,
        avg_test_abs_error=avg_error,
        median_test_relative_error_percent=median_rel,
        pass_1_percent_test=pass_1,
        test_count=len(test_rows),
        complexity_penalty=complexity_pen,
        collapse_penalty=collapse_pen,
        final_score=final_score,
        registry_size=len(registry.map),
        unique_model_ids=unique_ids,
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


def write_report(rows: list[FitRow], summaries: list[SummaryRow]) -> None:
    lines = [
        "# SIGT Balanced Engine 445 v12",
        "",
        "This is the controlled finite hypothesis-space engine scaled to all 445 constants.",
        "",
        "## Hypothesis Space",
        "",
        "```text",
        "x",
        "x^2",
        "sqrt(abs(x))",
        "log(abs(x)+eps)",
        "exp(-abs(x))",
        "x/(1+abs(x))",
        "-x",
        "1/x",
        "sign(x)",
        "```",
        "",
        "## Summary",
        "",
        "| Engine | Test pass <=1% | Median test rel error % | Avg abs error | Complexity penalty | Collapse penalty | Final score | Verdict |",
        "|:--|--:|--:|--:|--:|--:|--:|:--|",
    ]
    for s in summaries:
        lines.append(
            f"| `{s.engine}` | {s.pass_1_percent_test}/{s.test_count} | `{fmt(s.median_test_relative_error_percent)}` | `{fmt(s.avg_test_abs_error)}` | `{fmt(s.complexity_penalty)}` | `{fmt(s.collapse_penalty)}` | `{fmt(s.final_score)}` | `{s.verdict}` |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "`LEAKY_VALUE_ENGINE` reproduces the target because x is the observed value.",
        "`BIP39_PRIOR_ENGINE` uses the BIP39 sparse prior as x and is therefore the honest falsification mode.",
        "",
        "## Worst BIP39 Prior Test Rows",
        "",
        "| Constant | Unit | Model | Observed | Predicted | Rel error % |",
        "|:--|:--|:--|--:|--:|--:|",
    ]
    bip_test = [row for row in rows if row.engine == "BIP39_PRIOR_ENGINE" and row.split == "test"]
    for row in sorted(bip_test, key=lambda item: item.relative_error_percent, reverse=True)[:80]:
        lines.append(
            f"| `{row.name}` | `{row.unit}` | `{row.model_name}` | `{fmt(row.observed)}` | `{fmt(row.predicted)}` | `{fmt(row.relative_error_percent)}` |"
        )
    lines += [
        "",
        "## Scientific Status",
        "",
        "The balanced engine is useful because it exposes leakage.",
        "Perfect performance in leaky mode is not evidence.",
        "The BIP39 prior mode is the actual predictive test.",
        "",
    ]
    (RESULTS / "sigt_balanced_engine_445_v12_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    constants = constants_from_v8()
    all_rows: list[FitRow] = []
    summaries: list[SummaryRow] = []
    for engine in ["LEAKY_VALUE_ENGINE", "BIP39_PRIOR_ENGINE"]:
        rows, summary = evaluate_engine(constants, engine)
        all_rows.extend(rows)
        summaries.append(summary)
    payload = {
        "summaries": [asdict(s) for s in summaries],
        "rows": [asdict(row) for row in all_rows],
    }
    (RESULTS / "sigt_balanced_engine_445_v12.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "sigt_balanced_engine_445_v12.csv", [asdict(row) for row in all_rows])
    write_report(all_rows, summaries)
    print("SIGT_BALANCED_ENGINE_445_V12: OK")
    for s in summaries:
        print(f"{s.engine}: {s.verdict}; pass_1={s.pass_1_percent_test}/{s.test_count}; final_score={s.final_score:.12g}")
    print(RESULTS / "sigt_balanced_engine_445_v12_report.md")


if __name__ == "__main__":
    main()
