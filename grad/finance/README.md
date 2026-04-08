# Finance — graduate (KAIST)

## Overview

Individual project for **BTM50039 — AI for Business Management** (course metadata in notebook header). Student ID **20243788**, **Eunbi Cho**. Work centers on **HYBE**-related financial / managerial analytics using **tabular and time-oriented methods**: regression baselines, **XGBoost**, **SHAP** explanations, **tslearn** (e.g. DTW-related tooling), **DBSCAN**, **KMeans**, and interactive **Plotly** visuals where used.

## File


| File                          | Role                                                                                                                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `Hybe_finance analysis.ipynb` | End-to-end notebook: Colab drive mount to `.../KAIST/25_01/인공지능`, heavy stack of imports, data prep, modeling, SHAP, clustering sections. |


## Execution flow (high level)

```text
Hybe_finance analysis.ipynb
 └─ Colab: mount + chdir
 └─ imports (sklearn, xgboost, tslearn, shap, plotly, seaborn, …)
 └─ load / prepare dataset (see notebook for filenames)
 └─ regression + model comparison + metrics
 └─ SHAP explainability (XGBoost-focused sections)
 └─ time-series / clustering experiments (DBSCAN, KMeans, tslearn utilities)
```

## Data dependencies

Notebook paths point to the author’s Google Drive. **Identify `read_csv` / `read_excel` / similar calls inside the notebook** and mirror those files locally under `data/` before public reproducibility claims.

## How to run locally

1. Create a venv; install packages from repo root `requirements.txt` (you may need version pinning for `shap` / `xgboost` compatibility).
2. Replace Colab cells with local paths.
3. Run sequentially; expect **long runtime** for some model fits and SHAP.

## Ethics / disclosure

- If HYBE or market data are proprietary or licensed, keep them out of git and describe acquisition only at a high level in README.

## Improvements

- Split into `notebooks/01_eda.ipynb`, `02_regression.ipynb`, etc., once stable.
- Save key SHAP plots to `outputs/` with deterministic seeds documented.

