#!/usr/bin/env python3
"""Машинная проверка согласованной русской теории."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "docs" / "UNIFIED_CONSISTENT_THEORY_RU.md"
RESULTS = ROOT / "complete_theory_kit" / "results" / "full_theory_results.json"
REPORT = ROOT / "reports" / "MACHINE_VERIFICATION_REPORT.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def rel(calculated: float, reference: float) -> float:
    return abs(calculated - reference) / abs(reference) * 100.0


def main() -> None:
    if not TARGET.exists():
        fail(f"нет файла {TARGET}")
    if not RESULTS.exists():
        fail(f"нет файла {RESULTS}")

    text = TARGET.read_text(encoding="utf-8")
    data = json.loads(RESULTS.read_text(encoding="utf-8"))

    required_fragments = [
        r"\mathfrak U",
        "конечная, единая, абсолютно сходящаяся физика",
        r"\chi_I=2K^2+2K+1=85",
        "C_p=0.933350796",
        "C_W=0.982539",
        "Теорема абсолютной сходимости",
    ]
    forbidden_fragments = [
        "3.8472 | Регулярность",
        "4\\pi\\alpha \\cdot \\frac{f_1}{K} = 4\\pi",
        "| $m_e/(K f_1^6)$ | 5.60",
        "f_1^6 f_2 f_3^{-1} f_5 f_6$ | 938.3",
    ]

    for fragment in required_fragments:
        if fragment not in text:
            fail(f"обязательный фрагмент не найден: {fragment}")

    forbidden_hits = [fragment for fragment in forbidden_fragments if fragment in text]
    if forbidden_hits:
        fail("найдены старые несогласованные фрагменты: " + ", ".join(forbidden_hits))

    params = data["parameters"]
    f = data["structural_functions"]
    if abs(f["f2"] * f["f5"] - params["K"]) > 1e-12:
        fail("тождество f2*f5=K не выполнено")

    checks = {row["name"]: row for row in data["headline_constants"]}
    thresholds = {
        "alpha": 0.02,
        "alpha_s": 5.0,
        "g_I^2": 0.5,
        "G_raw_README_formula": 0.05,
        "infoton_mass": 0.02,
        "proton_mass": 1e-5,
        "W_mass": 1e-4,
    }
    for name, threshold in thresholds.items():
        err = checks[name]["relative_error_percent"]
        if err > threshold:
            fail(f"{name}: ошибка {err} выше порога {threshold}")

    convergence = data["convergence"][-1]
    if convergence["tail_bound"] > 1e-70:
        fail("хвост ряда слишком велик")

    graph = data["finite_graph"]
    if graph["trace_error"] > 1e-7:
        fail("след лапласиана не совпадает с суммой спектра")
    if graph["zero_modes_approx"] != 1:
        fail("ожидалась одна нулевая мода связного графа")

    lines = [
        "# Машинный отчет проверки единой согласованной теории",
        "",
        "Статус: PASS",
        "",
        "## Проверенные условия",
        "",
        "- файл `UNIFIED_CONSISTENT_THEORY_RU.md` существует;",
        "- финальная формула `\\mathfrak U` найдена;",
        "- старые несогласованные фрагменты не найдены;",
        "- тождество `f2*f5=K` выполнено;",
        "- ключевые ошибки находятся ниже заданных порогов;",
        "- хвост сходящегося ряда мал;",
        "- спектр лапласиана согласован со следом;",
        "- граф имеет одну нулевую моду.",
        "",
        "## Ключевые ошибки",
        "",
        "| Проверка | Ошибка, % | Порог, % |",
        "|:--|--:|--:|",
    ]
    for name, threshold in thresholds.items():
        lines.append(f"| {name} | {checks[name]['relative_error_percent']:.12g} | {threshold} |")
    lines += [
        "",
        "## Финальный вывод",
        "",
        "Согласованная русская теория прошла машинную проверку текущего набора критериев.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("MACHINE VERIFY: PASS")
    print(REPORT)


if __name__ == "__main__":
    main()

