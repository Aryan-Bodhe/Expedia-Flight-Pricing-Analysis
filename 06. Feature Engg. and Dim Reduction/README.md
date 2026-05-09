06. Feature Engineering & Dimensionality Reduction
===============================================

Overview
- This folder contains notebooks and experiments focused on creating predictive features and reducing dimensionality for downstream modelling.

Notebooks
- `preprocessing.ipynb` — feature creation steps such as:
	- Temporal features (booking window, day-of-week, cyclical encoding of time fields).
	- Airport and route encodings (target/time-windowed encoding for high-cardinality features).
	- Distance and duration derived features.
	- Outlier handling using Extended Isolation Forests (EIF).
	- Dimensionality reduction experiments (PCA / feature selection) to identify compact, high-signal feature sets.

Usage
- Use these notebooks to produce the `final_32_columns_no_outliers.parquet` dataset in `01. Dataset/data/` which is used by modelling notebooks.

Notes
- When copying transformations into a production pipeline, ensure encoders (target encoding maps, PCA transforms) are fit only on training data and serialised for inference.
