# README: Pricing Strategies using Expedia Flight Data

## Project Overview
This repository contains a comprehensive data science investigation into **dynamic pricing strategies** within the United States aviation market. Using a **31 GB Expedia dataset** (approx. 6 million observations), the project develops a predictive framework to estimate optimal ticket prices by leveraging distributed computing, advanced feature engineering, and non-linear machine learning models.

---

## Authors & Affiliation
*   **Indian Institute of Technology (IIT) Hyderabad**
*   **Team Members:** Aryan Bodhe, Avantika Patil, Gayatri Priya, Kajal Avanthika, Naishadha Voruganti
*   **Date:** May 4, 2026
*   **GitHub Repository:** `Expedia-Flight-Pricing-Analysis`

---

## Key Findings

### 1. The "Non-Stop Premium" Myth
Statistical analysis reveals that the assumption of a universal price hike for direct flights is a myth.
*   **85.6%** of routes show no statistical price difference between direct and indirect flights.
*   **14.4%** of routes (mostly high-traffic corporate corridors) carry a targeted "Convenience Tax" averaging **$33.56**.

### 2. The Procrastination Penalty
Ticket prices follow a non-linear "hockey stick" curve based on the booking window:
*   **The Goldilocks Zone:** Prices are lowest **29–42 days** before departure (average $331.01).
*   **The Penalty:** Booking within **0–7 days** of departure triggers a **$31.05 (9.38%)** price surge.

### 3. Model Performance
Non-linear models significantly outperformed traditional linear regression (OLS) due to severe multicollinearity and heteroscedasticity in flight data.
| Model | Testing $R^{2}$ | Testing RMSE |
| :--- | :--- | :--- |
| **Random Forest (Winner)** | **0.7711** | **$82.94** |
| XGBoost | 0.7439 | $87.73 |
| LightGBM | 0.7200 | $92.07 |
| CatBoost | 0.7198 | $91.75 |
| Elastic Net (Linear) | 0.5464 | $116.72 |


---

## Methodology

### Data Processing
*   **Infrastructure:** Utilized **PySpark** for distributed processing of the 31 GB raw dataset.
*   **Sampling:** Extracted a refined **1 GB economy-class sample** (821,337 rows) for modeling.
*   **Cleaning:** Parsed nested segment strings, converted time to minutes, and handled null values.

### Feature Engineering
*   **Cyclical Encoding:** Transformed flight months into Sine/Cosine components to preserve temporal proximity.
*   **Target Encoding:** Replaced high-cardinality airport codes with time-windowed average fares to capture "hub expensiveness".
*   **Synergy Features:** Created interaction terms like *Demand Pressure* and *Layover Discomfort Cost*.
*   **Outlier Detection:** Used **Extended Isolation Forest (EIF)** to remove the top 2% of contextual pricing anomalies.

---

## Strategic Recommendations
*   **Smart Premium Positioning:** Airlines should undercut legacy carrier premiums on corporate routes while remaining above budget base fares.
*   **Revenue Management:** Implement aggressive price surges in the final 14-day window to capture price-insensitive emergency/corporate travelers.
*   **Hub-and-Spoke Efficiency:** Use connecting flights to consolidate capacity on price-sensitive leisure routes where the model shows passengers require steep discounts.

---

## References
*   **Dataset:** Expedia Flight Prices Dataset via Kaggle.
*   **Tools:** Python (Pandas, PySpark, Scikit-Learn, XGBoost, LightGBM, CatBoost), Flightmap Web App.
