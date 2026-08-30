# Descriptive Statistics

Descriptive statistics **summarise** a dataset — they don't infer or predict, they describe what the data looks like.

---

## 1. Measures of Central Tendency

*Where is the data centred?*

| Measure | Formula | Python | When to use |
|---------|---------|--------|-------------|
| **Mean** | Σx / n | `df['col'].mean()` | Symmetric data, no extreme outliers |
| **Median** | Middle value when sorted | `df['col'].median()` | Skewed data or outliers present |
| **Mode** | Most frequent value | `df['col'].mode()[0]` | Categorical data; can be multimodal |

### Mean vs Median — which to use?

- **Symmetric distribution** → mean ≈ median → either works
- **Right-skewed** (long tail on right, e.g. income) → mean > median → use **median**
- **Left-skewed** (long tail on left) → mean < median → use **median**
- Outliers pull the mean but not the median → median is more **robust**

```python
df['damage'].mean()
df['damage'].median()
df['calamity_type'].mode()[0]
```

---

## 2. Measures of Dispersion

*How spread out is the data?*

| Measure | Formula | Python | Note |
|---------|---------|--------|------|
| **Range** | max − min | `df['col'].max() - df['col'].min()` | Simple but sensitive to outliers |
| **MAD** | mean(\|x − x̄\|) | `(df['col'] - df['col'].mean()).abs().mean()` | Mean Absolute Deviation — interpretable, less common |
| **Variance** | Σ(x − x̄)² / (n−1) | `df['col'].var()` | In squared units — hard to interpret directly |
| **Std Dev (SD)** | √Variance | `df['col'].std()` | Same units as data — most used |
| **IQR** | Q3 − Q1 | `df['col'].quantile(0.75) - df['col'].quantile(0.25)` | Robust to outliers |

> Python `.var()` and `.std()` use **n−1** (Bessel's correction) by default — sample statistics.  
> Pass `ddof=0` for population formula.

* Bessel's correction. : When to Use n−1 in the Denominator for Variance
The choice between n and n−1 depends on what your data represents:
* n → when your data is the entire population
* n−1 → when your data is a sample drawn from a larger population

This distinction is called Bessel's correction.

### Why SD over Variance?

Variance is in squared units (e.g. km²). SD is in the same units as the original data, so it's interpretable as a typical distance from the mean.

### SD vs IQR

- SD is affected by outliers (uses all values)
- IQR only looks at the middle 50% → robust to outliers
- Use IQR when data is skewed or has outliers

```python
df['col'].var()
df['col'].std()
df.std().idxmin()                        # column with lowest SD
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1

# MAD
mad = (df['col'] - df['col'].mean()).abs().mean()
```

### Key insight — when means are equal, SD decides

Investment example: three agencies all returned 4% mean.
SD: George&Wallace=9.49, Imperial=7.98, HighRise=5.30 → **HighRise is most stable**, pick it.

---

## 3. Measures of Position — Percentiles & Quartiles

*Where does a value sit relative to others?*

- **Percentile:** P-th percentile = value below which P% of data falls
- **Quartiles:** special percentiles dividing data into 4 equal parts

| Quartile | Percentile | Meaning |
|----------|-----------|---------|
| Q1 | 25th | 25% of data is below this |
| Q2 | 50th | Median — 50% below |
| Q3 | 75th | 75% of data is below this |
| IQR | Q3 − Q1 | Spread of the middle 50% |

```python
df['col'].quantile(0.25)                      # Q1
df['col'].quantile([0.25, 0.5, 0.75])         # multiple at once
df['col'].quantile(0.90)                      # 90th percentile
df.select_dtypes('number').quantile(0.25)     # Q1 for ALL numeric columns at once
df['col'].describe()                          # count, mean, std, min, Q1, Q2, Q3, max
df.describe(include=[object])                 # count, unique, top (mode), freq for categoricals
```

### Box Plot — visual summary of all 5

```
  |----[  Q1 | Q2 | Q3  ]-------|
min   whisker  box  whisker    max
```

- Box = IQR (Q1 to Q3)
- Line inside box = median (Q2)
- Whiskers extend to min/max within 1.5×IQR from box edges
- Points beyond whiskers = **outliers**

```python
import matplotlib.pyplot as plt
df['col'].plot(kind='box')
plt.show()
```

---

## 4. Measures of Association — Correlation

*Do two variables move together?*

**Pearson correlation coefficient r:**

$$r = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i-\bar{x})^2 \cdot \sum(y_i-\bar{y})^2}}$$

| r value | Interpretation |
|---------|---------------|
| +1 | Perfect positive linear relationship |
| 0 | No linear relationship |
| −1 | Perfect negative linear relationship |
| \|r\| > 0.7 | Strong |
| 0.3 < \|r\| < 0.7 | Moderate |
| \|r\| < 0.3 | Weak |

> Correlation measures **linear** association only. r = 0 does not mean no relationship — could be non-linear.

```python
df['col1'].corr(df['col2'])                       # single pair — pandas
np.corrcoef(df['col1'], df['col2'])[0, 1]         # numpy — returns 2×2 matrix, grab [0,1]
scipy.stats.pearsonr(df['col1'], df['col2'])[0]   # scipy — returns (r, p-value), grab [0]
df.corr(numeric_only=True)                        # full correlation matrix — pandas 2.x

# rank what drives a target column
df.corr()['Profits'].drop('Profits').sort_values(ascending=False)

import seaborn as sns
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
sns.pairplot(df)    # scatter matrix of every pair of numeric columns
```

---

## 5. Quick Reference — Python

```python
df.describe()             # count, mean, std, min, Q1, Q2, Q3, max for all numeric cols
df.info()                 # dtypes, non-null counts
df['col'].value_counts()  # frequency of each value (useful for categorical)
df['col'].nunique()       # number of unique values
df['col'].isnull().sum()  # count missing values
```

---

## 6. Visualisations

| Plot | Use | Python |
|------|-----|--------|
| **Histogram** | Distribution shape of a numeric variable | `sns.histplot(data=df, x='col', bins=10)` |
| **Box plot** | 5-number summary + outliers | `sns.boxplot(data=df, x='col')` |
| **Count plot** | Frequency of categories | `sns.countplot(data=df, x='col')` |
| **Scatter plot** | Relationship between two numeric variables | `sns.scatterplot(data=df, x='col1', y='col2')` |
| **Pair plot** | Scatter matrix of all numeric pairs | `sns.pairplot(df)` |
| **Heatmap** | Correlation matrix | `sns.heatmap(df.corr(), annot=True, cmap='Reds')` |

### Overlaying reference lines on a histogram

```python
plt.vlines(x=df['col'].mean(),   ymin=0, ymax=10, colors='blue', label='Mean')
plt.vlines(x=df['col'].median(), ymin=0, ymax=10, colors='red',  label='Median')
plt.vlines(x=df['col'].quantile([0.25, 0.5, 0.75]), ymin=0, ymax=10, colors='red')
plt.legend()
```
