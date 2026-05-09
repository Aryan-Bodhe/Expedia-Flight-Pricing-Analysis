07. OLS Model
=============

Overview
- This folder contains the OLS (Ordinary Least Squares) modelling work and diagnostics exploring whether a linear model can explain airfare variations.

Files
- `ols_bp.ipynb` — step-by-step OLS modelling, assumptions checks, VIF (multicollinearity) analysis, heteroscedasticity tests, and residual diagnostics.

Key findings
- The notebooks document why OLS underperforms for this problem (high VIFs, heteroscedastic residuals, non-linear relationships) and motivate the transition to ensemble tree-based models in `08. Non Linear Modelling/`.

Usage
- Open `ols_bp.ipynb` to review model specification, diagnostics, and test results. Use the cleaned dataset from `01. Dataset/` to reproduce the notebooks.
