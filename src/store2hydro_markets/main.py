from __future__ import annotations

import argparse
from pathlib import Path

from store2hydro_markets.cases.case_a import compare_case_a


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run store2hydro market cases.")
    parser.add_argument("--baseline", required=True, help="Path to baseline network (.nc or CSV folder)")
    parser.add_argument("--retrofit", required=True, help="Path to retrofit network (.nc or CSV folder)")
    parser.add_argument("--solver", default="highs", help="Solver name, e.g. highs or gurobi")
    parser.add_argument("--output", default="runs/case_a_comparison.csv", help="Output CSV file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    comparison = compare_case_a(
        baseline_path=args.baseline,
        retrofit_path=args.retrofit,
        solver_name=args.solver,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(output_path, index=False)

    print(comparison)
    print(f"\nSaved comparison to {output_path}")


if __name__ == "__main__":
    main()
