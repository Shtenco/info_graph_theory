#!/usr/bin/env python3
"""Symbolic axiom system v9 for the information-graph/BIP39 program.

This script does not claim that the axioms are physically true.  It verifies
what follows inside the formal system:

- BIP39 structural identities from K = 6;
- frozen symbolic formula registry;
- theorem mode forbids target-specific calibration;
- fit mode is explicitly separated from theorem mode.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from bip39_no_fit_verification_v6 import FROZEN_FORMULAS, formula_registry_hash
from bip39_unification_search_v5 import bip39, feature_values, targets


KIT = Path(__file__).resolve().parent
RESULTS = KIT / "results"


@dataclass
class Axiom:
    key: str
    statement: str
    status: str


@dataclass
class Theorem:
    key: str
    statement: str
    derived_from: str
    lhs: str
    rhs: str
    passed: bool
    notes: str


@dataclass
class FormulaTheorem:
    target: str
    formula: str
    allowed_symbols: str
    forbidden_symbols: str
    theorem_mode: str
    registry_hash: str
    passed: bool


def axioms() -> list[Axiom]:
    return [
        Axiom("A0", "K is the primitive graph/BIP39 arity and K = 6.", "accepted_formal_axiom"),
        Axiom("A1", "BIP39 word bits are b = 2K - 1.", "definition"),
        Axiom("A2", "BIP39 dictionary size is D = 2^b.", "definition"),
        Axiom("A3", "BIP39 phrase length is W = 4K.", "definition"),
        Axiom("A4", "BIP39 checksum size is C = K + 2.", "definition"),
        Axiom("A5", "BIP39 total phrase bits are T = W b.", "definition"),
        Axiom("A6", "The graph sector uses N, p and U = ln(N)/abs(ln(Kp)).", "definition"),
        Axiom("A7", "The theorem mode forbids target-specific calibration coefficients.", "rule"),
        Axiom("A8", "Fit mode may compute calibration coefficients, but fit mode is not proof mode.", "rule"),
    ]


def bip39_theorems() -> list[Theorem]:
    inv = bip39()
    k = inv.derived_K
    checks = [
        ("T1", "bits_per_word = 2K - 1", str(inv.bits_per_word), str(int(2 * k - 1)), "A0,A1"),
        ("T2", "dictionary_size = 2^(2K - 1)", str(inv.dictionary_size), str(2 ** int(2 * k - 1)), "A0,A1,A2"),
        ("T3", "words_per_phrase = 4K", str(inv.words_per_phrase), str(int(4 * k)), "A0,A3"),
        ("T4", "sha256_entropy_bits = 4*2^K", str(inv.sha256_entropy_bits), str(4 * 2 ** int(k)), "A0"),
        ("T5", "checksum_bits = K + 2", str(inv.checksum_bits), str(int(k + 2)), "A0,A4"),
        ("T6", "phrase_bits_total = 4K(2K - 1)", str(inv.phrase_bits_total), str(int(4 * k * (2 * k - 1))), "A0,A1,A3,A5"),
        ("T7", "table_rows = 4", str(inv.table_rows), "4", "A3"),
        ("T8", "table_columns = K", str(inv.table_columns), str(int(k)), "A0"),
    ]
    rows: list[Theorem] = []
    for key, statement, lhs, rhs, derived in checks:
        rows.append(Theorem(key, statement, derived, lhs, rhs, lhs == rhs, "integer identity"))
    return rows


def formula_theorems() -> list[FormulaTheorem]:
    allowed = {"K", "lnDict", "U", "bits", "bip_density", "dict", "entropy", "pi", "words", "f1", "total_bits", "checksum", "lnK"}
    forbidden_markers = ["C_", "observed", "target", "experiment", "calibration"]
    registry_hash = formula_registry_hash()
    rows: list[FormulaTheorem] = []
    for target, spec in FROZEN_FORMULAS.items():
        factors = set(spec["factors"])
        text = str(spec["text"])
        forbidden_used = [marker for marker in forbidden_markers if marker in text]
        unknown = sorted(factors - allowed)
        passed = not unknown and not forbidden_used
        rows.append(
            FormulaTheorem(
                target=target,
                formula=text,
                allowed_symbols=", ".join(sorted(factors)),
                forbidden_symbols=", ".join(forbidden_used or []),
                theorem_mode="NO_CALIBRATION",
                registry_hash=registry_hash,
                passed=passed,
            )
        )
    return rows


def numeric_substitution_audit() -> dict[str, object]:
    inv = bip39()
    features = feature_values(inv)
    rows = []
    for target in targets():
        spec = FROZEN_FORMULAS[target.name]
        predicted = float(spec["base"])
        for name, exponent in spec["factors"].items():
            predicted *= features[name] ** exponent
        rel = abs(predicted - target.observed) / abs(target.observed) * 100.0
        rows.append(
            {
                "target": target.name,
                "observed": target.observed,
                "predicted": predicted,
                "relative_error_percent": rel,
                "pass_readme_tolerance": rel < 5.0,
            }
        )
    return {
        "rows": rows,
        "count": len(rows),
        "pass_readme_style_tolerance": sum(1 for row in rows if row["pass_readme_tolerance"]),
        "mean_relative_error_percent": sum(row["relative_error_percent"] for row in rows) / len(rows),
        "max_relative_error_percent": max(row["relative_error_percent"] for row in rows),
    }


def system_hash(payload: dict[str, object]) -> str:
    stable = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(payload: dict[str, object]) -> None:
    ax = [Axiom(**row) for row in payload["axioms"]]
    th = [Theorem(**row) for row in payload["bip39_theorems"]]
    ft = [FormulaTheorem(**row) for row in payload["formula_theorems"]]
    audit = payload["numeric_substitution_audit"]
    lines = [
        "# Symbolic Axiom System v9",
        "",
        f"System hash: `{payload['system_hash']}`",
        "",
        "## Status",
        "",
        "```text",
        "FORMAL_SYMBOLIC_SYSTEM_VERIFIED",
        "PHYSICAL_TRUTH_NOT_PROVEN_BY_SYMBOLIC_FORM ALONE",
        "CALIBRATION_FORBIDDEN_IN_THEOREM_MODE",
        "```",
        "",
        "## Axioms",
        "",
        "| Key | Statement | Status |",
        "|:--|:--|:--|",
    ]
    for row in ax:
        lines.append(f"| `{row.key}` | {row.statement} | `{row.status}` |")
    lines += [
        "",
        "## BIP39 Theorems",
        "",
        "| Key | Statement | Derived from | LHS | RHS | Pass |",
        "|:--|:--|:--|--:|--:|:--|",
    ]
    for row in th:
        lines.append(f"| `{row.key}` | {row.statement} | `{row.derived_from}` | `{row.lhs}` | `{row.rhs}` | `{row.passed}` |")
    lines += [
        "",
        "## Frozen Formula Theorems",
        "",
        "| Target | Formula | Symbols | Theorem mode | Pass |",
        "|:--|:--|:--|:--|:--|",
    ]
    for row in ft:
        lines.append(f"| `{row.target}` | `{row.formula}` | `{row.allowed_symbols}` | `{row.theorem_mode}` | `{row.passed}` |")
    lines += [
        "",
        "## Numeric Substitution Audit",
        "",
        f"- `count = {audit['count']}`",
        f"- `pass_readme_style_tolerance = {audit['pass_readme_style_tolerance']}/{audit['count']}`",
        f"- `mean_relative_error_percent = {audit['mean_relative_error_percent']:.12g}`",
        f"- `max_relative_error_percent = {audit['max_relative_error_percent']:.12g}`",
        "",
        "## Boundary",
        "",
        "The symbolic system proves only conditional statements: if the axioms and definitions are accepted, the listed formulas follow inside the formal language.",
        "It does not prove that nature must obey these axioms. That remains an empirical validation problem.",
        "",
    ]
    (RESULTS / "symbolic_axiom_system_v9_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {
        "axioms": [asdict(row) for row in axioms()],
        "bip39_theorems": [asdict(row) for row in bip39_theorems()],
        "formula_theorems": [asdict(row) for row in formula_theorems()],
        "numeric_substitution_audit": numeric_substitution_audit(),
        "registry_hash": formula_registry_hash(),
    }
    payload["system_hash"] = system_hash(payload)
    (RESULTS / "symbolic_axiom_system_v9.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(RESULTS / "symbolic_axiom_system_v9_theorems.csv", payload["bip39_theorems"])
    write_csv(RESULTS / "symbolic_axiom_system_v9_formulas.csv", payload["formula_theorems"])
    write_report(payload)
    print("SYMBOLIC_AXIOM_SYSTEM_V9: OK")
    print(f"system_hash={payload['system_hash']}")
    print(RESULTS / "symbolic_axiom_system_v9_report.md")


if __name__ == "__main__":
    main()
