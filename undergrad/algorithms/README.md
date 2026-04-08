# Algorithms (undergraduate)

## Overview

Collection of **algorithm coursework** in Jupyter notebooks: **divide-and-conquer** geometry, **graph algorithms** with **Dijkstra** shortest paths on real-world styled coordinates, **genetic algorithms** (continuous function optimization and **TSP**), and a general assignment notebook.

> Note: the subfolder is named `Generic Algorithm`; notebook content refers to **genetic** algorithms.

## Files

| Path | Topic (from notebook content) |
|------|------------------------------|
| `algorithm.ipynb` | Assignment #1 style work: sorting / array experiments with NumPy, timing, plotting (`22000724_Eunbi Cho`, Algorithm_01). |
| `Divide and Conquer.ipynb` | Convex hull via **divide-and-conquer** on randomly generated valid planar points (no shared x/y, no collinear triples). |
| `Graph Algorithm.ipynb` | Graph construction, **haversine**-style distances, **Dijkstra** shortest path; weather “good vs bad” variants; plotting paths. |
| `Generic Algorithm/Team1_Task1.ipynb` | **Genetic algorithm** for optimizing a continuous function (SymPy / numpy / matplotlib). |
| `Generic Algorithm/Team1_Task 2.ipynb` | **TSP** solved with a **genetic algorithm** (Colab drive mount in early cells). |

## Execution flow (typical)

Each notebook is **linear top-to-bottom**. There is **no shared Python package** between notebooks; duplication is expected for coursework.

```text
*.ipynb
 └─ (optional) Colab: mount Drive + chdir
 └─ imports
 └─ helper definitions in early cells
 └─ experiments / plots / reported results
```

## How to run

1. Prefer **Jupyter** or **VS Code / Cursor** notebook mode.
2. For `Graph Algorithm.ipynb`, install `haversine` (`pip install haversine`).
3. For genetic-algorithm tasks using **SymPy**, ensure `sympy` is installed.
4. Replace **Colab-only** cells in `Team1_Task 2.ipynb` when running locally.

## Data dependencies

- `Graph Algorithm.ipynb` loads **tabular / coordinate data** from the author’s Drive path in Colab; **local users must supply equivalent CSV** (or similar) and update the load cell. Exact filenames appear in the notebook’s load section (inspect `pd.read_csv` calls).

## Improvement ideas

- Rename folder `Generic Algorithm` → `genetic-algorithm` for clarity (requires git mv + link updates).
- Factor repeated plotting utilities into `src/plotting.py` if you refactor to a package layout.
