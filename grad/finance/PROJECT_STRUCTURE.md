# PROJECT_STRUCTURE — `grad/finance`

## Entry point

- `Hybe_finance analysis.ipynb` (filename contains a space; quote paths in shell commands).

## Module layout

No `.py` package; logic is **notebook-scoped**.

## Subsystem map (text diagram)

```text
Hybe_finance analysis.ipynb
 ├─ Data ingest  ──►  DataFrame(s)
 ├─ Regression suite  ──►  LinearRegression, RandomForest, XGBoost, SVR, MLPRegressor, …
 │        └─ metrics: R², MSE, MAE (as coded)
 ├─ SHAP  ──►  explainability plots / summaries
 └─ Clustering / time-series  ──►  DBSCAN, KMeans, tslearn preprocessing / cdist_dtw usage
```

## What to modify for which purpose


| Goal                 | Where                            | Risk                            |
| -------------------- | -------------------------------- | ------------------------------- |
| New target variable  | Feature definition cells         | Leakage if future info included |
| Different model list | Model definition / training loop | Metric comparison validity      |
| Faster iteration     | Subsample data                   | Conclusions may not generalize  |


## Dependencies observed in imports

`pandas`, `numpy`, `sklearn` (multiple estimators), `xgboost`, `tslearn`, `shap`, `matplotlib`, `seaborn`, `plotly`, `DBSCAN`, `KMeans`, etc. — see first import cell for authoritative list.

## Verification caveat

Notebook is large; this document reflects **header cells and grep-visible section titles** (e.g. “Regression and SHAP”). Re-validate section order before citing in a paper or presentation.