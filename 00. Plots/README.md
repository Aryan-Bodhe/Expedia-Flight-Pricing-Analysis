00. Plots
=============

This folder stores static figures produced by the project's exploratory data analysis and visualization notebooks. The images are exported so results can be reviewed without re-running heavy notebooks.

Contents
- `totalFare_histplot.png` — raw fare distribution.
- `totalFare_histplot_post_eif.png` — fare distribution after Extended Isolation Forest outlier removal.
- `feature_correlation_heatmap.png` — correlation heatmap used during feature selection.
- `median_fare_daywise.png`, `weekday_vs_weekend_fare.png` — temporal fare comparisons.
- `h1_top_routes.png`, `h1_overall_premium.png`, `h2_airline_strategy.png`, `h3_pricing_curve.png`, `h3_booking_window.png` — hypothesis and business-insight plots.

How these files were generated
- Most plots come from notebooks in `04. EDA/` and `02. Data Visualisation/`.
- To regenerate a specific figure, open the corresponding notebook in `04. EDA/` and run the relevant cell(s); large datasets may require sampling or a PySpark kernel.

Notes
- Images are versioned for presentation; filenames reflect the notebook or analysis section that produced them.
- If you run notebooks that overwrite images, commit the updated images intentionally (they can be large).
