# PROJECT_STRUCTURE — `algorithms`

## Entry points

There is **no single `app.py`**; each notebook is its own entry.

| Notebook | First meaningful stage |
|----------|------------------------|
| `algorithm.ipynb` | Imports + “Process By Hand” / array generation for Algorithm assignment 1. |
| `Divide and Conquer.ipynb` | Markdown brief + point generation + DAC convex hull logic. |
| `Graph Algorithm.ipynb` | Drive mount (Colab) + library install + data load + graph build + Dijkstra. |
| `Generic Algorithm/Team1_Task1.ipynb` | Hyperparameters for GA on a continuous function. |
| `Generic Algorithm/Team1_Task 2.ipynb` | TSP GA formulation + (optional) Colab setup. |

## Structural diagram (logical, not import-based)

```text
algorithm.ipynb
 └─ NumPy arrays + timing + matplotlib plots

Divide and Conquer.ipynb
 └─ generate_valid_points()
 └─ convex hull DAC routines (defined in notebook)
 └─ visualization

Graph Algorithm.ipynb
 └─ load geographic/table data
 └─ build weighted graph (haversine)
 └─ Dijkstra + path reconstruction
 └─ scenario plots (good / bad weather sections)

Team1_Task1.ipynb
 └─ GA loop optimizing mathematical objective

Team1_Task 2.ipynb
 └─ GA encoding of TSP tours
 └─ fitness / crossover / mutation (see notebook cells)
```

## Experimental vs core (within coursework sense)

| Notebook | “Core” submission logic | Experimental |
|----------|-------------------------|--------------|
| All | Cells that produce required figures / answers | Parameter sweeps, extra plots, Chat-GPT noted penalty experiments in graph notebook |

## Modification risks

| Change | Risk |
|--------|------|
| Renaming notebook files | Breaks references in README / reports. |
| Editing graph data paths without documenting | Notebook becomes non-runnable. |
| Refactoring into `.py` modules | Must update notebook imports and working directory. |

## Functions / classes

No separate `.py` modules were present at documentation time; **all definitions live inside notebook cells**. For a function-level table, run prompt **E** from your workflow *against the live notebook* after any edit.
