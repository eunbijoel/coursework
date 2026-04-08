# Machine learning (undergraduate)

## Overview

Two coursework notebooks: **gradient-based optimization** on a fixed univariate polynomial, and a structured **K-means clustering** report with background, math, and implementation-style code.

## Files


| File                     | Content                                                                                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Gradient Descent.ipynb` | Gradient descent on f(x)=2x^4-10x^3+8x^2+5x; figures may be inline base64 (see below) or under `images/` after extraction.                                                       |
| `Kmeans.ipynb`           | Authored by **Eunbi Cho** (`22000724@handong.ac.kr`, GitHub `eunbijoel`). Parts: background of k-means, key concepts (objective / Lloyd’s idea), implementation and experiments. |


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
3. `**Gradient Descent.ipynb` looks like one giant JSON line?** That is normal when the notebook stores images as **base64 inside markdown**. Cursor’s **text** editor is painful for that.

### Readable preview in Cursor

- Open `**Gradient Descent.ipynb`** and use the **Notebook** view (cell layout), not raw `.ipynb` JSON. If it opens as plain text, try **Open With…** and pick the notebook editor, or open from the file explorer with the notebook icon behavior your build uses.

### Optional: pull images out of the notebook (recommended once)

From this folder in PowerShell:

```powershell
python .\extract_embedded_images.py
```

This creates `images/figure-*.png`, replaces `data:image/...;base64,...` with `![](images/figure-N.png)`, and rewrites the `.ipynb` with **indented JSON** so the file is easier to sanity-check in git diffs.

## Data / assets

- **Gradient Descent**: after extraction, figures live in `images/`; commit those PNGs if you want them on GitHub.
- **Kmeans**: relies on cells as authored (synthetic or loaded data — confirm in notebook before presenting).

## Improvements

- Export `Gradient Descent` outputs to `outputs/` and strip base64 from `.ipynb` for smaller git diffs.
- Split `Kmeans.ipynb` into `notebooks/` + `src/kmeans.py` if you want importable modules.

