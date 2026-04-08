# Machine learning (undergraduate)

## Overview

Two coursework notebooks: **gradient-based optimization** on a fixed univariate polynomial, and a structured **K-means clustering** report with background, math, and implementation-style code.

## Files

| File | Content |
|------|---------|
| `Gradient Descent.ipynb` | Student ID `22000724`; plots and optimization for \(f(x)=2x^4-10x^3+8x^2+5x\) (markdown title); includes embedded figures. |
| `Kmeans.ipynb` | Authored by **Eunbi Cho** (`22000724@handong.ac.kr`, GitHub `eunbijoel`). Parts: background of k-means, key concepts (objective / Lloyd’s idea), implementation and experiments. |

## Execution flow

```text
Gradient Descent.ipynb
 └─ markdown problem statement
 └─ code cells: define f, derivatives, GD loop, plots

Kmeans.ipynb
 └─ exposition cells
 └─ code: data generation or loading (per notebook), k-means steps, visualization
```

## How to run

1. `pip install numpy matplotlib` (add `scikit-learn` if k-means uses sklearn).
2. Open each notebook and run **Restart kernel & run all** after trusting the notebook.
3. `Gradient Descent.ipynb` is **large** (embedded images); use a capable editor or clear outputs if size is problematic.

## Data / assets

- **Gradient Descent**: self-contained math + plots; embedded PNG in markdown may bloat file size.
- **Kmeans**: relies on cells as authored (synthetic or loaded data — confirm in notebook before presenting).

## Improvements

- Export `Gradient Descent` outputs to `outputs/` and strip base64 from `.ipynb` for smaller git diffs.
- Split `Kmeans.ipynb` into `notebooks/` + `src/kmeans.py` if you want importable modules.
