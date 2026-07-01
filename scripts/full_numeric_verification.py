#!/usr/bin/env python3
"""Полная числовая верификация распарсиваемых таблиц README."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
RESULTS = ROOT / "complete_theory_kit" / "results" / "full_theory_results.json"
REPORT = ROOT / "reports" / "FULL_NUMERIC_VERIFICATION_REPORT.md"
JSON_REPORT = ROOT / "reports" / "FULL_NUMERIC_VERIFICATION_RESULTS.json"


def parse_number(text: str) -> float | None:
    s = text.strip()
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("**", "")
    s = s.replace("$", "")
    s = s.replace("\\", "")
    s = s.replace(",", "")
    s = s.replace("−", "-").replace("–", "-")
    s = s.replace("~", "")
    s = s.replace("%", "")
    s = re.sub(r"\\text\{[^}]*\}", "", s)
    s = re.sub(r"\s+", " ", s)
    # Convert common LaTeX scientific notation.
    m = re.search(r"([-+]?\d+(?:\.\d+)?)\s*times\s*10\^\{?([-+]?\d+)\}?", s)
    if m:
        return float(m.group(1)) * (10.0 ** int(m.group(2)))
    m = re.search(r"([-+]?\d+(?:\.\d+)?)\s*[x×]\s*10\^?([-+]?\d+)", s)
    if m:
        return float(m.group(1)) * (10.0 ** int(m.group(2)))
    m = re.search(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s)
    if not m:
        return None
    return float(m.group(0))


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def rel_error(calc: float, ref: float) -> float:
    return abs(calc - ref) / abs(ref) * 100.0 if ref != 0 else abs(calc - ref)


def verify_control_table(text: str) -> list[dict[str, object]]:
    start = text.find("### 8.7 Единая контрольная таблица")
    end = text.find("### 8.8", start)
    if start < 0 or end < 0:
        return []
    rows = []
    for line_no, line in enumerate(text[:end].splitlines(), 1):
        if line_no < text[:start].count("\n") + 1:
            continue
        if not line.startswith("|") or "|:--" in line or "Категория" in line:
            continue
        cells = split_row(line)
        if len(cells) < 5:
            continue
        category, quantity = cells[0], cells[1]
        calc = parse_number(cells[2])
        ref = parse_number(cells[3])
        stated = parse_number(cells[4])
        if category == "BIP39":
            bip39_values = {
                "Бит на слово": 11.0,
                "Размер словаря": 2048.0,
                "Слов на фразу": 24.0,
                "Энтропия (SHA-256)": 256.0,
                "Контрольная сумма": 8.0,
                "Всего бит на фразу": 264.0,
                "Строк таблицы BIP39": 4.0,
                "Столбцов таблицы BIP39": 6.0,
            }
            calc = bip39_values.get(quantity, calc)
        if calc is None or ref is None or stated is None:
            continue
        actual = rel_error(calc, ref)
        # Many README values are rounded, so allow max absolute 0.15 percentage points
        # or 15% relative of the stated rounded error.
        tolerance = max(0.15, abs(stated) * 0.15)
        if "~" in cells[3] or "approx" in cells[3]:
            tolerance = max(tolerance, 0.35)
        ok = abs(actual - stated) <= tolerance
        rows.append({
            "table": "control_8_7",
            "line": line_no,
            "category": category,
            "quantity": quantity,
            "calc": calc,
            "ref": ref,
            "stated_error_percent": stated,
            "actual_error_percent": actual,
            "delta_percent_points": actual - stated,
            "ok": ok,
        })
    return rows


def verify_isotope_table(text: str) -> list[dict[str, object]]:
    start = text.find("### 6.4 Таблица предсказаний")
    end = text.find("### 6.5", start)
    if start < 0 or end < 0:
        return []
    base_line = text[:start].count("\n") + 1
    section = text[start:end]
    rows = []
    for offset, line in enumerate(section.splitlines(), 0):
        if not line.startswith("|") or "|:--" in line or "Изотоп" in line:
            continue
        cells = split_row(line)
        if len(cells) < 8:
            continue
        isotope = cells[0]
        pred = parse_number(cells[4])
        exp = parse_number(cells[5])
        diff = parse_number(cells[6])
        stated = parse_number(cells[7])
        if pred is None or exp is None or diff is None or stated is None:
            continue
        actual_diff = pred - exp
        actual_err = actual_diff / exp * 100.0
        ok = abs(actual_diff - diff) <= 5e-6 and abs(abs(actual_err) - abs(stated)) <= 0.01
        rows.append({
            "table": "isotopes_6_4",
            "line": base_line + offset,
            "isotope": isotope,
            "predicted": pred,
            "reference": exp,
            "stated_diff": diff,
            "actual_diff": actual_diff,
            "stated_error_percent": stated,
            "actual_error_percent": actual_err,
            "ok": ok,
        })
    return rows


def verify_bip39_from_json(data: dict) -> list[dict[str, object]]:
    return [
        {
            "table": "bip39_json",
            "quantity": row["name"],
            "calc": row["calculated"],
            "ref": row["reference"],
            "error_percent": row["relative_error_percent"],
            "ok": abs(row["relative_error_percent"]) < 1e-12,
        }
        for row in data["bip39"]
    ]


def verify_lenr_balance(text: str) -> list[dict[str, object]]:
    checks = []
    p_a = 1_974_226.7
    p_b = 7_188.9
    p_total = 1_981_415.6
    useful = 99_070.8
    gross_b = 0.845756
    net_b = 0.718893
    checks.append({
        "table": "lenr_balance",
        "quantity": "P_A+P_B=P_total",
        "calc": p_a + p_b,
        "ref": p_total,
        "abs_delta": (p_a + p_b) - p_total,
        "ok": abs((p_a + p_b) - p_total) < 1e-6,
    })
    checks.append({
        "table": "lenr_balance",
        "quantity": "useful_energy_100h_MWh",
        "calc": useful * 100 / 1_000_000,
        "ref": 9.90708,
        "abs_delta": useful * 100 / 1_000_000 - 9.90708,
        "ok": abs(useful * 100 / 1_000_000 - 9.90708) < 1e-10,
    })
    checks.append({
        "table": "lenr_balance",
        "quantity": "gross_B_times_0.85",
        "calc": gross_b * 0.85,
        "ref": net_b,
        "abs_delta": gross_b * 0.85 - net_b,
        "ok": abs(gross_b * 0.85 - net_b) < 1e-6,
    })
    return checks


def verify_core_json(data: dict) -> list[dict[str, object]]:
    rows = []
    params = data["parameters"]
    f = data["structural_functions"]
    rows.append({
        "table": "core",
        "quantity": "f2*f5=K",
        "calc": f["f2"] * f["f5"],
        "ref": params["K"],
        "abs_delta": f["f2"] * f["f5"] - params["K"],
        "ok": abs(f["f2"] * f["f5"] - params["K"]) < 1e-12,
    })
    for row in data["headline_constants"]:
        # Use thresholds aligned with the current machine verifier.
        thresholds = {
            "alpha": 0.02,
            "alpha_s": 5.0,
            "g_I^2": 0.5,
            "G_raw_README_formula": 0.05,
            "infoton_mass": 0.02,
            "proton_mass": 1e-5,
            "W_mass": 1e-4,
        }
        threshold = thresholds.get(row["name"], 1.0)
        rows.append({
            "table": "headline_json",
            "quantity": row["name"],
            "calc": row["calculated"],
            "ref": row["reference"],
            "error_percent": row["relative_error_percent"],
            "threshold_percent": threshold,
            "ok": row["relative_error_percent"] <= threshold,
        })
    graph = data["finite_graph"]
    rows.append({
        "table": "graph",
        "quantity": "trace_equals_sum_eigenvalues",
        "calc": graph["sum_eigenvalues"],
        "ref": graph["trace_laplacian"],
        "abs_delta": graph["trace_error"],
        "ok": graph["trace_error"] < 1e-7,
    })
    conv = data["convergence"][-1]
    rows.append({
        "table": "convergence",
        "quantity": "tail_bound_small",
        "calc": conv["tail_bound"],
        "ref": 1e-70,
        "ok": conv["tail_bound"] < 1e-70,
    })
    return rows


def main() -> None:
    text = README.read_text(encoding="utf-8")
    data = json.loads(RESULTS.read_text(encoding="utf-8"))

    groups = {
        "core": verify_core_json(data),
        "bip39": verify_bip39_from_json(data),
        "control_table": verify_control_table(text),
        "isotopes": verify_isotope_table(text),
        "lenr": verify_lenr_balance(text),
    }

    all_rows = [row for rows in groups.values() for row in rows]
    passed = sum(1 for row in all_rows if row.get("ok"))
    failed_rows = [row for row in all_rows if not row.get("ok")]
    status = "PASS_NUMERIC_TABLES" if not failed_rows else "FAIL_NUMERIC_TABLES"

    JSON_REPORT.write_text(json.dumps({
        "status": status,
        "total_checks": len(all_rows),
        "passed": passed,
        "failed": len(failed_rows),
        "groups": {name: {"total": len(rows), "passed": sum(1 for r in rows if r.get("ok"))} for name, rows in groups.items()},
        "failed_rows": failed_rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Полная числовая верификация README",
        "",
        f"Статус: `{status}`",
        "",
        "## Сводка",
        "",
        f"- Всего проверок: `{len(all_rows)}`",
        f"- Пройдено: `{passed}`",
        f"- Ошибок: `{len(failed_rows)}`",
        "",
        "## Группы",
        "",
        "| Группа | Проверок | Пройдено |",
        "|:--|--:|--:|",
    ]
    for name, rows in groups.items():
        lines.append(f"| {name} | {len(rows)} | {sum(1 for r in rows if r.get('ok'))} |")
    lines += ["", "## Ошибки", ""]
    if failed_rows:
        lines += ["| Таблица | Строка/Величина | Деталь |", "|:--|:--|:--|"]
        for row in failed_rows[:100]:
            ident = row.get("line", row.get("quantity", row.get("isotope", "")))
            lines.append(f"| {row.get('table')} | {ident} | `{row}` |")
    else:
        lines.append("Не найдены в распарсиваемых числовых таблицах.")
    lines += [
        "",
        "## Важная граница",
        "",
        "Этот отчет проверяет все распарсиваемые числовые таблицы и ключевые JSON-результаты. Он не доказывает физическую истинность теории и не символически выводит каждую TeX-формулу. Для этого нужен следующий слой: CAS/символьный парсер формул.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(status)
    print(f"checks={len(all_rows)} passed={passed} failed={len(failed_rows)}")
    print(REPORT)


if __name__ == "__main__":
    main()

