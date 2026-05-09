03. Data Preprocessing
======================

Purpose
- Preprocessing notebooks implement cleaning, feature extraction, and dataset transformations that prepare the raw Expedia data for EDA and modelling.

Notebooks
- `preprocessing.ipynb` — end-to-end preprocessing pipeline: parsing dates, filling missing values, basic feature creation, and saving parquet outputs used by later stages.
- `synergy.ipynb` — experiments combining multiple preprocessing strategies and notes on pipeline choices.

Key outputs
- Cleaned parquet files saved to `01. Dataset/data/` (see `final_32_columns_no_outliers.parquet`).

Usage
- Open `preprocessing.ipynb` to follow the pipeline step-by-step. For automated runs, extract the transformation cells and adapt them into a script that reads/writes parquet files.

Notes
- Keep preprocessing reproducible: document any sampling, random seeds, or external lookups used during processing.
