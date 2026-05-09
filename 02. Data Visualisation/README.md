02. Data Visualisation
======================

Overview
- Visual analysis and presentation-quality maps/plots for the Expedia pricing project. This folder centralizes visualization code and helper modules used by the notebooks in `04. EDA/` and the final report in `09. Results and Conclusions/`.

Structure
- `Flightmap/` — a small Python module for building interactive flight route maps (see `Flightmap/README.md`).
- Top-level visualizations (notebooks) are in `04. EDA/` and export static images to `00. Plots/`.

Dependencies
- Typical visual stack: `matplotlib`, `seaborn`, `plotly`, `folium`, `geopandas`, and `branca` for maps. Use your package manager to install required libs before running map examples.

Usage
- For interactive map examples, open `02. Data Visualisation/Flightmap/main.py` or run the notebooks in `04. EDA/` that call the Flightmap helpers.

Notes
- Map generation can be memory- and CPU-intensive with the full dataset; use the samples in `01. Dataset/` for development.
