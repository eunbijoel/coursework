# Financial data analysis (undergraduate)

## Overview

Mid-term style work using **Korean equity data in Parquet** format: loading multiple parquet files, deriving or analyzing return horizons (notebook comments reference **3 / 6 / 12 month** return windows in Korean).

## File

| File | Role |
|------|------|
| `stock data analysis.ipynb` | Colab-oriented: mounts Drive, `cd` into course folder, installs `pyarrow`, loads parquet datasets with Korean filenames. |

## Data dependencies (from notebook source)

Notebook references (names transcribed from code — copy exactly from the notebook if your files differ):

- `주식_전체_December_from2000_edit.parquet`
- `주식_전체_from2000_edit.parquet` (comment: daily data for multi-month return horizons)
- `A000020.동화약품~A123690.한국화장품_전처리파일_주식_December_from2000.parquet`

These files are **not** committed (see root `.gitignore`). Place them under e.g. `data/` and update paths.

## Execution flow

```text
stock data analysis.ipynb
 └─ drive.mount + chdir (Colab)
 └─ import pandas, numpy
 └─ pip install pyarrow (if needed)
 └─ read_parquet(...) → analysis cells
```

## How to run locally

1. Install `pandas`, `pyarrow`, `numpy`.
2. Remove or bypass Colab cells; set working directory to where parquet files live.
3. Run all cells top-to-bottom.

## Improvements

- Add `data/README.md` with source of data and column definitions (compliance / ethics for market data).
- Encode filenames in ASCII symlinks or rename files for cross-platform paths.
