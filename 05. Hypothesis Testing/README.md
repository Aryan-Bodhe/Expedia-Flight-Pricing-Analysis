05. Hypothesis Testing
======================

Purpose
- Implement formal statistical tests to validate common pricing hypotheses observed during EDA (for example: the "Direct Flight Premium", booking-window effects, weekday/weekend differences).

Notebooks
- `hypotesting.ipynb` — contains test definitions, sampling strategy, test statistics, and interpretation. Tests include:
	- Direct vs multi-stop price comparisons (paired / unpaired tests as appropriate).
	- Booking-window significance tests (comparing price distributions across windows).
	- Airline strategy comparisons (brand-level price differences).

Notes
- Use the sampled datasets in `01. Dataset/` for quick iteration. For full inference, run tests on larger samples and report effect sizes and confidence intervals alongside p-values.

