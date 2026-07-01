#!/usr/bin/env python3
"""Spectral Graph Automata Field Theory v4.

This layer reformulates the information-graph program as a constrained graph
neural automaton.  The automaton basis is fixed before fitting; only a small
readout is trained on the declared training targets.  The goal is to test
whether a graph-automata field can survive hard anti-overfitting rules.

It is a scientific scaffold, not a proof of physics.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from optimize_graph_action_v3 import (
    ALPHA_GRAPH,
    ALPHA_REF,
    K,
    M_E_MEV,
    GraphInvariants,
    Target,
    base_value,
    build_small_world_graph,
    graph_invariants,
    laplacian_from_adjacency,
    log10_error,
    solve_linear_system,
    targets,
)


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


CHANNELS = 8
AUTOMATA_STEPS = 9
RIDGE_GRID = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
_GRAPH_CACHE: tuple[GraphInvariants, list[list[float]], list[list[float]]] | None = None
_DESIGN_CACHE: dict[str, list[float]] = {}


@dataclass
class AutomatonBasis:
    name: str
    role: str
    update_rule: str


@dataclass
class AutomataFit:
    feature_names: list[str]
    theta: list[float]
    ridge: float
    train_loss: float
    effective_dof: float
    automata_feature_count: int
    penalty_value: float
    action_value: float


@dataclass
class AutomataPrediction:
    target: str
    split: str
    family: str
    observed: float
    predicted: float
    log10_error: float
    tolerance_log10: float
    passed: bool


BASIS = [
    AutomatonBasis("identity_memory", "local persistence", "X <- X"),
    AutomatonBasis("laplacian_diffusion", "spectral locality", "X <- X - eps L X"),
    AutomatonBasis("neighbor_message", "graph message passing", "X <- D^-1 A X"),
    AutomatonBasis("phase_rotation", "U(1)-like channel rotation", "X <- R(q_charge) X"),
    AutomatonBasis("spin_gate", "spin/isospin gate", "X <- tanh(spin * X)"),
    AutomatonBasis("color_gate", "SU(3)-like color sector proxy", "X <- color-weighted channels"),
    AutomatonBasis("heat_kernel_gate", "absolute convergence regulator", "X <- exp(-sigma n) X"),
    AutomatonBasis("spectral_pool", "observable extraction", "pool(X, L, heat kernel)"),
]


def initial_state(target: Target, n: int) -> list[list[float]]:
    rows: list[list[float]] = []
    for i in range(n):
        phase = 2.0 * math.pi * (i + 1.0) / n
        rows.append(
            [
                1.0,
                math.sin(phase * (target.q_generation + 1.0)),
                math.cos(phase * (abs(target.q_charge) + 1.0)),
                target.q_spin,
                target.q_isospin,
                math.log(abs(target.q_mass) + 1.0),
                math.log(abs(target.q_color) + 1.0),
                1.0 if target.family == "mass" else -1.0 if target.family == "coupling" else 0.0,
            ]
        )
    return rows


def matvec_laplacian(lap: list[list[float]], state: list[list[float]]) -> list[list[float]]:
    n = len(lap)
    out = [[0.0 for _ in range(CHANNELS)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            weight = lap[i][j]
            if weight == 0.0:
                continue
            for c in range(CHANNELS):
                out[i][c] += weight * state[j][c]
    return out


def neighbor_average(adj: list[list[float]], state: list[list[float]]) -> list[list[float]]:
    n = len(adj)
    out = [[0.0 for _ in range(CHANNELS)] for _ in range(n)]
    for i in range(n):
        degree = max(1.0, sum(adj[i]))
        for j in range(n):
            if adj[i][j] == 0.0:
                continue
            for c in range(CHANNELS):
                out[i][c] += state[j][c] / degree
    return out


def automaton_step(
    state: list[list[float]],
    adj: list[list[float]],
    lap: list[list[float]],
    target: Target,
    step: int,
) -> list[list[float]]:
    diffusion = matvec_laplacian(lap, state)
    message = neighbor_average(adj, state)
    sigma = 0.055 + 0.01 * abs(target.q_spin)
    heat = math.exp(-sigma * (step + 1))
    charge_phase = math.tanh(target.q_charge)
    spin_gate = math.tanh(target.q_spin + 0.5 * target.q_isospin)
    color_gate = 1.0 + 0.03 * target.q_color
    eps = 0.035
    n = len(state)
    updated = [[0.0 for _ in range(CHANNELS)] for _ in range(n)]
    for i in range(n):
        for c in range(CHANNELS):
            left = state[i][(c - 1) % CHANNELS]
            right = state[i][(c + 1) % CHANNELS]
            rotated = math.cos(charge_phase) * state[i][c] + math.sin(charge_phase) * 0.5 * (right - left)
            local = 0.42 * state[i][c] + 0.30 * message[i][c] - eps * diffusion[i][c]
            gated = math.tanh(local + 0.08 * spin_gate * rotated)
            updated[i][c] = heat * color_gate * gated
    return updated


def run_automaton(target: Target) -> tuple[list[float], GraphInvariants]:
    inv, adj, lap = graph_bundle()
    state = initial_state(target, inv.node_count)
    for step in range(AUTOMATA_STEPS):
        state = automaton_step(state, adj, lap, target, step)
    pooled = pool_features(state, inv, target)
    return pooled, inv


def graph_bundle() -> tuple[GraphInvariants, list[list[float]], list[list[float]]]:
    global _GRAPH_CACHE
    if _GRAPH_CACHE is None:
        inv = graph_invariants()
        adj = build_small_world_graph(inv.node_count, inv.degree_k)
        lap = laplacian_from_adjacency(adj)
        _GRAPH_CACHE = (inv, adj, lap)
    return _GRAPH_CACHE


def pool_features(state: list[list[float]], inv: GraphInvariants, target: Target) -> list[float]:
    n = len(state)
    means = [sum(row[c] for row in state) / n for c in range(CHANNELS)]
    energies = [sum(row[c] * row[c] for row in state) / n for c in range(CHANNELS)]
    abs_means = [sum(abs(row[c]) for row in state) / n for c in range(CHANNELS)]
    graph_scalars = [
        math.log(inv.spectral_gap + 1e-12),
        math.log(inv.lambda_max + 1e-12),
        math.log(inv.heat_t_1 + 1e-12),
        inv.spectral_entropy,
        math.log(abs(inv.kirchhoff_log_proxy) + 1.0),
    ]
    descriptors = [
        math.log(abs(target.q_mass) + 1.0),
        abs(target.q_charge),
        target.q_spin,
        target.q_generation,
        math.log(abs(target.q_color) + 1.0),
    ]
    interactions = [
        means[1] * descriptors[0],
        means[2] * descriptors[1],
        energies[3] * descriptors[2],
        abs_means[4] * descriptors[3],
        energies[6] * descriptors[4],
        graph_scalars[0] * means[5],
        graph_scalars[3] * abs_means[7],
    ]
    return [1.0] + means + energies + abs_means + graph_scalars + descriptors + interactions


def feature_names() -> list[str]:
    return (
        ["bias"]
        + [f"mean_c{i}" for i in range(CHANNELS)]
        + [f"energy_c{i}" for i in range(CHANNELS)]
        + [f"abs_mean_c{i}" for i in range(CHANNELS)]
        + ["log_gap", "log_lambda_max", "log_heat_t_1", "spectral_entropy", "log_kirchhoff"]
        + ["q_mass", "q_charge_abs", "q_spin", "q_generation", "q_color"]
        + [
            "mean_c1_x_q_mass",
            "mean_c2_x_charge",
            "energy_c3_x_spin",
            "abs_mean_c4_x_generation",
            "energy_c6_x_color",
            "log_gap_x_mean_c5",
            "entropy_x_abs_mean_c7",
        ]
    )


def design_row(target: Target) -> list[float]:
    if target.name in _DESIGN_CACHE:
        return _DESIGN_CACHE[target.name]
    values, _ = run_automaton(target)
    _DESIGN_CACHE[target.name] = values
    return values


def fit_ridge(train: list[Target], ridge: float) -> list[float]:
    x_rows = [design_row(t) for t in train]
    y = [math.log(t.observed / base_value(t)) for t in train]
    p = len(x_rows[0])
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    xty = [0.0 for _ in range(p)]
    for row, yi in zip(x_rows, y):
        for i in range(p):
            xty[i] += row[i] * yi
            for j in range(p):
                xtx[i][j] += row[i] * row[j]
    for i in range(p):
        xtx[i][i] += ridge * (0.0 if i == 0 else 1.0)
    return solve_linear_system(xtx, xty)


def effective_dof(train: list[Target], ridge: float) -> float:
    x_rows = [design_row(t) for t in train]
    p = len(x_rows[0])
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    for row in x_rows:
        for i in range(p):
            for j in range(p):
                xtx[i][j] += row[i] * row[j]
    reg = [row[:] for row in xtx]
    for i in range(p):
        reg[i][i] += ridge * (0.0 if i == 0 else 1.0)
    trace = 0.0
    for col in range(p):
        rhs = [xtx[i][col] for i in range(p)]
        solved = solve_linear_system(reg, rhs)
        trace += solved[col]
    return trace


def predict(target: Target, theta: list[float]) -> float:
    row = design_row(target)
    log_ratio = sum(a * b for a, b in zip(theta, row))
    log_ratio = max(-800.0, min(800.0, log_ratio))
    return base_value(target) * math.exp(log_ratio)


def evaluate(theta: list[float], all_targets: list[Target]) -> list[AutomataPrediction]:
    rows: list[AutomataPrediction] = []
    for target in all_targets:
        pred = predict(target, theta)
        err = log10_error(pred, target.observed)
        rows.append(
            AutomataPrediction(
                target=target.name,
                split=target.split,
                family=target.family,
                observed=target.observed,
                predicted=pred,
                log10_error=err,
                tolerance_log10=target.tolerance_log10,
                passed=err <= target.tolerance_log10,
            )
        )
    return rows


def summarize(rows: list[AutomataPrediction], split: str) -> dict[str, object]:
    selected = [r for r in rows if r.split == split]
    errors = [r.log10_error for r in selected]
    return {
        "split": split,
        "pass_count": sum(1 for r in selected if r.passed),
        "target_count": len(selected),
        "mean_log10_error": sum(errors) / len(errors),
        "max_log10_error": max(errors),
    }


def fit_automata_field() -> tuple[AutomataFit, list[AutomataPrediction], GraphInvariants]:
    all_targets = targets()
    train = [t for t in all_targets if t.split == "train"]
    names = feature_names()
    best: AutomataFit | None = None
    best_rows: list[AutomataPrediction] = []
    _, inv = run_automaton(train[0])
    automata_terms = [name for name in names if name.startswith(("mean_", "energy_", "abs_mean_", "log_", "entropy"))]
    for ridge in RIDGE_GRID:
        theta = fit_ridge(train, ridge)
        rows = evaluate(theta, all_targets)
        train_errors = [r.log10_error for r in rows if r.split == "train"]
        train_loss = sum(e * e for e in train_errors) / len(train_errors)
        dof = effective_dof(train, ridge)
        automata_count = sum(1 for name, value in zip(names, theta) if name in automata_terms and abs(value) > 1e-6)
        ridge_norm = sum(value * value for value in theta[1:])
        shortcut_penalty = 0.75 if automata_count < 6 else 0.0
        complexity_penalty = 0.04 * dof + 0.01 * ridge_norm
        penalty = shortcut_penalty + complexity_penalty
        action = train_loss + penalty
        fit = AutomataFit(
            feature_names=names,
            theta=theta,
            ridge=ridge,
            train_loss=train_loss,
            effective_dof=dof,
            automata_feature_count=automata_count,
            penalty_value=penalty,
            action_value=action,
        )
        if best is None or fit.action_value < best.action_value:
            best = fit
            best_rows = rows
    assert best is not None
    return best, best_rows, inv


def dimensional_baseline(all_targets: list[Target]) -> list[AutomataPrediction]:
    rows: list[AutomataPrediction] = []
    for target in all_targets:
        pred = base_value(target)
        err = log10_error(pred, target.observed)
        rows.append(
            AutomataPrediction(
                target=target.name,
                split=target.split,
                family=target.family,
                observed=target.observed,
                predicted=pred,
                log10_error=err,
                tolerance_log10=target.tolerance_log10,
                passed=err <= target.tolerance_log10,
            )
        )
    return rows


def verdict(fit: AutomataFit, graph_blind: dict[str, object], baseline_blind: dict[str, object]) -> str:
    train_count = len([t for t in targets() if t.split == "train"])
    if fit.effective_dof >= train_count:
        return "FAIL_COMPLEXITY: graph automata field has too much effective DOF"
    if fit.automata_feature_count < 6:
        return "FAIL_AUTOMATA_BASIS: readout does not materially use automata features"
    if int(graph_blind["pass_count"]) < 6:
        return "FAIL_BLIND_SCORE: fewer than 6 locked known-blind targets pass"
    if float(graph_blind["mean_log10_error"]) >= float(baseline_blind["mean_log10_error"]):
        return "FAIL_BASELINE: graph automata field does not beat dimensional baseline"
    return "PROVISIONAL_NUMERIC_SURVIVAL: automata field survived locked known-blind; future blind still required"


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
            "prediction_id": "SGAFT_V4_FUTURE_001",
            "target": "next independent alpha measurement or CODATA adjustment",
            "frozen_object": "graph_automata_field_v4.json",
            "unlock_rule": "first independent release after 2026-06-30",
            "status": "future_blind_registered",
        },
        {
            "prediction_id": "SGAFT_V4_FUTURE_002",
            "target": "third-party selected particle/nuclear observable subset",
            "frozen_object": "graph_automata_field_v4.json",
            "unlock_rule": "target list timestamped externally before any formula/code edit",
            "status": "future_blind_registered",
        },
        {
            "prediction_id": "SGAFT_V4_FUTURE_003",
            "target": "independent implementation of automata-basis invariant vector",
            "frozen_object": "CHANNELS=8, AUTOMATA_STEPS=9, K=6, seed=12345",
            "unlock_rule": "independent code reproduces pooled automata features",
            "status": "future_blind_registered",
        },
    ]
    write_csv(RESULTS / "graph_automata_field_v4_future_blind_registry.csv", rows)


def write_report(
    fit: AutomataFit,
    rows: list[AutomataPrediction],
    baseline_rows: list[AutomataPrediction],
    inv: GraphInvariants,
    final: str,
) -> None:
    graph_train = summarize(rows, "train")
    graph_blind = summarize(rows, "locked_known_blind")
    base_blind = summarize(baseline_rows, "locked_known_blind")
    lines = [
        "# Spectral Graph Automata Field Theory v4",
        "",
        f"Final verdict: `{final}`",
        "",
        "## Master Object",
        "",
        "```text",
        "U_GNN = (G, L, X_t, A_theta, Phi_theta, R, exp(-sigma n), S_penalty)",
        "",
        "X_{t+1} = A(G, L, X_t; automata_basis)",
        "O_k = Phi_theta(pool(X_T, L, heat_kernel))",
        "",
        "S_penalty =",
        "  lambda_dof * effective_DOF_ridge(Phi_theta)",
        "+ lambda_ridge * ||theta||_2^2",
        "+ lambda_basis * I[automata basis is not materially used]",
        "+ lambda_leak * Leakage(theta, locked_known_blind)",
        "```",
        "",
        "## Automata Basis",
        "",
        "| Basis | Role | Update rule |",
        "|:--|:--|:--|",
    ]
    for basis in BASIS:
        lines.append(f"| `{basis.name}` | {basis.role} | `{basis.update_rule}` |")
    lines += [
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
        "## Fit Audit",
        "",
        f"- `ridge = {fmt(fit.ridge)}`",
        f"- `train_loss = {fmt(fit.train_loss)}`",
        f"- `effective_dof = {fmt(fit.effective_dof)}`",
        f"- `automata_feature_count = {fit.automata_feature_count}`",
        f"- `penalty_value = {fmt(fit.penalty_value)}`",
        f"- `action_value = {fmt(fit.action_value)}`",
        "",
        "## Scoreboard",
        "",
        "| Model | Split | Pass | Mean log10 error | Max log10 error |",
        "|:--|:--|--:|--:|--:|",
        f"| `SGAFT_V4` | `train` | {graph_train['pass_count']}/{graph_train['target_count']} | `{fmt(float(graph_train['mean_log10_error']))}` | `{fmt(float(graph_train['max_log10_error']))}` |",
        f"| `SGAFT_V4` | `locked_known_blind` | {graph_blind['pass_count']}/{graph_blind['target_count']} | `{fmt(float(graph_blind['mean_log10_error']))}` | `{fmt(float(graph_blind['max_log10_error']))}` |",
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
        "## Interpretation",
        "",
        "This is the graph-neural version of the theory: formulas are not hand-written per target.",
        "The fixed automata basis produces a state, and a penalized readout maps that state to observables.",
        "A negative verdict means the current automata basis is not yet a validated physical theory.",
        "",
    ]
    (RESULTS / "graph_automata_field_v4_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    fit, rows, inv = fit_automata_field()
    baseline_rows = dimensional_baseline(targets())
    graph_blind = summarize(rows, "locked_known_blind")
    base_blind = summarize(baseline_rows, "locked_known_blind")
    final = verdict(fit, graph_blind, base_blind)
    payload = {
        "verdict": final,
        "constants": {
            "K": K,
            "alpha_graph": ALPHA_GRAPH,
            "alpha_reference": ALPHA_REF,
            "electron_mass_MeV": M_E_MEV,
            "channels": CHANNELS,
            "automata_steps": AUTOMATA_STEPS,
        },
        "basis": [asdict(b) for b in BASIS],
        "graph_invariants": asdict(inv),
        "fit": asdict(fit),
        "predictions": [asdict(r) for r in rows],
        "baseline_predictions": [asdict(r) for r in baseline_rows],
        "summaries": {
            "train": summarize(rows, "train"),
            "locked_known_blind": graph_blind,
            "baseline_locked_known_blind": base_blind,
        },
    }
    (RESULTS / "graph_automata_field_v4.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "graph_automata_field_v4_predictions.csv", [asdict(r) for r in rows])
    write_csv(RESULTS / "graph_automata_field_v4_baseline_predictions.csv", [asdict(r) for r in baseline_rows])
    write_future_registry()
    write_report(fit, rows, baseline_rows, inv, final)
    print(final)
    print(f"effective_dof={fit.effective_dof:.12g}")
    print(f"automata_feature_count={fit.automata_feature_count}")
    print(RESULTS / "graph_automata_field_v4_report.md")


if __name__ == "__main__":
    main()
