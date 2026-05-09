Flightmap module
=================

Purpose
- Small visualization module to render flight paths and interactive maps used in the EDA and results sections.

Files
- `main.py` — example runner that builds the interactive map and exports views.
- `dataloader.py` — helpers to load airport metadata and flight samples from the dataset.
- `base_map.py` — map base creation (tile layers, projection helpers).
- `layers.py` — functions for drawing routes, animated arcs, and clustered points.
- `views.py` — high-level abstractions to compose map views used in presentations.

How to run
1. Ensure the project's data is available (see `01. Dataset/`).
2. Install visualization dependencies: `pip install pandas folium branca geopandas` (some packages may require system libraries).
3. Run the example:

```bash
python3 Flightmap/main.py
```

Notes
- The module is intended for small samples; rendering the full dataset may be slow or require simplifying geometry.
- Use the dataloader's sampling helpers to create reproducible examples.
