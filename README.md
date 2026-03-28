# store2hydro-markets

A PyPSA-based framework to evaluate the value of retrofitting existing hydropower dams with pumping capability under different electricity market designs.

## Overview

This repository provides the market valuation layer of the store2hydro project.

It takes existing PyPSA(-Eur) networks as input and evaluates the system and economic value of hydro retrofit under different market configurations.

The repository does not construct retrofit assets itself. Instead, it compares predefined system configurations such as:
- a baseline network without retrofit
- a retrofit network in which hydro plants already have pumping capability

## Market Cases

- Case A: Energy-only
- Case B: Energy + reserve capacity
- Case C: Energy + reserve capacity + activation
- Case D: Uncertain reserve prices

## Current Scope

Initial focus:
- load existing PyPSA networks from `.nc` or CSV
- run Case A for a baseline and retrofit network
- compare objective value, prices, generation, storage behavior, and hydro revenues

## Example

Run from command line:

python -m store2hydro_markets.main \
  --baseline path/to/baseline.nc \
  --retrofit path/to/retrofit.nc \
  --solver highs \
  --output runs/case_a_comparison.csv

## Repository Structure



```text
store2hydro-markets/
├─ configs/
├─ src/store2hydro_markets/
│  ├─ io.py
│  ├─ main.py
│  ├─ cases/
│  │  └─ case_a.py
│  └─ analysis/
│     └─ case_a.py
├─ notebooks/
└─ runs/

```

## Notes

- Networks must already contain the hydro retrofit (if applicable)
- Ensure consistent base network when comparing scenarios

## License

MIT 
