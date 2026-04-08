# PROJECT_STRUCTURE — `ai-management-capstone`

Evidence-oriented map of what exists in this folder. Scope: files present in the repository as analyzed; no invented modules.

## Entry points

| Mode | Entry | Notes |
|------|--------|-------|
| Interactive analysis | `Capstone project.ipynb` | Primary executable artifact. |
| Narrative / report | `Big data train.md` | Human-readable; code blocks are illustrative unless copied into a runnable notebook. |

## Directory structure

```text
ai-management-capstone/
├── README.md
├── PROJECT_STRUCTURE.md
├── Capstone project.ipynb
└── Big data train.md
```

## File responsibilities

| Path | Responsibility |
|------|----------------|
| `Capstone project.ipynb` | Load chart/MV table, explore schema, run analysis cells in order. |
| `Big data train.md` | Document EDA steps and interpretation for Dallas crime data; includes pandas/seaborn/matplotlib snippets. |

## Data flow (Capstone notebook)

```text
FINAL.csv  ──►  pandas DataFrame `df`  ──►  downstream cells (plots, stats, models — as implemented in notebook)
```

## Data flow (Big data train.md narrative)

```text
raw_Dallas.dta  ──►  DataFrame  ──►  cleaning / describe / plots  ──►  written conclusions + project ideas
```

## What to change for which purpose

| Goal | Where to work | Risk |
|------|----------------|------|
| New chart features | New cells or new `.py` module later under `src/` if refactored | Column names must match `FINAL.csv` reality. |
| Reproducible local run | Replace Colab path cells in `Capstone project.ipynb` | Easy to forget drive-specific paths. |
| Publish report | `Big data train.md` + add `docs/assets/` for images | Broken image links if paths move. |

## Dependency surface (from notebook imports)

- `pandas`, `numpy`, `seaborn`, `matplotlib`
- `google.colab` (optional; Colab only)

## Open questions (explicit uncertainty)

- Full list of modeling steps inside `Capstone project.ipynb` was not exhaustively cell-by-cell audited in documentation; **open the notebook** to confirm the latest logic after the first data load.
