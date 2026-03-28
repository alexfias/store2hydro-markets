from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import pandas as pd
import pypsa


@dataclass
class CaseAResults:
    scenario_name: str
    objective: float | None
    total_load_mwh: float
    total_generation_mwh: float
    hydro_generation_mwh: float
    storage_dispatch_mwh: float
    storage_charge_mwh: float
    average_price: float | None
    max_price: float | None
    min_price: float | None
    total_generator_revenue: float | None
    total_hydro_revenue: float | None


def _get_snapshot_weights(n: pypsa.Network) -> pd.Series:
    if hasattr(n, "snapshot_weightings") and "objective" in n.snapshot_weightings:
        return n.snapshot_weightings["objective"]
    return pd.Series(1.0, index=n.snapshots)


def _weighted_sum_over_time(df: pd.DataFrame, weights: pd.Series) -> pd.Series:
    aligned = df.mul(weights, axis=0)
    return aligned.sum(axis=0)


def _total_weighted_sum(df: pd.DataFrame, weights: pd.Series) -> float:
    aligned = df.mul(weights, axis=0)
    return float(aligned.to_numpy().sum())


def _get_bus_prices(n: pypsa.Network) -> pd.DataFrame | None:
    buses_t = getattr(n, "buses_t", None)
    if buses_t is None:
        return None
    if not hasattr(buses_t, "marginal_price"):
        return None
    return buses_t.marginal_price.copy()


def _get_load(n: pypsa.Network, weights: pd.Series) -> float:
    loads_t = getattr(n, "loads_t", None)
    if loads_t is None or not hasattr(loads_t, "p_set"):
        return 0.0
    return _total_weighted_sum(loads_t.p_set, weights)


def _get_total_generation(n: pypsa.Network, weights: pd.Series) -> float:
    generators_t = getattr(n, "generators_t", None)
    if generators_t is None or not hasattr(generators_t, "p"):
        return 0.0
    return _total_weighted_sum(generators_t.p.clip(lower=0.0), weights)


def _get_hydro_generators(n: pypsa.Network) -> pd.Index:
    if "carrier" not in n.generators.columns:
        return pd.Index([])
    hydro_mask = n.generators["carrier"].astype(str).str.contains("hydro", case=False, na=False)
    return n.generators.index[hydro_mask]


def _get_hydro_generation(n: pypsa.Network, weights: pd.Series) -> float:
    hydro_gens = _get_hydro_generators(n)
    if len(hydro_gens) == 0:
        return 0.0
    return _total_weighted_sum(n.generators_t.p[hydro_gens].clip(lower=0.0), weights)


def _get_storage_dispatch_and_charge(n: pypsa.Network, weights: pd.Series) -> tuple[float, float]:
    dispatch = 0.0
    charge = 0.0

    if hasattr(n, "storage_units_t") and hasattr(n.storage_units_t, "p"):
        p = n.storage_units_t.p
        dispatch += _total_weighted_sum(p.clip(lower=0.0), weights)
        charge += _total_weighted_sum((-p.clip(upper=0.0)), weights)

    if hasattr(n, "links_t") and hasattr(n.links_t, "p0"):
        if "carrier" in n.links.columns:
            pump_links = n.links.index[
                n.links["carrier"].astype(str).str.contains("pump", case=False, na=False)
            ]
            if len(pump_links) > 0:
                # Convention: electricity consumption appears on bus0 side, often positive in magnitude
                # depending on PyPSA sign conventions. We use absolute value to stay robust for summary stats.
                charge += _total_weighted_sum(n.links_t.p0[pump_links].abs(), weights)

    return dispatch, charge


def _generator_revenues(n: pypsa.Network, weights: pd.Series) -> tuple[float | None, float | None]:
    prices = _get_bus_prices(n)
    if prices is None:
        return None, None

    if not hasattr(n, "generators_t") or not hasattr(n.generators_t, "p"):
        return None, None

    p = n.generators_t.p.clip(lower=0.0)
    revenues = []

    for gen in n.generators.index:
        bus = n.generators.at[gen, "bus"]
        if bus not in prices.columns:
            continue
        rev = (p[gen] * prices[bus] * weights).sum()
        revenues.append((gen, float(rev)))

    if not revenues:
        return None, None

    revenue_series = pd.Series(dict(revenues))
    hydro_gens = _get_hydro_generators(n)
    hydro_revenue = float(revenue_series.reindex(hydro_gens).fillna(0.0).sum())

    return float(revenue_series.sum()), hydro_revenue


def summarize_case_a(n: pypsa.Network, scenario_name: str) -> CaseAResults:
    weights = _get_snapshot_weights(n)
    prices = _get_bus_prices(n)

    total_generator_revenue, total_hydro_revenue = _generator_revenues(n, weights)
    storage_dispatch, storage_charge = _get_storage_dispatch_and_charge(n, weights)

    if prices is not None and not prices.empty:
        avg_price = float(prices.mean().mean())
        max_price = float(prices.max().max())
        min_price = float(prices.min().min())
    else:
        avg_price = None
        max_price = None
        min_price = None

    objective = getattr(n, "objective", None)
    if objective is not None:
        objective = float(objective)

    return CaseAResults(
        scenario_name=scenario_name,
        objective=objective,
        total_load_mwh=_get_load(n, weights),
        total_generation_mwh=_get_total_generation(n, weights),
        hydro_generation_mwh=_get_hydro_generation(n, weights),
        storage_dispatch_mwh=storage_dispatch,
        storage_charge_mwh=storage_charge,
        average_price=avg_price,
        max_price=max_price,
        min_price=min_price,
        total_generator_revenue=total_generator_revenue,
        total_hydro_revenue=total_hydro_revenue,
    )


def results_to_frame(results: list[CaseAResults]) -> pd.DataFrame:
    return pd.DataFrame([asdict(r) for r in results])
