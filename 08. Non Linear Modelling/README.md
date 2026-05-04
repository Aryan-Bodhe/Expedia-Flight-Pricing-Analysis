# Expedia Flight Pricing Analysis

A large-scale data science project utilizing **PySpark** and **Ensemble Learning** to decode dynamic pricing strategies in the U.S. aviation market.

## Project Overview
This project analyzes a **31 GB dataset** (approx. 6 million observations) from Expedia to build a predictive framework for airfare. We address the limitations of traditional linear models by implementing non-linear, tree-based regressors that capture the complex, non-linear logic of the airline industry.

---

## Performance Benchmarks
After extensive testing, the **Random Forest Regressor** emerged as the champion model, effectively capturing over 77% of price variance.

| Model | Testing $R^2$ | RMSE | MAE | MAPE |
| :--- | :--- | :--- | :--- | :--- |
| **Random Forest** | **0.7711** | **$82.94** | **$57.53** | **19.73%** |
| **XGBoost** | 0.7439 | $87.73 | $61.65 | 19.98% |
| **CatBoost** | 0.7198 | $91.75 | $67.12 | 23.51% |
| **LightGBM** | 0.7200 | $92.07 | $67.49 | 23.72% |

---

## 🛠️ Technical Methodology

### 1. Handling Big Data
* **Engine:** Utilized **PySpark** for distributed data processing.
* **Sampling Strategy:** Performed `RandomizedSearchCV` on representative 10–20% stratified samples to avoid **Out of Memory (OOM)** errors, followed by full-scale training on the 100% dataset.

### 2. Feature Engineering & Preprocessing
* **Outlier Removal:** Implemented **Extended Isolation Forests (EIF)** to strip contextual noise.
* **Encoding:** Applied **Cyclical Encoding** (Sine/Cosine) for temporal features and **Time-Windowed Target Encoding** for high-cardinality airport data.
* **Statistical Diagnostics:** Confirmed that OLS was unsuitable due to **VIF scores > 1000** and severe heteroscedasticity.

---

## Strategic Business Insights

* **The "Procrastination Penalty":** The model identified a consistent **$31.05** average fare surge for bookings made within 7 days of departure.
* **The Non-Stop Premium:** Hypothesis testing revealed that the "convenience tax" is not universal; it is surgically applied to only **14.4% of routes**, specifically targeting high-yield corporate corridors.
* **Smart Premium Positioning:** Insights suggest carriers can undercut legacy airlines by pricing direct flights between budget base fares and legacy "convenience taxes."

---

