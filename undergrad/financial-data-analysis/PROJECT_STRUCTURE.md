# PROJECT_STRUCTURE — `financial-data-analysis`

## Entry point

- `stock data analysis.ipynb` — sole executable artifact in this folder.

## Data flow

```text
*.parquet (local or Drive)
      │
      ▼
pandas.read_parquet(engine="pyarrow")
      │
      ▼
downstream feature / return calculations (see notebook)
```

## Responsibilities

| Component | Responsibility |
|-----------|----------------|
| Early Colab cells | Environment setup; **must be replaced** for local runs. |
| `read_parquet` cells | Bind variable names `stock_df`, `full_stock_df`, `acc_df` (as in source). |
| Later cells | Analysis specific to course mid-term (inspect notebook). |

## Modification risks

| Change | Risk |
|--------|------|
| Renaming parquet files without updating all `read_parquet` calls | Silent failure or wrong dataframe. |
| Mixing engines (`fastparquet` vs `pyarrow`) | Dtype / null handling differences. |

## Uncertainty

- Full analytical narrative and all intermediate variables were not re-executed during documentation; **open the notebook** for the authoritative flow after the load section.
