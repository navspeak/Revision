# Bivariate Analysis

Study how **two variables relate** to each other.

---

## Types of Variable Pairs

| Pair | Analysis | Visual |
|------|----------|--------|
| Numeric × Numeric | Correlation (Pearson r) | Scatter plot, pair plot |
| Numeric × Categorical | Compare distributions across groups | Box plot, violin plot |
| Categorical × Categorical | Cross-tabulation, frequency | Heatmap of crosstab |

---

## Numeric × Numeric — Correlation

### Pearson r — three ways

```python
# 1. pandas — single pair
df['col1'].corr(df['col2'])

# 2. numpy — returns 2×2 matrix
import numpy as np
np.corrcoef(df['col1'], df['col2'])[0, 1]

# 3. scipy — returns (r, p-value)
import scipy.stats
scipy.stats.pearsonr(df['col1'], df['col2'])[0]

# Full correlation matrix
df.corr(numeric_only=True)

# Rank what drives a target
df.corr()['Target'].drop('Target').sort_values(ascending=False)
```

### Interpreting r

| \|r\| | Strength |
|-------|---------|
| > 0.7 | Strong |
| 0.3 – 0.7 | Moderate |
| < 0.3 | Weak |
| 0 | No **linear** relationship (could still be non-linear) |

> **Correlation ≠ Causation.** A high r means they move together, not that one causes the other.  
> But causation **does** imply correlation — so low r is a signal that the relationship is weak or absent.

### Visualise

```python
sns.scatterplot(data=df, x='col1', y='col2', alpha=0.5)

sns.pairplot(df)                                          # scatter matrix of all pairs

sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='Reds')
```

### Example — Company Expenditure vs Profit

| Expenditure type | r with Profit | Action |
|-----------------|---------------|--------|
| Marketing | 0.94 (strong) | Keep current strategy |
| Infrastructure | 0.52 (moderate) | Room to optimise |
| Human Resources | −0.04 (none) | Investigate — no return on spend |

### Gold/Silver example — same asset class, low correlation in a specific year

```python
df[["M", "Y"]] = df["Month"].str.split("-", expand=True)
df_2008 = df[df["Y"] == '08']
df_2008[["SilverPrice", "GoldPrice"]].corr()
# Result: r ≈ 0.009 in 2008 — crisis year broke normal correlation
```

---

## Numeric × Categorical

This is segmented analysis — covered in `3SegmentedUnivariate.md`.

```python
sns.boxplot(data=df, x='category', y='numeric')
sns.violinplot(data=df, x='category', y='numeric')
df.groupby('category')['numeric'].describe()
```

---

## Categorical × Categorical — Cross-tabulation

```python
pd.crosstab(df['cat1'], df['cat2'])                    # frequency table
pd.crosstab(df['cat1'], df['cat2'], normalize='index') # row proportions

sns.heatmap(pd.crosstab(df['cat1'], df['cat2']), annot=True, fmt='d')
```

---

## Scatter Plot Tips

```python
sns.scatterplot(
    data=df,
    x='col1', y='col2',
    hue='category',      # colour by a third variable
    alpha=0.5,
    edgecolor='linen'
)

# Add reference lines
plt.axhline(y=threshold, color='red', linestyle='--')
plt.axvline(x=threshold, color='red', linestyle='--')
```
