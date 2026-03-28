from __future__ import annotations

from pathlib import Path
import pandas as pd
import pypsa

from store2hydro_markets.io import load_network
from store2hydro_markets.analysis.case_a import summarize_case_a, results_to_frame


def solve_energy_only(n: pypsa.Network, solver_name: str = "highs", solver_options: dict | None = None) -> pypsa.Network:
    """
    Solve the standard energy-only case using the network as provided.
    """
    solver_options = solver_options or {}

    if hasattr(n, "optimize"):
        n.optimize(solver_name=solver_name, solver_options=solver_options)
    else:
        raise RuntimeError("This PyPSA version does not expose n.optimize().")

    return n


def run_case_a_for_network(
    network_path: str | Path,
    scenario_name: str,
    solver_name: str = "highs",
    solver_options: dict | None = None,
) -> tuple[pypsa.Network, pd.DataFrame]:
    n = load_network(network_path)
    n = solve_energy_only(n, solver_name=solver_name, solver_options=solver_options)
    summary = summarize_case_a(n, scenario_name)
    return n, results_to_frame([summary])


def compare_case_a(
    baseline_path: str | Path,
    retrofit_path: str | Path,
    solver_name: str = "highs",
    solver_options: dict | None = None,
) -> pd.DataFrame:
    _, baseline_df = run_case_a_for_network(
        baseline_path,
        scenario_name="baseline",
        solver_name=solver_name,
        solver_options=solver_options,
    )
    _, retrofit_df = run_case_a_for_network(
        retrofit_path,
        scenario_name="retrofit",
        solver_name=solver_name,
        solver_options=solver_options,
    )

    df = pd.concat([baseline_df, retrofit_df], ignore_index=True)

    if len(df) == 2:
        numeric_cols = df.select_dtypes(include="number").columns
        delta = {"scenario_name": "retrofit_minus_baseline"}
        for col in numeric_cols:
            delta[col] = df.loc[1, col] - df.loc[0, col]
        df = pd.concat([df, pd.DataFrame([delta])], ignore_index=True)

    return df
