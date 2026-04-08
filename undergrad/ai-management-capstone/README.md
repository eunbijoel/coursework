# AI management capstone (undergraduate)

## Overview

Capstone work combining **management / business context** with **data analysis and ML-oriented features** on **K-pop chart and music-video (YouTube) data**. A separate written report (`Big data train.md`) documents **exploratory data analysis (EDA)** on the **Dallas crime** dataset (Stata format) as an earlier structured analytics exercise.

## Objectives

- **Capstone notebook**: Work with tabular chart / MV metadata and engineered audio-related columns (e.g. MFCC summaries, duration, chart dates) for downstream analysis or modeling.
- **Big data train.md**: EDA narrative on Dallas crime data — loading, cleaning context, univariate and multivariate views, and suggestions for predictive or dashboard-style follow-ups.

## Repository files

| File | Role |
|------|------|
| `Capstone project.ipynb` | Main capstone workflow: Colab drive mount, loads `FINAL.csv`, inspects K-pop chart rows and feature columns. |
| `Big data train.md` | Standalone markdown report (EDA on `raw_Dallas.dta`); references embedded figures `image.png`, etc. |

## Execution flow (Capstone notebook)

```text
Capstone project.ipynb
 └─ Mount Google Drive + chdir to Colab project path
 └─ Import pandas / numpy / seaborn / matplotlib
 └─ pd.read_csv('FINAL.csv')  (+ drop index column if present)
 └─ EDA / feature inspection / modeling cells (run top-to-bottom)
```

## Data dependencies

| Artifact | Referenced in | Notes |
|----------|----------------|-------|
| `FINAL.csv` | `Capstone project.ipynb` | Must be co-located or path updated; not stored in git by default. |
| `raw_Dallas.dta` | `Big data train.md` (code snippets) | Stata dataset for Dallas crime EDA; not included. |
| Figure assets (`image.png`, …) | `Big data train.md` | Referenced for rendered report; add under `docs/assets/` if you publish the full write-up. |

## How to run locally

1. Copy `FINAL.csv` into this folder (or subfolder `data/`) and replace the Colab `drive.mount` / `%cd` cells with local paths.
2. Open `Capstone project.ipynb` and run sequentially.
3. For `Big data train.md`, use a Markdown preview; to re-execute code, extract snippets into a notebook and point `pd.read_stata` to your local `.dta` file.

## Possible improvements

- Add `data/README.md` listing column dictionary for `FINAL.csv`.
- Strip or isolate Colab-only cells behind a `LOCAL=1` flag pattern.
- Add a minimal `environment.yml` or pinned `requirements.txt` per project if versions diverge from repo root.
