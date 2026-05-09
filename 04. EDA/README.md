04. EDA
=======

This folder contains exploratory data analysis notebooks used to discover patterns, verify assumptions, and create the plots shown in `00. Plots/`.

Notebooks
- `analysis_1.ipynb` — initial descriptive statistics and basic visualizations (distributions, counts).
- `analysis_2.ipynb` — route-level analysis and top-route summaries.
- `analysis_3.ipynb` — airline strategy visualizations and comparative plots.
- `analysis_4.ipynb` — temporal and booking-window analyses (Goldilocks zone, procrastination penalty).
- `isolation_forest.ipynb` — outlier detection using Extended Isolation Forests (EIF) and post-EIF diagnostics.

How to reproduce plots
- Run the relevant notebook cells. For full-dataset EDA, use the sampled parquet in `01. Dataset/` to avoid memory issues, or run with a PySpark kernel if available.

Notes
- Many visual outputs are exported to `00. Plots/` for the report and further analysis.
