# Coursework archive

**Eunbi Cho** · `[@eunbijoel](https://github.com/eunbijoel)` 

Personal repository of **undergraduate and graduate coursework** (notebooks, assignments, small projects), grouped by stage and topic. This is a **portfolio / archive**: not all paths are one-click reproducible without local data and path fixes.

Each leaf folder has a **README** (overview, how to run, data). Several folders also add **PROJECT_STRUCTURE.md** for extra architecture notes; `**undergrad/machine-learning/`** keeps everything in **README.md** only.

---

## Layout

```text
coursework/
├── README.md                 # This file
├── requirements.txt          # Suggested Python dependencies (not frozen)
├── .gitignore                # venv, checkpoints, common large data extensions
├── undergrad/
│   ├── ai-management-capstone/
│   ├── algorithms/
│   ├── machine-learning/
│   └── financial-data-analysis/
└── grad/
    ├── finance/
    ├── nlp/                  # Placeholder (no artifacts here yet)
    └── ra-scholar-frus-news/ # Placeholder (public release TBD)
```

---

## Project index


| Path                                 | Summary                                                                                            | Primary artifacts                             |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `undergrad/ai-management-capstone/`  | AI × management capstone: K-pop chart / MV features (`FINAL.csv` pipeline).                        | `Capstone project.ipynb`, `Big data train.md` |
| `undergrad/algorithms/`              | DAC convex hull, graph + Dijkstra, genetic algorithms (TSP, function optimization), misc.          | Several `.ipynb` (see folder README)          |
| `undergrad/machine-learning/`        | Gradient descent on a polynomial; K-means (background + code).                                     | `Gradient Descent.ipynb`, `Kmeans.ipynb`      |
| `undergrad/financial-data-analysis/` | Korean equity parquet workflows (mid-term style).                                                  | `stock data analysis.ipynb`                   |
| `grad/finance/`                      | KAIST *AI for Business Management*: HYBE-oriented analysis, regression, SHAP, time-series tooling. | `Hybe_finance analysis.ipynb`                 |
| `grad/nlp/`                          | Reserved for NLP work.                                                                             | —                                             |
| `grad/ra-scholar-frus-news/`         | Reserved for RA-related Scholar / news data work.                                                  | —                                             |


