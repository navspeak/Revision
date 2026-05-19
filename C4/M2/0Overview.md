# M2 — Linear Regression

Linear regression is the entry point to predictive modelling — simple enough to build full intuition, powerful enough for many real-world problems. Concepts learned here (loss functions, coefficients, evaluation metrics) carry directly into every model that follows.

---

## Module Agenda

| # | Topic | Key Ideas |
|---|-------|-----------|
| 1 | Intuition & Setup | What LR does, simple example, the line of best fit |
| 2 | Assumptions | When LR works and when it doesn't |
| 3 | Coefficients | Interpretation, meaning, caution |
| 4 | Model Evaluation | MSE, RMSE, MAE, R², Adjusted R² |
| 5 | Practical Demo | End-to-end: build → interpret → evaluate |

---

## Files

| File | Content |
|------|---------|
| `1LinearRegression.md` | Intuition, OLS, assumptions, coefficients, evaluation metrics |
| `2OLS_gradientDescent.md` | OLS closed-form derivation, gradient descent, learning rate α |
| `3Assumptions.md` | 5 assumptions explained with small dataset — holds vs violated |
| `4MAPE.md` | MAPE explained with example; comparison with RMSE |
| `5Metrics.md` | All metrics in logical order with step-by-step calculations — ME → MAE → SSE → MSE → RMSE → MAPE → SST → SSR → R² |
| `6Coefficients.md` | Interpreting coefficients — sign, magnitude, holding others constant, cautions |
| `7SklearnAPI.md` | sklearn API pattern — fit(), predict(), metrics; same across all models |
| `LinearRegression.ipynb` | Runnable notebook — Advertising dataset, sklearn + statsmodels |
