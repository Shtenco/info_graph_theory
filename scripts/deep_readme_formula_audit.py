#!/usr/bin/env python3
"""Глубокий аудит README: самосогласованность ключевых формул и старые фрагменты."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
RESULTS = ROOT / "complete_theory_kit" / "results" / "full_theory_results.json"
REPORT = ROOT / "reports" / "DEEP_README_FORMULA_AUDIT.md"


def line_hits(text: str, patterns: list[tuple[str, str]]) -> list[dict[str, str | int]]:
    lines = text.splitlines()
    hits = []
    for i, line in enumerate(lines, 1):
        for label, pattern in patterns:
            if re.search(pattern, line):
                hits.append({"line": i, "label": label, "text": line.strip()})
    return hits


def main() -> None:
    text = README.read_text(encoding="utf-8")
    analysis_text = text.split("# Базовый машинный отчет", 1)[0]
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    params = data["parameters"]
    f = data["structural_functions"]
    checks = {row["name"]: row for row in data["headline_constants"]}

    # Patterns are grouped by severity. Historical mentions in audit tables are
    # acceptable but still recorded as historical, not active formula failures.
    suspicious_patterns = [
        ("old_f5_value", r"3\.8472"),
        ("old_gI_factor", r"4\\pi\\alpha"),
        ("old_infoton_without_chi", r"(?<!chi_I )(?<!\\chi_I )m_e/\(K f_1\^6\)"),
        ("old_proton_f3_formula", r"f_1\^6 f_2 f_3\^\{-1\} f_5 f_6"),
        ("old_spectrum_master_formula", r"M_\w*\s*=\s*M_\{?Inf\}?.*f_3\^\{?c\}?"),
        ("unverified_full_71_claim", r"71.*констант|69.*71|p < 10\^\{-1000\}|50\\sigma"),
        ("unverified_106_claim", r"106 частиц"),
        ("unverified_all_rows_claim", r"0\.0%"),
    ]
    hits = line_hits(analysis_text, suspicious_patterns)

    active_failures = []
    historical_mentions = []
    for hit in hits:
        line = int(hit["line"])
        label = str(hit["label"])
        # Lines inside the audit section that explicitly compare "was -> became"
        # are historical, not active formulas.
        if (
            (2500 <= line <= 2800 and label in {"old_f5_value", "old_gI_factor"})
            or ("было" in str(hit["text"]).lower() and "стало" in str(hit["text"]).lower())
            or ("$K/\\ln K=3.8472$" in str(hit["text"]) and "$K/\\ln K=3.3487$" in str(hit["text"]))
            or ("$4\\pi\\alpha f_1/K=0.801$" in str(hit["text"]) and "$2\\pi\\alpha" in str(hit["text"]))
        ):
            historical_mentions.append(hit)
        elif label == "unverified_all_rows_claim":
            historical_mentions.append(hit)
        elif label in {"unverified_full_71_claim", "unverified_106_claim"}:
            historical_mentions.append(hit)
        else:
            active_failures.append(hit)

    numeric_checks = []
    K = params["K"]
    f2, f5 = f["f2"], f["f5"]
    numeric_checks.append(("f2*f5=K", f2 * f5, K, abs(f2 * f5 - K)))
    numeric_checks.append(("alpha", checks["alpha"]["calculated"], checks["alpha"]["reference"], checks["alpha"]["relative_error_percent"]))
    numeric_checks.append(("g_I^2", checks["g_I^2"]["calculated"], checks["g_I^2"]["reference"], checks["g_I^2"]["relative_error_percent"]))
    numeric_checks.append(("infoton_mass", checks["infoton_mass"]["calculated"], checks["infoton_mass"]["reference"], checks["infoton_mass"]["relative_error_percent"]))
    numeric_checks.append(("proton_mass", checks["proton_mass"]["calculated"], checks["proton_mass"]["reference"], checks["proton_mass"]["relative_error_percent"]))
    numeric_checks.append(("W_mass", checks["W_mass"]["calculated"], checks["W_mass"]["reference"], checks["W_mass"]["relative_error_percent"]))

    # Estimate coverage: formulas/statements in README vs formulas checked by current Python.
    formula_lines = [
        (i, line.strip())
        for i, line in enumerate(analysis_text.splitlines(), 1)
        if ("$" in line or "\\" in line) and not line.strip().startswith("|:--")
    ]
    checked_items = len(checks) + len(data["bip39"]) + 3  # convergence, graph trace, f2*f5

    status = "PASS_WITH_LIMITATIONS" if not active_failures else "FAIL_ACTIVE_INCONSISTENCIES"

    out = [
        "# Глубокий аудит формул README",
        "",
        f"Статус: `{status}`",
        "",
        "## Краткий вывод",
        "",
    ]
    if active_failures:
        out += [
            "В README найдены активные фрагменты, похожие на старые или несогласованные формулы. Их нужно исправить перед заявлением полной самосогласованности.",
            "",
        ]
    else:
        out += [
            "Активных старых формул из известного набора проблем не найдено. Однако это не является доказательством правильности всех формул огромной теории: текущий Python-аудит покрывает ключевой слой, но не каждую строку README.",
            "",
        ]

    out += [
        "## Машинно проверенные числовые условия",
        "",
        "| Условие | Расчет | Референс | Ошибка / расхождение |",
        "|:--|--:|--:|--:|",
    ]
    for name, calc, ref, err in numeric_checks:
        out.append(f"| {name} | {calc:.12g} | {ref:.12g} | {err:.12g} |")

    out += [
        "",
        "## Активные проблемные фрагменты",
        "",
    ]
    if active_failures:
        out += ["| Строка | Тип | Текст |", "|--:|:--|:--|"]
        for h in active_failures:
            out.append(f"| {h['line']} | `{h['label']}` | {h['text']} |")
    else:
        out.append("Не найдены.")

    out += [
        "",
        "## Исторические или неполностью проверенные утверждения",
        "",
        "Эти строки не обязательно являются ошибкой, но они не должны считаться полностью доказанными текущим Python-набором.",
        "",
    ]
    if historical_mentions:
        out += ["| Строка | Тип | Текст |", "|--:|:--|:--|"]
        for h in historical_mentions[:80]:
            out.append(f"| {h['line']} | `{h['label']}` | {h['text']} |")
        if len(historical_mentions) > 80:
            out.append(f"| ... | ... | еще {len(historical_mentions)-80} строк |")
    else:
        out.append("Не найдены.")

    out += [
        "",
        "## Покрытие проверки",
        "",
        f"- строк с формульными признаками в README: `{len(formula_lines)}`",
        f"- элементов, явно проверяемых текущим Python-аудитом: примерно `{checked_items}`",
        "",
        "Следовательно, утверждение `все формулы README полностью доказаны машинно` пока слишком сильное. Корректное утверждение: `ключевой согласованный слой прошел машинную проверку; полный формальный аудит всех формул требует расширения парсера и тестов`.",
        "",
        "## Рекомендация",
        "",
        "Для полной самосогласованности следующего уровня нужно добавить машинные тесты для всех таблиц: 71 константы, 106 частиц, ядерных масс, времен жизни, космологии и LENR-баланса.",
    ]
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(status)
    print(REPORT)


if __name__ == "__main__":
    main()

