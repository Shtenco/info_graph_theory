#!/usr/bin/env python3
"""Reduced-model optimizer and blind-prediction scaffold v2.

This script tries to rescue the information-graph program in the only honest
way: reduce formula freedom, fit only on a declared training set, evaluate on
known holdout constants, and emit a frozen registry for future blind tests.

It does not claim a physical proof. It reports whether the optimized reduced
model earns a provisional status under strict anti-overfitting rules.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


K = 6.0
P = 4.8027e-42
N = 4.197668e121
M_E_MEV = 0.51099895
PI = math.pi
LN_K = math.log(K)
LN_N = math.log(N)
F1 = 104.37
F2 = LN_K
F3 = math.sqrt(K * P)
F4 = 1.0 / P
F5 = K / LN_K
F6 = 1.0527
ALPHA_GRAPH = 2.0 * LN_K**2 / (PI * LN_N)


FEATURES = {
    "K": K,
    "pi": PI,
    "lnK": LN_K,
    "U": math.log(N) / abs(math.log(K * P)),
    "f1": F1,
    "f2": F2,
    "f5": F5,
    "f6": F6,
}


@dataclass
class Target:
    name: str
    value: float
    unit: str
    family: str
    split: str
    tolerance_log10: float


@dataclass
class FormulaCandidate:
    family: str
    base: str
    coefficient: float
    exponents: dict[str, int]
    train_mean_log10_error: float
    complexity: int
    objective: float


@dataclass
class PredictionRow:
    model: str
    target: str
    split: str
    family: str
    true_value: float
    predicted: float | None
    log10_error: float
    tolerance_log10: float
    passed: bool
    formula: str
    notes: str


def targets() -> list[Target]:
    return [
        Target("W_mass_MeV", 80379.0, "MeV", "mass", "train", 0.01),
        Target("Z_mass_MeV", 91187.6, "MeV", "mass", "train", 0.01),
        Target("H_mass_MeV", 125200.0, "MeV", "mass", "train", 0.02),
        Target("alpha", 1.0 / 137.035999084, "dimensionless", "coupling", "train", 0.002),
        Target("proton_mass_MeV", 938.2720813, "MeV", "mass", "holdout", 0.01),
        Target("neutron_mass_MeV", 939.5654133, "MeV", "mass", "holdout", 0.01),
        Target("tau_mass_MeV", 1776.86, "MeV", "mass", "holdout", 0.02),
        Target("alpha_s_mZ", 0.1181, "dimensionless", "coupling", "holdout", 0.03),
        Target("sin2_thetaW", 0.223, "dimensionless", "coupling", "holdout", 0.02),
        Target("G_F_GeV_minus2", 1.1663787e-5, "GeV^-2", "weak_dimensional", "holdout", 0.05),
        Target("planck_mass_GeV", 1.22089e19, "GeV", "gravity_dimensional", "holdout", 0.05),
        Target("cosmological_constant_m_minus2", 1.089e-52, "m^-2", "cosmology", "holdout", 0.2),
        Target("Lambda_QCD_GeV", 0.217, "GeV", "strong_scale", "holdout", 0.05),
        Target("binding_energy_Fe56_MeV", 8.79, "MeV", "nuclear", "holdout", 0.02),
    ]


def log10_error(predicted: float | None, true_value: float) -> float:
    if predicted is None or predicted <= 0 or not math.isfinite(predicted):
        return float("inf")
    return abs(math.log10(predicted / true_value))


def monomial_value(exponents: dict[str, int]) -> float:
    value = 1.0
    for name, exponent in exponents.items():
        value *= FEATURES[name] ** exponent
    return value


def complexity_of(exponents: dict[str, int], has_coefficient: bool) -> int:
    return sum(abs(v) for v in exponents.values()) + (1 if has_coefficient else 0)


def formula_text(base: str, coefficient: float, exponents: dict[str, int]) -> str:
    parts = [base]
    if abs(math.log10(coefficient)) > 1e-12:
        parts.append(f"C_global({coefficient:.6g})")
    for key, exponent in exponents.items():
        if exponent:
            parts.append(f"{key}^{exponent}")
    return " * ".join(parts)


def optimize_mass_family(all_targets: list[Target]) -> FormulaCandidate:
    train = [t for t in all_targets if t.family == "mass" and t.split == "train"]
    names = ["K", "pi", "U", "f1", "f5", "f6"]
    best: FormulaCandidate | None = None
    exponent_range = range(-2, 3)
    for values in itertools.product(exponent_range, repeat=len(names)):
        exponents = dict(zip(names, values))
        raw = M_E_MEV * monomial_value(exponents)
        if raw <= 0 or not math.isfinite(raw):
            continue
        log_offsets = [math.log10(t.value / raw) for t in train]
        coefficient = 10 ** (sum(log_offsets) / len(log_offsets))
        errors = [log10_error(coefficient * raw, t.value) for t in train]
        mean_error = sum(errors) / len(errors)
        complexity = complexity_of(exponents, has_coefficient=True)
        objective = mean_error + 0.01 * complexity
        candidate = FormulaCandidate("mass", "m_e", coefficient, exponents, mean_error, complexity, objective)
        if best is None or candidate.objective < best.objective:
            best = candidate
    assert best is not None
    return best


def predict_reduced(candidate: FormulaCandidate, target: Target) -> tuple[float | None, str, str]:
    if target.family == "mass":
        value = M_E_MEV * candidate.coefficient * monomial_value(candidate.exponents)
        return value, formula_text(candidate.base, candidate.coefficient, candidate.exponents), "optimized shared mass formula"
    if target.name == "alpha":
        return ALPHA_GRAPH, "2 lnK^2 / (pi lnN)", "fixed graph alpha formula"
    if target.name == "alpha_s_mZ":
        return (PI**3 / 2.0) * ALPHA_GRAPH, "pi^3 alpha / 2", "fixed relation, no refit"
    if target.name == "sin2_thetaW":
        return 0.2146, "uncorrected weak proxy", "fixed existing proxy"
    return None, "MISSING", "no dimensionally complete reduced formula registered"


def predict_dimensional(target: Target) -> tuple[float | None, str, str]:
    guesses = {
        "mass": 1_000.0,
        "coupling": 0.1,
        "weak_dimensional": 1e-5,
        "gravity_dimensional": 1e19,
        "cosmology": 1e-52,
        "strong_scale": 0.2,
        "nuclear": 8.0,
    }
    return guesses.get(target.family, 1.0), "category scale", "dimensional baseline"


def predict_random(target: Target) -> tuple[float | None, str, str]:
    rng = random.Random("v2:" + target.name)
    center = math.log10(target.value)
    return 10 ** rng.uniform(center - 3.0, center + 3.0), "log-uniform +/-3 decades", "favorable random baseline"


def evaluate_model(model: str, all_targets: list[Target], candidate: FormulaCandidate) -> list[PredictionRow]:
    rows: list[PredictionRow] = []
    for target in all_targets:
        if model == "REDUCED_GRAPH_OPTIMIZED_V2":
            predicted, formula, notes = predict_reduced(candidate, target)
        elif model == "DIMENSIONAL_BASELINE":
            predicted, formula, notes = predict_dimensional(target)
        elif model == "RANDOM_LOG_BASELINE":
            predicted, formula, notes = predict_random(target)
        else:
            raise ValueError(model)
        err = log10_error(predicted, target.value)
        rows.append(
            PredictionRow(
                model=model,
                target=target.name,
                split=target.split,
                family=target.family,
                true_value=target.value,
                predicted=predicted,
                log10_error=err,
                tolerance_log10=target.tolerance_log10,
                passed=err <= target.tolerance_log10,
                formula=formula,
                notes=notes,
            )
        )
    return rows


def summarize(rows: list[PredictionRow], split: str) -> dict[str, object]:
    selected = [r for r in rows if r.split == split]
    finite = [r.log10_error for r in selected if math.isfinite(r.log10_error)]
    missing = len(selected) - len(finite)
    return {
        "model": selected[0].model if selected else "NONE",
        "split": split,
        "pass_count": sum(1 for r in selected if r.passed),
        "target_count": len(selected),
        "missing_count": missing,
        "mean_log10_error": float("inf") if missing else sum(finite) / len(finite),
        "max_log10_error": float("inf") if missing else max(finite),
    }


def verdict(summaries: list[dict[str, object]]) -> str:
    graph = next(s for s in summaries if s["model"] == "REDUCED_GRAPH_OPTIMIZED_V2" and s["split"] == "holdout")
    baselines = [s for s in summaries if s["model"] != "REDUCED_GRAPH_OPTIMIZED_V2" and s["split"] == "holdout"]
    best_baseline = min(baselines, key=lambda s: float(s["mean_log10_error"]))
    if int(graph["missing_count"]) > 0:
        return "NOT_PHYSICS_CURRENT_FORM: reduced model still has missing dimensionally complete predictions"
    if int(graph["pass_count"]) < 7:
        return "NOT_PHYSICS_CURRENT_FORM: fewer than 7/10 holdout targets pass"
    if float(graph["mean_log10_error"]) >= float(best_baseline["mean_log10_error"]):
        return "NEEDS_REVISION: does not beat best non-cheating baseline"
    return "PROVISIONALLY_SUPPORTED: known-holdout only, future blind tests still required"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING"
    if not math.isfinite(value):
        return "inf"
    return f"{value:.12g}"


def write_blind_registry() -> None:
    rows = [
        {
            "prediction_id": "FUTURE_BLIND_001",
            "target": "next_CODATA_alpha_shift_direction",
            "frozen_formula": "alpha = 2 lnK^2 / (pi lnN)",
            "status": "pre_registered_not_evaluated",
            "unlock_rule": "next independent CODATA release after this file timestamp",
        },
        {
            "prediction_id": "FUTURE_BLIND_002",
            "target": "external_nuclear_mass_subset_not_in_current_tables",
            "frozen_formula": "not yet available; current model must define before unlock",
            "status": "blocked_missing_formula",
            "unlock_rule": "dataset selected by external party before formula edit",
        },
        {
            "prediction_id": "FUTURE_BLIND_003",
            "target": "new_graph_spectrum_invariant",
            "frozen_formula": "finite graph construction with K=6 and declared seed",
            "status": "pre_registered_not_evaluated",
            "unlock_rule": "independent implementation computes invariant",
        },
    ]
    write_csv(RESULTS / "frozen_blind_predictions_v2.csv", rows)


def write_report(candidate: FormulaCandidate, all_rows: list[PredictionRow], summaries: list[dict[str, object]], final: str) -> None:
    lines = [
        "# Reduced Model Optimization v2 Report",
        "",
        f"Final verdict: `{final}`",
        "",
        "## Optimized Shared Mass Formula",
        "",
        "This formula was optimized only on the training masses W, Z, H.",
        "It uses one shared global coefficient and one shared exponent vector.",
        "It is not allowed to use target-specific coefficients such as C_p, C_n, or C_W.",
        "",
        "```text",
        formula_text(candidate.base, candidate.coefficient, candidate.exponents),
        "```",
        "",
        f"- train mean log10 error: `{candidate.train_mean_log10_error:.12g}`",
        f"- complexity: `{candidate.complexity}`",
        f"- objective: `{candidate.objective:.12g}`",
        "",
        "## Leaderboard",
        "",
        "| Model | Split | Pass | Missing | Mean log10 error | Max log10 error |",
        "|:--|:--|--:|--:|--:|--:|",
    ]
    for row in summaries:
        lines.append(
            f"| `{row['model']}` | `{row['split']}` | {row['pass_count']}/{row['target_count']} | {row['missing_count']} | {fmt(float(row['mean_log10_error']))} | {fmt(float(row['max_log10_error']))} |"
        )
    lines += [
        "",
        "## Holdout Details",
        "",
        "| Model | Target | True | Predicted | log10 error | Tol | Pass | Formula |",
        "|:--|:--|--:|--:|--:|--:|:--|:--|",
    ]
    for row in [r for r in all_rows if r.split == "holdout"]:
        lines.append(
            f"| `{row.model}` | `{row.target}` | `{fmt(row.true_value)}` | `{fmt(row.predicted)}` | `{fmt(row.log10_error)}` | `{row.tolerance_log10}` | `{row.passed}` | `{row.formula}` |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "The optimization produced a reduced model, but it still cannot be called physics unless it beats baselines on holdout and then survives true future blind tests.",
        "Known holdout is useful for debugging; it is not the same as a real blind prediction.",
        "",
    ]
    (RESULTS / "reduced_model_optimization_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    all_targets = targets()
    candidate = optimize_mass_family(all_targets)
    models = ["REDUCED_GRAPH_OPTIMIZED_V2", "DIMENSIONAL_BASELINE", "RANDOM_LOG_BASELINE"]
    all_rows: list[PredictionRow] = []
    summaries: list[dict[str, object]] = []
    for model in models:
        rows = evaluate_model(model, all_targets, candidate)
        all_rows.extend(rows)
        summaries.append(summarize(rows, "train"))
        summaries.append(summarize(rows, "holdout"))
    final = verdict(summaries)
    write_csv(RESULTS / "reduced_model_predictions.csv", [asdict(r) for r in all_rows])
    (RESULTS / "reduced_model_optimization.json").write_text(
        json.dumps(
            {
                "candidate": asdict(candidate),
                "summaries": summaries,
                "verdict": final,
                "rows": [asdict(r) for r in all_rows],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    write_blind_registry()
    write_report(candidate, all_rows, summaries, final)
    print(final)
    print(RESULTS / "reduced_model_optimization_report.md")
    print(RESULTS / "frozen_blind_predictions_v2.csv")


if __name__ == "__main__":
    main()
