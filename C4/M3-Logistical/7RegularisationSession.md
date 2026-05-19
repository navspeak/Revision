# Session: Regularisation and Hyperparameter Tuning

Extending linear and logistic models — controlling complexity and improving generalisation.

---

## What this session covers

1. **Hyperparameters** — what they are, how they differ from model parameters, why they matter
2. **Cross-Validation** — systematic way to evaluate models and select hyperparameters with confidence
3. **Regularisation** — L1 (Lasso) and L2 (Ridge) for linear regression
4. **Logistic Regression Regularisation** — same ideas extended to classification

---

## Why It Matters

| Problem | Solution |
|---------|----------|
| How do I choose model settings (α, λ, C)? | Hyperparameter tuning |
| Is my evaluation reliable on one split? | Cross-validation |
| Model overfits — too sensitive to training data | Regularisation |
| Coefficients explode, model unstable | L2 (Ridge) shrinks them |
| Too many features, want feature selection | L1 (Lasso) zeroes some out |

---

## Learning Outcomes

By the end of this session you will:

- Understand the role of **hyperparameters** in model design
- Use **cross-validation** for reliable model assessment
- Apply **regularisation** to build stable, interpretable, effective models
- Know when to choose **L1 vs L2** based on the problem

---

## Files

| File | Content |
|------|---------|
| `8Hyperparameters.md` | Hyperparameters vs parameters, examples |
| `9CrossValidation.md` | k-fold CV, why one split isn't enough |
| `10Regularisation.md` | L1 (Lasso), L2 (Ridge), λ, geometric intuition |
| `11LogisticRegularisation.md` | Regularisation in Logistic Regression, hyperparameter C |
