# store2hydro-markets

A PyPSA-based framework to evaluate the value of retrofitting existing hydropower dams with pumping capability under different electricity market designs.

## Overview

This repository builds on an existing PyPSA(-Eur) network and evaluates the incremental value of hydro retrofit across multiple market configurations.

We consider existing reservoir hydropower plants that are retrofitted with pumping capability, allowing them to:
- generate electricity from natural inflow
- store electricity via pumping
- provide flexibility services to the power system

Unlike conventional pumped hydro storage, these assets retain natural inflow, making them hybrid inflow-storage systems.

## Market Cases

The framework evaluates four market settings:

- Case A: Energy-only
- Case B: Energy + reserve capacity
- Case C: Energy + reserve capacity + activation
- Case D: Uncertain reserve prices

## Project Scope (v0.1)

Initial focus:

- Load an existing PyPSA network (.nc or CSV folder)
- Add fixed-size pumping retrofit to selected hydro reservoirs
- Run Case A (energy-only)
- Compare baseline vs retrofit

## Workflow

Typical pipeline:

n = load_network(path)
n = apply_retrofit(n, config)
n = apply_market_case(n, case)
n.optimize()
results = analyze(n)

## Repository Structure

store2hydro-markets/
├─ configs/
├─ src/store2hydro_markets/
│  ├─ io.py
│  ├─ retrofit.py
│  ├─ cases/
│  ├─ analysis/
├─ notebooks/
├─ runs/

## Key Concept

We evaluate the incremental value of adding pumping capability to existing hydro reservoirs.

## Status

Early development (v0.1)

## Future Extensions

- Endogenous retrofit investment decisions
- Optimal pumping capacity sizing
- Stochastic optimization

## License

MIT 
