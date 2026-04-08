# Coursework archive (undergrad & graduate)

Monorepo of coursework and small projects by **Eunbi Cho** (`eunbijoel`), organized by education stage and topic. Each leaf folder has its own **README** (overview, how to run, data dependencies) and **PROJECT_STRUCTURE** (inventory, flow, modification risks).

## Repository layout

```text
coursework/
├── README.md                 # This file
├── requirements.txt          # Suggested Python dependencies (not frozen)
├── .gitignore                # Ignores checkpoints, venv, common data extensions
├── undergrad/
│   ├── ai-management-capstone/
│   ├── algorithms/
│   ├── machine-learning/
│   └── financial-data-analysis/
└── grad/
    ├── finance/
    ├── nlp/                  # Placeholder (no artifacts committed yet)
    └── ra-scholar-frus-news/ # Placeholder (no artifacts committed yet)
```

## Project index

| Path | Summary | Primary artifacts |
|------|---------|-------------------|
| `undergrad/ai-management-capstone/` | AI × management capstone: K-pop chart / MV features (`FINAL.csv` pipeline). | `Capstone project.ipynb`, `Big data train.md` |
| `undergrad/algorithms/` | Assignments: divide & conquer convex hull, graph + Dijkstra, genetic algorithm (TSP, function opt), misc. | Several `.ipynb` (see folder README) |
| `undergrad/machine-learning/` | ML coursework: gradient descent on polynomial, K-means theory + implementation. | `Gradient Descent.ipynb`, `Kmeans.ipynb` |
| `undergrad/financial-data-analysis/` | Financial data analysis mid-term: Korean equity parquet inputs, returns features. | `stock data analysis.ipynb` |
| `grad/finance/` | KAIST *AI for Business Management* individual project: HYBE-oriented modeling, regression, SHAP, time-series tools. | `Hybe_finance analysis.ipynb` |
| `grad/nlp/` | Reserved for NLP work. | — |
| `grad/ra-scholar-frus-news/` | Reserved for RA-related Scholar / news data work (public release TBD). | — |

## How to use this repo

1. **Python environment**  
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. **Open notebooks**  
   Start Jupyter from the repository root (or open folders in VS Code / Cursor with Jupyter support).

3. **Data paths**  
   Many notebooks were authored in **Google Colab** and reference paths under Google Drive (e.g. `%cd '/content/drive/...'`). Those cells will **not** run as-is on a local machine until you:
   - place the same files next to the notebook, **or**
   - update `read_csv` / `read_parquet` / `read_stata` paths to your local `data/` layout.

   Each subfolder README lists **expected inputs** where identifiable from the notebook source.

4. **Git LFS / large files**  
   `.gitignore` excludes common data extensions to avoid accidental commits of huge datasets. If you intentionally version sample data, use a `data/sample/` policy and document it in the relevant README.

## Verification note

Documentation here was produced by **reading the committed notebooks and markdown** in this tree. If a notebook was edited after the last doc update, re-run your own structural review (entry cells, paths, outputs).

## Publish to GitHub

1. Create a new repository **`coursework`** under your user (public, no template README).  
2. In PowerShell:
   ```powershell
   Set-Location C:\Users\keti\coursework
   powershell -ExecutionPolicy Bypass -File .\push-coursework.ps1
   ```
   Or run `git init`, `git add -A`, `git commit`, `git remote add origin https://github.com/eunbijoel/coursework.git`, `git push -u origin main` yourself.

## License

Add a `LICENSE` file when you decide how this archive may be reused (coursework often stays “all rights reserved” or CC-BY-NC for portfolio use).
