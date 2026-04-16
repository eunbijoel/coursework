# Financial data analysis (undergraduate)

## Overview

**Korean equity data in Parquet** format: loading multiple parquet files, deriving or analyzing returns.

## Data dependencies
- `Stock from 2000.parquet`
- `Stock from 2000_edit.parquet` (daily data for multi-month return horizons)
- `A000020.동화약품~A123690.한국화장품_주식_from2000.parquet`

## Calculation of:

```text
stock data analysis.ipynb
 └─ Factor Analysis: PER, PBR, PSR, PCR
 └─ Quality Factor: ROE, GPA, CFO
 └─ Momentum Factor: 3 / 6 / 12 month return windows
 └─ Growth Factor
 └─ 4 Factor Analyis
 └─ Magic Formula (Joel Greenblatt) to set up portfolio
```
