# Interpreting Coefficients in Logistic Regression

In linear regression, β₁ = "one unit increase in x increases y by β₁."

In logistic regression the output is a probability — the relationship between x and p is non-linear (sigmoid). So we can't interpret β directly the same way. We use **odds** instead.

```
  p = P(y = 1 | X) = σ(z) = 1 / (1 + e⁻ᶻ)
```

---

## Odds

Odds = ratio of probability of event occurring to probability of it not occurring:

```
Odds = p / (1 − p)

p = 0.5  →  Odds = 0.5/0.5 = 1.0   (even chance)
p = 0.7  →  Odds = 0.7/0.3 = 2.33  (2.33x more likely to happen than not)
p = 0.2  →  Odds = 0.2/0.8 = 0.25  (1/4 as likely to happen as not)
```

---

## Log-Odds (Logit)

From the sigmoid function:

```
p = 1 / (1 + e⁻ᶻ)
```

Solving for z:

```
z = log(p / (1 − p))   ← log of the odds = log-odds = logit
```

And z is exactly the linear combination:

```
z = β₀ + β₁x₁ + β₂x₂ + ...
```

So:

```
log(p / (1−p)) = β₀ + β₁x₁ + β₂x₂ + ...
```

The logit function transforms the non-linear relationship between p and x into a **linear** relationship between log-odds and x.

```
p  →  non-linear relationship with x  (sigmoid shape)
log(p/1-p)  →  linear relationship with x  (straight line)
```

---

## Coefficient Interpretation

β₁ represents the **change in log-odds** for a one unit increase in x:

```
log-odds at x:    β₀ + β₁x
log-odds at x+1:  β₀ + β₁(x+1) = β₀ + β₁x + β₁

Difference = β₁   ← change in log-odds per unit increase in x
```

Log-odds are hard to interpret directly. Exponentiate to get the **odds ratio**:

```
Odds Ratio = e^β₁
```

---

## Odds Ratio

The odds ratio tells you the **multiplicative change in odds** for a one unit increase in x:

```
e^β₁ = 1.5  →  odds increase by 50% for each unit increase in x
e^β₁ = 2.0  →  odds double for each unit increase in x
e^β₁ = 0.8  →  odds decrease by 20% for each unit increase in x
e^β₁ = 1.0  →  no effect
```

### Example

```
Model: log(p/1-p) = −3.0 + 0.5 × Age

β₁ = 0.5
Odds Ratio = e^0.5 = 1.65

→ For each additional year of age,
  the odds of the outcome increase by 65%
```

---

## Why Odds Ratio Instead of Raw Coefficient?

- Predictors have different scales — comparing raw β values across features is misleading
- No direct linear relationship between β and the probability output
- Odds ratio gives a scale-independent, interpretable measure of effect size

---

## sklearn

```python
import numpy as np

model.fit(X_train, y_train)

# Raw coefficients (log-odds scale)
print(model.coef_)          # β₁, β₂, ...
print(model.intercept_)     # β₀

# Odds ratios
odds_ratios = np.exp(model.coef_)
print(odds_ratios)
```

---

## Summary

| | Formula | Interpretation |
|-|---------|----------------|
| Odds | p / (1−p) | How much more likely event is vs not |
| Log-odds (logit) | log(p / 1−p) = z | Linear combination — what the model computes |
| Coefficient β | change in log-odds per unit x | Not directly interpretable |
| Odds Ratio | e^β | Multiplicative change in odds per unit x — report this |
