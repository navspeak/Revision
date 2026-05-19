# Interpretation of Coefficients

One of the most valuable features of linear regression is that its coefficients are **readable**. Each one has a direct, practical meaning — not just a number, but an insight.

---

## The Model

```
ŷ = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

| Symbol | Name | Meaning |
|--------|------|---------|
| β₀ | Intercept | Predicted value of y when ALL features = 0 |
| β₁, β₂ ... | Coefficients | Change in y for a one-unit increase in that feature, **holding all others constant** |

---

## Simple Example — Bakery

```
Time = β₀ + β₁ × Muffins
Time = 10  + 2  × Muffins
```

| Coefficient | Value | Interpretation |
|-------------|-------|----------------|
| β₀ = 10 | Intercept | Fixed setup time — 10 mins even before a single muffin is made |
| β₁ = 2 | Muffins | Each additional muffin adds **2 minutes** to the wait time |

**Predictions:**
```
3 muffins → 10 + 2×3 = 16 mins
7 muffins → 10 + 2×7 = 24 mins
```

The coefficient directly ties a number to meaning: *order one more muffin, wait 2 more minutes.*

---

## Multiple Example — Bakery with Staff

```
Time = β₀ + β₁ × Muffins + β₂ × Staff
Time = 15  + 2  × Muffins + (−3) × Staff
```

| Coefficient | Value | Interpretation |
|-------------|-------|----------------|
| β₀ = 15 | Intercept | Base setup time with no muffins and no staff |
| β₁ = 2 | Muffins | Each extra muffin adds 2 mins, **holding staff constant** |
| β₂ = −3 | Staff | Each extra staff member saves 3 mins, **holding muffins constant** |

**Key phrase: "holding all others constant"**
This means β₁ tells you the effect of Muffins alone — not mixed with any change in Staff.

```
3 muffins, 1 staff → 15 + 2×3 + (−3)×1 = 15 + 6 − 3 = 18 mins
3 muffins, 2 staff → 15 + 2×3 + (−3)×2 = 15 + 6 − 6 = 15 mins

One extra staff member saved 3 mins — exactly what β₂ = −3 says.
```

---

## Real Example — Advertising Dataset

```
Sales = 2.94 + 0.046 × TV + 0.188 × Radio + (−0.001) × Newspaper
```

| Feature | Coefficient | Interpretation |
|---------|-------------|----------------|
| Intercept | 2.94 | Expected sales with zero spend on all channels |
| TV | 0.046 | Each ₹1000 extra on TV → **+0.046 units** sales, holding Radio and Newspaper constant |
| Radio | 0.188 | Each ₹1000 extra on Radio → **+0.188 units** sales, holding others constant |
| Newspaper | −0.001 | Each ₹1000 extra on Newspaper → virtually **no effect** on sales |

**Insight:** Radio gives 4× more return per ₹1000 than TV. Newspaper is essentially useless.

---

## Extracting Coefficients in sklearn

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression().fit(X_train, y_train)

print("Intercept:", model.intercept_)
print("Coefficients:", dict(zip(X.columns, model.coef_)))
```

Output:
```
Intercept: 2.94
Coefficients: {'TV': 0.046, 'Radio': 0.188, 'Newspaper': -0.001}
```

---

## Sign and Magnitude

| Coefficient | What it means |
|-------------|---------------|
| Positive (+) | Feature and y move in the same direction — more x → more y |
| Negative (−) | Feature and y move in opposite directions — more x → less y |
| Large magnitude | Strong influence on y |
| Near zero | Little to no influence on y |

---

## Cautions

**1. Coefficients are not directly comparable unless features are on the same scale.**
TV spend ranges 0–300; Radio ranges 0–50. A TV coefficient of 0.046 vs Radio of 0.188 doesn't mean Radio is 4× more important — the units differ. Scale features first (Min-Max) to compare fairly.

**2. Correlation ≠ causation.**
A positive coefficient means x and y move together — it does not mean x *causes* y. Ice cream sales and drowning rates are both high in summer — neither causes the other.

**3. Multicollinearity distorts coefficients.**
If two features are highly correlated, their individual coefficients become unstable and misleading. Check VIF before trusting individual coefficients.

**4. Intercept is often not meaningful on its own.**
β₀ = predicted y when all features = 0. For most real problems (zero TV spend, zero income, zero area) this value is outside the range of the data and has no practical interpretation.

---

## Summary

```
Each coefficient = effect of that one feature on y,
                   with everything else held constant.

Positive → more x, more y
Negative → more x, less y
Near zero → feature has little influence

This is what makes LR interpretable:
not just a prediction, but an explanation.
```
