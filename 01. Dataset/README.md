01. Dataset
============

This folder holds the raw and processed data used across the project.

Source
- Primary source: Expedia Flight Prices Dataset on Kaggle: https://www.kaggle.com/datasets/dilwong/flightprices

Contents
- `data/airportsData.csv` — airport metadata used to map IATA codes to coordinates and names.
- `data/flights_economy_1gb.parquet` — a 1 GB sample used for development and faster iteration.
- `data/final_32_columns_no_outliers.parquet` — cleaned dataset used for modelling (32 selected columns, outliers removed).
- Notebooks that operate on these files:
	- `data_cleaning.ipynb` — cleaning and initial sanity checks.
	- `preprocessing.ipynb` — preprocessing pipeline and saved outputs.
	- `sampling.ipynb` — scripts that produce representative samples for experimentation.
	- `first.ipynb`, `second.ipynb` — exploratory & early-stage processing notebooks.

How to load
- Parquet (recommended):

```python
import pandas as pd
df = pd.read_parquet('01. Dataset/data/final_32_columns_no_outliers.parquet')
```

Notes
- The original full dataset is large; use the provided sampled parquet files for local development. Replace or re-create these parquet files from the Kaggle source if you need the original raw CSVs.
