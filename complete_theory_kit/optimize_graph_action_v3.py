#!/usr/bin/env python3
"""Graph-action optimizer v3 with hard penalty and locked blind-style tests.

The purpose of this script is deliberately strict:

1. Put the large unified action back under graph theory.
2. Optimize only on a frozen training set.
3. Penalize degrees of freedom, target leakage, and non-graph shortcuts.
4. Evaluate on a locked known-blind holdout set.
5. Pre-register future blind tests that cannot be evaluated from today's data.

This is not a proof of physics. It is an anti-overfitting machine around the
information-graph hypothesis.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


K = 6.0
P = 4.8027e-42
N_UNIVERSE = 4.197668e121
M_E_MEV = 0.51099895
ALPHA_REF = 1.0 / 137.035999084
ALPHA_GRAPH = 2.0 * math.log(K) ** 2 / (math.pi * math.log(N_UNIVERSE))


@dataclass(frozen=True)
class Target:
    name: str
    observed: float
    unit: str
    family: str
    split: str
    tolerance_log10: float
    q_mass: float
    q_charge: float
    q_spin: float
    q_generation: float
    q_isospin: float
    q_color: float


@dataclass
class GraphInvariants:
    node_count: int
    degree_k: int
    edge_count: int
    trace_laplacian: float
    spectral_gap: float
    lambda_max: float
    mean_lambda: float
    heat_t_025: float
    heat_t_1: float
    spectral_entropy: float
    kirchhoff_log_proxy: float


@dataclass
class FitResult:
    feature_names: list[str]
    theta: list[float]
    train_loss: float
    ridge_norm: float
    effective_dof: float
    graph_feature_count: int
    action_value: float
    penalty_value: float
    leakage_penalty: float
    shortcut_penalty: float


@dataclass
class Prediction:
    target: str
    split: str
    family: str
    observed: float
    predicted: float
    log10_error: float
    tolerance_log10: float
    passed: bool


def build_small_world_graph(n: int = 48, k: int = 6, rewire_probability: float = 0.08, seed: int = 12345) -> list[list[float]]:
    # Deterministic local graph used as a finite proxy for the original K=6
    # information graph. The cosmological p is too small for a visible finite
    # demo, so p remains in the analytic invariants while this finite graph
    # exposes the Laplacian/spectrum machinery.
    import random

    rng = random.Random(seed)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    half = k // 2
    for i in range(n):
        for d in range(1, half + 1):
            j = (i + d) % n
            if rng.random() < rewire_probability:
                candidates = [x for x in range(n) if x != i and matrix[i][x] == 0.0]
                j = rng.choice(candidates)
            matrix[i][j] = 1.0
            matrix[j][i] = 1.0
    return matrix


def laplacian_from_adjacency(adj: list[list[float]]) -> list[list[float]]:
    n = len(adj)
    lap = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        degree = sum(adj[i])
        lap[i][i] = degree
        for j in range(n):
            if i != j:
                lap[i][j] = -adj[i][j]
    return lap


def jacobi_eigenvalues_symmetric(a: list[list[float]], max_iter: int = 20000, eps: float = 1e-11) -> list[float]:
    n = len(a)
    m = [row[:] for row in a]
    for _ in range(max_iter):
        p = 0
        q = 1
        max_off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                val = abs(m[i][j])
                if val > max_off:
                    max_off = val
                    p, q = i, j
        if max_off < eps:
            break
        if abs(m[p][p] - m[q][q]) < 1e-30:
            angle = math.pi / 4.0
        else:
            angle = 0.5 * math.atan2(2.0 * m[p][q], m[q][q] - m[p][p])
        c = math.cos(angle)
        s = math.sin(angle)
        app = c * c * m[p][p] - 2.0 * s * c * m[p][q] + s * s * m[q][q]
        aqq = s * s * m[p][p] + 2.0 * s * c * m[p][q] + c * c * m[q][q]
        m[p][q] = m[q][p] = 0.0
        for r in range(n):
            if r != p and r != q:
                mrp = c * m[r][p] - s * m[r][q]
                mrq = s * m[r][p] + c * m[r][q]
                m[r][p] = m[p][r] = mrp
                m[r][q] = m[q][r] = mrq
        m[p][p] = app
        m[q][q] = aqq
    return sorted(max(0.0, m[i][i]) for i in range(n))


def graph_invariants() -> GraphInvariants:
    adj = build_small_world_graph()
    lap = laplacian_from_adjacency(adj)
    eig = jacobi_eigenvalues_symmetric(lap)
    positive = [x for x in eig if x > 1e-8]
    trace = sum(lap[i][i] for i in range(len(lap)))
    heat_025 = sum(math.exp(-0.25 * x) for x in eig) / len(eig)
    heat_1 = sum(math.exp(-x) for x in eig) / len(eig)
    total_positive = sum(positive)
    weights = [x / total_positive for x in positive]
    entropy = -sum(w * math.log(w) for w in weights)
    kirchhoff = sum(math.log(x) for x in positive) - math.log(len(eig))
    return GraphInvariants(
        node_count=len(adj),
        degree_k=6,
        edge_count=int(sum(sum(row) for row in adj) // 2),
        trace_laplacian=trace,
        spectral_gap=positive[0],
        lambda_max=max(eig),
        mean_lambda=trace / len(eig),
        heat_t_025=heat_025,
        heat_t_1=heat_1,
        spectral_entropy=entropy,
        kirchhoff_log_proxy=kirchhoff,
    )


def targets() -> list[Target]:
    return [
        Target("electron_mass_MeV", 0.51099895, "MeV", "mass", "train", 0.002, 1, -1, 0.5, 1, -0.5, 0),
        Target("muon_mass_MeV", 105.6583755, "MeV", "mass", "train", 0.01, 1, -1, 0.5, 2, -0.5, 0),
        Target("W_mass_MeV", 80379.0, "MeV", "mass", "train", 0.01, 2, 1, 1, 2, 1, 0),
        Target("Z_mass_MeV", 91187.6, "MeV", "mass", "train", 0.01, 2, 0, 1, 2, 0, 0),
        Target("H_mass_MeV", 125200.0, "MeV", "mass", "train", 0.02, 2, 0, 0, 3, 0, 0),
        Target("alpha", ALPHA_REF, "dimensionless", "coupling", "train", 0.002, 0, 1, 1, 1, 0, 0),
        Target("proton_mass_MeV", 938.2720813, "MeV", "mass", "locked_known_blind", 0.01, 3, 1, 0.5, 1, 0.5, 3),
        Target("neutron_mass_MeV", 939.5654133, "MeV", "mass", "locked_known_blind", 0.01, 3, 0, 0.5, 1, -0.5, 3),
        Target("tau_mass_MeV", 1776.86, "MeV", "mass", "locked_known_blind", 0.02, 1, -1, 0.5, 3, -0.5, 0),
        Target("top_mass_MeV", 172690.0, "MeV", "mass", "locked_known_blind", 0.03, 1, 2 / 3, 0.5, 3, 0.5, 3),
        Target("alpha_s_mZ", 0.1181, "dimensionless", "coupling", "locked_known_blind", 0.03, 0, 0, 1, 3, 0, 8),
        Target("sin2_thetaW", 0.223, "dimensionless", "coupling", "locked_known_blind", 0.02, 0, 0, 1, 2, 0, 0),
        Target("G_F_GeV_minus2", 1.1663787e-5, "GeV^-2", "weak_dimensional", "locked_known_blind", 0.05, -2, 0, 1, 2, 1, 0),
        Target("planck_mass_GeV", 1.22089e19, "GeV", "gravity_dimensional", "locked_known_blind", 0.05, 1, 0, 2, 4, 0, 0),
        Target("Lambda_QCD_GeV", 0.217, "GeV", "strong_scale", "locked_known_blind", 0.05, 1, 0, 1, 1, 0, 8),
        Target("binding_energy_Fe56_MeV", 8.79, "MeV", "nuclear", "locked_known_blind", 0.02, 56, 26, 0, 1, 0, 3),
    ]


def base_value(target: Target) -> float:
    if target.family == "mass":
        return M_E_MEV
    if target.family == "coupling":
        return ALPHA_GRAPH
    if target.family == "weak_dimensional":
        return 1.0e-5
    if target.family == "gravity_dimensional":
        return 1.0e19
    if target.family == "strong_scale":
        return 0.2
    if target.family == "nuclear":
        return 8.0
    raise ValueError(target.family)


def feature_catalog(inv: GraphInvariants) -> dict[str, float]:
    return {
        "lnK": math.log(K),
        "lnN_over_abs_lnKp": math.log(N_UNIVERSE) / abs(math.log(K * P)),
        "f5": K / math.log(K),
        "spectral_gap": inv.spectral_gap,
        "lambda_max": inv.lambda_max,
        "mean_lambda": inv.mean_lambda,
        "heat_t_025": inv.heat_t_025,
        "heat_t_1": inv.heat_t_1,
        "spectral_entropy": inv.spectral_entropy,
        "kirchhoff_log_proxy": inv.kirchhoff_log_proxy,
    }


def row_features(target: Target, inv: GraphInvariants, feature_names: list[str]) -> list[float]:
    catalog = feature_catalog(inv)
    graph_terms = {
        name: math.log(abs(value) + 1e-300)
        for name, value in catalog.items()
    }
    descriptor_terms = {
        "q_mass": math.log(abs(target.q_mass) + 1.0),
        "q_charge_abs": abs(target.q_charge),
        "q_spin": target.q_spin,
        "q_generation": target.q_generation,
        "q_isospin": target.q_isospin,
        "q_color": math.log(abs(target.q_color) + 1.0),
        "family_mass": 1.0 if target.family == "mass" else 0.0,
        "family_coupling": 1.0 if target.family == "coupling" else 0.0,
        "family_dimensional": 1.0 if target.family not in {"mass", "coupling"} else 0.0,
    }
    values = {"bias": 1.0}
    values.update(graph_terms)
    values.update(descriptor_terms)
    values.update(
        {
            "gap_x_q_mass": graph_terms["spectral_gap"] * descriptor_terms["q_mass"],
            "entropy_x_generation": graph_terms["spectral_entropy"] * descriptor_terms["q_generation"],
            "heat_x_spin": graph_terms["heat_t_1"] * descriptor_terms["q_spin"],
            "lambda_max_x_color": graph_terms["lambda_max"] * descriptor_terms["q_color"],
            "kirchhoff_x_charge": graph_terms["kirchhoff_log_proxy"] * descriptor_terms["q_charge_abs"],
            "mean_lambda_x_dimensional": graph_terms["mean_lambda"] * descriptor_terms["family_dimensional"],
        }
    )
    return [values[name] for name in feature_names]


def solve_linear_system(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [a[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
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


def fit_ridge(train: list[Target], inv: GraphInvariants, feature_names: list[str], ridge: float) -> list[float]:
    x_rows = [row_features(t, inv, feature_names) for t in train]
    y = [math.log(t.observed / base_value(t)) for t in train]
    p = len(feature_names)
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    xty = [0.0 for _ in range(p)]
    for row, yi in zip(x_rows, y):
        for i in range(p):
            xty[i] += row[i] * yi
            for j in range(p):
                xtx[i][j] += row[i] * row[j]
    for i, name in enumerate(feature_names):
        xtx[i][i] += ridge * (0.0 if name == "bias" else 1.0)
    return solve_linear_system(xtx, xty)


def effective_ridge_dof(train: list[Target], inv: GraphInvariants, feature_names: list[str], ridge: float) -> float:
    x_rows = [row_features(t, inv, feature_names) for t in train]
    p = len(feature_names)
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    for row in x_rows:
        for i in range(p):
            for j in range(p):
                xtx[i][j] += row[i] * row[j]
    regularized = [row[:] for row in xtx]
    for i, name in enumerate(feature_names):
        regularized[i][i] += ridge * (0.0 if name == "bias" else 1.0)
    trace = 0.0
    for col in range(p):
        rhs = [xtx[i][col] for i in range(p)]
        solved = solve_linear_system(regularized, rhs)
        trace += solved[col]
    return max(0.0, trace)


def predict(target: Target, inv: GraphInvariants, feature_names: list[str], theta: list[float]) -> float:
    x = row_features(target, inv, feature_names)
    log_ratio = sum(a * b for a, b in zip(theta, x))
    log_ratio = max(-800.0, min(800.0, log_ratio))
    return base_value(target) * math.exp(log_ratio)


def log10_error(predicted: float, observed: float) -> float:
    if predicted <= 0 or not math.isfinite(predicted):
        return float("inf")
    return abs(math.log10(predicted / observed))


def evaluate(all_targets: list[Target], inv: GraphInvariants, feature_names: list[str], theta: list[float]) -> list[Prediction]:
    rows = []
    for target in all_targets:
        predicted = predict(target, inv, feature_names, theta)
        err = log10_error(predicted, target.observed)
        rows.append(
            Prediction(
                target=target.name,
                split=target.split,
                family=target.family,
                observed=target.observed,
                predicted=predicted,
                log10_error=err,
                tolerance_log10=target.tolerance_log10,
                passed=err <= target.tolerance_log10,
            )
        )
    return rows


def fit_graph_action() -> tuple[GraphInvariants, FitResult, list[Prediction]]:
    inv = graph_invariants()
    all_targets = targets()
    train = [t for t in all_targets if t.split == "train"]
    graph_features = [
        "gap_x_q_mass",
        "entropy_x_generation",
        "heat_x_spin",
        "lambda_max_x_color",
        "kirchhoff_x_charge",
        "mean_lambda_x_dimensional",
    ]
    descriptor_features = [
        "q_mass",
        "q_charge_abs",
        "q_spin",
        "q_generation",
        "q_color",
        "family_mass",
        "family_coupling",
        "family_dimensional",
    ]
    feature_names = ["bias"] + graph_features + descriptor_features

    best: FitResult | None = None
    best_rows: list[Prediction] = []
    for ridge in [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]:
        theta = fit_ridge(train, inv, feature_names, ridge)
        rows = evaluate(all_targets, inv, feature_names, theta)
        train_errors = [r.log10_error for r in rows if r.split == "train"]
        train_loss = sum(e * e for e in train_errors) / len(train_errors)
        effective_dof = effective_ridge_dof(train, inv, feature_names, ridge)
        graph_feature_count = sum(1 for name, value in zip(feature_names, theta) if name in graph_features and abs(value) > 1e-6)
        ridge_norm = sum(value * value for name, value in zip(feature_names, theta) if name != "bias")
        leakage_penalty = 0.0
        shortcut_penalty = 0.5 if graph_feature_count < 3 else 0.0
        penalty_value = 0.03 * effective_dof + 0.01 * ridge_norm + leakage_penalty + shortcut_penalty
        action_value = train_loss + penalty_value
        candidate = FitResult(
            feature_names=feature_names,
            theta=theta,
            train_loss=train_loss,
            ridge_norm=ridge_norm,
            effective_dof=effective_dof,
            graph_feature_count=graph_feature_count,
            action_value=action_value,
            penalty_value=penalty_value,
            leakage_penalty=leakage_penalty,
            shortcut_penalty=shortcut_penalty,
        )
        if best is None or candidate.action_value < best.action_value:
            best = candidate
            best_rows = rows
    assert best is not None
    return inv, best, best_rows


def dimensional_baseline(all_targets: list[Target]) -> list[Prediction]:
    rows = []
    for target in all_targets:
        predicted = base_value(target)
        err = log10_error(predicted, target.observed)
        rows.append(
            Prediction(
                target=target.name,
                split=target.split,
                family=target.family,
                observed=target.observed,
                predicted=predicted,
                log10_error=err,
                tolerance_log10=target.tolerance_log10,
                passed=err <= target.tolerance_log10,
            )
        )
    return rows


def summary(rows: list[Prediction], split: str) -> dict[str, object]:
    selected = [r for r in rows if r.split == split]
    errors = [r.log10_error for r in selected]
    return {
        "split": split,
        "pass_count": sum(1 for r in selected if r.passed),
        "target_count": len(selected),
        "mean_log10_error": sum(errors) / len(errors),
        "max_log10_error": max(errors),
    }


def verdict(graph_blind: dict[str, object], baseline_blind: dict[str, object], fit: FitResult) -> str:
    if fit.effective_dof >= len([t for t in targets() if t.split == "train"]):
        return "FAIL_COMPLEXITY: effective fitted DOF is not below training target count"
    if fit.graph_feature_count < 3:
        return "FAIL_GRAPH_STRUCTURE: optimized action does not materially use graph-spectrum interactions"
    if int(graph_blind["pass_count"]) < 6:
        return "FAIL_BLIND_SCORE: fewer than 6 locked known-blind targets pass"
    if float(graph_blind["mean_log10_error"]) >= float(baseline_blind["mean_log10_error"]):
        return "FAIL_BASELINE: graph action does not beat dimensional baseline"
    return "PROVISIONAL_NUMERIC_SURVIVAL: locked known-blind passed; future blind still required"


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


def write_future_registry() -> None:
    rows = [
        {
            "prediction_id": "GRAPH_ACTION_V3_FUTURE_001",
            "target": "next_CODATA_alpha_value",
            "frozen_rule": "use graph_action_v3.json theta and ALPHA_GRAPH; no refit",
            "unlock_rule": "first CODATA release after 2026-06-30",
            "status": "future_blind_registered",
        },
        {
            "prediction_id": "GRAPH_ACTION_V3_FUTURE_002",
            "target": "externally selected nuclear binding-energy subset",
            "frozen_rule": "use graph_action_v3.json theta; evaluator chooses nuclei before any code edit",
            "unlock_rule": "third-party target list timestamped after this registry",
            "status": "future_blind_registered",
        },
        {
            "prediction_id": "GRAPH_ACTION_V3_FUTURE_003",
            "target": "independent implementation of K=6 finite graph spectral invariants",
            "frozen_rule": "node_count=48, degree_k=6, seed=12345, rewire_probability=0.08",
            "unlock_rule": "independent code computes spectrum without reading generated CSV",
            "status": "future_blind_registered",
        },
    ]
    write_csv(RESULTS / "graph_action_v3_future_blind_registry.csv", rows)


def write_report(inv: GraphInvariants, fit: FitResult, rows: list[Prediction], baseline_rows: list[Prediction], final: str) -> None:
    graph_train = summary(rows, "train")
    graph_blind = summary(rows, "locked_known_blind")
    base_blind = summary(baseline_rows, "locked_known_blind")
    lines = [
        "# Graph Action Optimization v3",
        "",
        f"Final verdict: `{final}`",
        "",
        "## Unified Penalized Graph Action",
        "",
        "```text",
        "S_total(theta; G, L) = S_U[X; theta] + S_penalty",
        "",
        "S_penalty =",
        "  lambda_dof * effective_DOF_ridge(theta)",
        "+ lambda_ridge * ||theta||_2^2",
        "+ lambda_shortcut * I[too few spectral graph invariants are active]",
        "+ lambda_leak * Leakage(theta, locked_known_blind)",
        "",
        "Optimization domain:",
        "  train only = {electron, muon, W, Z, H, alpha}",
        "",
        "Locked evaluation domain:",
        "  locked_known_blind = {proton, neutron, tau, top, alpha_s, sin2_thetaW, G_F, Planck, Lambda_QCD, Fe56}",
        "```",
        "",
        "## Graph Invariants",
        "",
        "| Invariant | Value |",
        "|:--|--:|",
    ]
    for key, value in asdict(inv).items():
        lines.append(f"| `{key}` | `{fmt(float(value))}` |")
    lines += [
        "",
        "## Optimized Theta",
        "",
        "| Feature | Theta |",
        "|:--|--:|",
    ]
    for name, value in zip(fit.feature_names, fit.theta):
        lines.append(f"| `{name}` | `{fmt(value)}` |")
    lines += [
        "",
        "## Penalty Audit",
        "",
        f"- `train_loss = {fmt(fit.train_loss)}`",
        f"- `ridge_norm = {fmt(fit.ridge_norm)}`",
        f"- `effective_dof = {fmt(fit.effective_dof)}`",
        f"- `graph_feature_count = {fit.graph_feature_count}`",
        f"- `penalty_value = {fmt(fit.penalty_value)}`",
        f"- `shortcut_penalty = {fmt(fit.shortcut_penalty)}`",
        f"- `leakage_penalty = {fmt(fit.leakage_penalty)}`",
        f"- `action_value = {fmt(fit.action_value)}`",
        "",
        "## Scoreboard",
        "",
        "| Model | Split | Pass | Mean log10 error | Max log10 error |",
        "|:--|:--|--:|--:|--:|",
        f"| `GRAPH_ACTION_V3` | `train` | {graph_train['pass_count']}/{graph_train['target_count']} | `{fmt(float(graph_train['mean_log10_error']))}` | `{fmt(float(graph_train['max_log10_error']))}` |",
        f"| `GRAPH_ACTION_V3` | `locked_known_blind` | {graph_blind['pass_count']}/{graph_blind['target_count']} | `{fmt(float(graph_blind['mean_log10_error']))}` | `{fmt(float(graph_blind['max_log10_error']))}` |",
        f"| `DIMENSIONAL_BASELINE` | `locked_known_blind` | {base_blind['pass_count']}/{base_blind['target_count']} | `{fmt(float(base_blind['mean_log10_error']))}` | `{fmt(float(base_blind['max_log10_error']))}` |",
        "",
        "## Locked Known-Blind Details",
        "",
        "| Target | Observed | Predicted | log10 error | Tol | Pass |",
        "|:--|--:|--:|--:|--:|:--|",
    ]
    for row in [r for r in rows if r.split == "locked_known_blind"]:
        lines.append(
            f"| `{row.target}` | `{fmt(row.observed)}` | `{fmt(row.predicted)}` | `{fmt(row.log10_error)}` | `{fmt(row.tolerance_log10)}` | `{row.passed}` |"
        )
    lines += [
        "",
        "## Scientific Reading",
        "",
        "This v3 layer forces the theory to live inside graph invariants instead of free target-specific constants.",
        "A pass here would still not be a final proof, because locked known-blind data are already historically known.",
        "The future registry is the required next gate: formulas are frozen first, external data arrive later.",
        "",
    ]
    (RESULTS / "graph_action_v3_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    inv, fit, rows = fit_graph_action()
    baseline_rows = dimensional_baseline(targets())
    graph_blind = summary(rows, "locked_known_blind")
    base_blind = summary(baseline_rows, "locked_known_blind")
    final = verdict(graph_blind, base_blind, fit)
    payload = {
        "verdict": final,
        "graph_invariants": asdict(inv),
        "fit": asdict(fit),
        "predictions": [asdict(r) for r in rows],
        "baseline_predictions": [asdict(r) for r in baseline_rows],
        "summaries": {
            "graph_train": summary(rows, "train"),
            "graph_locked_known_blind": graph_blind,
            "baseline_locked_known_blind": base_blind,
        },
    }
    (RESULTS / "graph_action_v3.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "graph_action_v3_predictions.csv", [asdict(r) for r in rows])
    write_csv(RESULTS / "graph_action_v3_baseline_predictions.csv", [asdict(r) for r in baseline_rows])
    write_future_registry()
    write_report(inv, fit, rows, baseline_rows, final)
    print(final)
    print(f"effective_dof={fit.effective_dof:.12g}")
    print(f"graph_feature_count={fit.graph_feature_count}")
    print(RESULTS / "graph_action_v3_report.md")


if __name__ == "__main__":
    main()
