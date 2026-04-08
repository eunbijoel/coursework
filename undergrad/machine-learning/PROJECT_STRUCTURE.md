# PROJECT_STRUCTURE — `machine-learning`

## Entry points

| Artifact | Role |
|----------|------|
| `Gradient Descent.ipynb` | Optimization demo / assignment for a single-variable polynomial. |
| `Kmeans.ipynb` | Pedagogical + implementation notebook for k-means. |

## Call graph (conceptual)

```text
Gradient Descent.ipynb
 └─ f(x), f'(x) [in cells]
 └─ gradient descent update loop
 └─ matplotlib figures

Kmeans.ipynb
 └─ narrative markdown
 └─ clustering implementation cells
 └─ evaluation / visualization cells
```

## I/O

| Notebook | Typical input | Typical output |
|----------|---------------|----------------|
| Gradient Descent | Coefficients / step size hyperparameters in cells | Numeric sequence, plots |
| Kmeans | In-notebook arrays or loaded CSV (verify) | Cluster labels, plots |

## What to edit for which purpose

| Task | Location | Caution |
|------|----------|---------|
| Change learning rate / iterations | GD notebook parameter cells | Stability / divergence |
| Change k or distance metric | Kmeans notebook | Algorithm assumptions change |

## Risks when modifying

- Clearing outputs in `Gradient Descent.ipynb` without backing up may remove reference figures you use in reports.
- If k-means is implemented manually, vectorization bugs are easy; add small asserts vs sklearn for sanity checks.
