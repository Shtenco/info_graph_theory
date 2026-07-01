#!/usr/bin/env python3
"""Run the complete v2 kit: reproducibility audit plus reduced-model benchmark."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


KIT = Path(__file__).resolve().parent


def run(script: str) -> None:
    subprocess.run([sys.executable, str(KIT / script)], cwd=KIT, check=True)


def main() -> None:
    run("run_full_simulation.py")
    run("unified_action_v3.py")
    run("optimize_reduced_model_v2.py")
    run("optimize_graph_action_v3.py")
    run("graph_automata_field_theory_v4.py")
    run("bip39_unification_search_v5.py")
    run("bip39_no_fit_verification_v6.py")
    run("bip39_all_constants_benchmark_v7.py")
    run("bip39_fit_all_445_v8.py")
    run("symbolic_axiom_system_v9.py")
    run("symbolic_all_445_constants_v10.py")
    run("bip39_symbolic_approximator_v11.py")
    run("sigt_balanced_engine_445_v12.py")
    run("sigt_predictive_victory_attempt_v13.py")
    print("COMPLETE_THEORY_KIT_V2: OK")


if __name__ == "__main__":
    main()
