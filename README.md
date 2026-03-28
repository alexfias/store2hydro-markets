# store2hydro-markets

A PyPSA-based framework to evaluate the value of retrofitting existing hydropower dams with pumping capability under different electricity market designs.

## Overview

This repository provides the **market valuation layer** of the *store2hydro* project.

It takes existing PyPSA(-Eur) networks as input and evaluates the **system and economic value of hydro retrofit** under different market configurations.

The repository does **not construct retrofit assets itself**. Instead, it compares different **predefined system configurations**, such as:

- a baseline network (no retrofit)
- a retrofit network (hydro plants equipped with pumping capability)

---

## Key Idea

We evaluate:

> What is the incremental value of hydro retrofit under different electricity market designs?

This is done by comparing identical systems with and without retrofit across multiple market settings.

---

## Market Cases

The framework evaluates four market designs:

- **Case A: Energy-only**
  - Standard energy market (baseline PyPSA setup)

- **Case B: Energy + reserve capacity**
  - Adds reserve capacity provision and feasibility constraints

- **Case C: Energy + reserve capacity + activation**
  - Includes expected reserve activation and impacts on dispatch and storage

- **Case D: Uncertain reserve prices**
  - Introduces stochasticity in reserve market revenues

---

## Project Scope (v0.1)

Initial focus:

- Load existing PyPSA networks (`.nc` or CSV folder)
- Evaluate different system configurations:
  - baseline (no retrofit)
  - retrofit scenario (provided as input)
- Implement and run **Case A (energy-only)**
- Compare system operation and revenues across configurations

---

## Workflow

Typical pipeline:

```python
n = load_network(path)

n = apply_market_case(n, case)   # A–D

n.optimize()

results = analyze(n)

## Repository Structure

store2hydro-markets/
├─ configs/
├─ src/store2hydro_markets/
│  ├─ io.py
│  ├─ cases/
│  ├─ analysis/
├─ notebooks/
├─ runs/

##Input Assumptions

Networks are provided as:
NetCDF files (.nc), or
PyPSA CSV folders
Hydro retrofit (if present) is already encoded in the network
The same base network structure should be used across comparisons

## Experimental Design

The framework compares along two dimensions:

1. Asset configuration
baseline hydro system
retrofitted hydro system
2. Market design
Case A → D

This enables clean identification of:

the value of retrofit
the impact of market design

## Key Concept

We evaluate the incremental value of adding pumping capability to existing hydro reservoirs.

## Status

Early development (v0.1)

## Future Extensions

Reserve capacity modeling (Case B)
Activation modeling (Case C)
Stochastic optimization (Case D)
Endogenous retrofit investment (optional future work)
Integration with PyPSA-Eur workflows

## License

MIT 
