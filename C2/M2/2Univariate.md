# Univariate Analysis

Examine **one variable at a time** — its distribution, shape, central tendency, spread, and outliers.

---

## Numerical vs Categorical

| Variable type | Question | Tools |
|---------------|----------|-------|
| **Numerical** | How is it distributed? Any outliers? | histogram, box plot, describe() |
| **Categorical** | Which category dominates? How many unique values? | count plot, value_counts() |

---

## Numerical Variables

### Step 1 — Summary stats

```python
df['col'].describe()       # count, mean, std, min, Q1, Q2, Q3, max
df['col'].skew()           # positive = right-skewed, negative = left-skewed
```

### Step 2 — Visualise distribution

```python
sns.histplot(data=df, x='col', bins=10)
sns.boxplot(data=df, x='col')
```

### Step 3 — Overlay mean/median to check skew

```python
plt.vlines(x=df['col'].mean(),   ymin=0, ymax=10, colors='blue', label='Mean')
plt.vlines(x=df['col'].median(), ymin=0, ymax=10, colors='red',  label='Median')
plt.legend()
```

- mean >> median → right-skewed (outliers on the high end)
- mean << median → left-skewed
- mean ≈ median → roughly symmetric

### Outlier detection — IQR method

```python
Q1  = df['col'].quantile(0.25)
Q3  = df['col'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[(df['col'] < lower) | (df['col'] > upper)]
```

Box plot whiskers extend to ±1.5×IQR — points beyond are plotted as individual dots = outliers.

---

## Categorical Variables

### Summary

```python
df['col'].value_counts()           # frequency of each category, sorted descending
df['col'].value_counts(normalize=True)  # as proportions
df['col'].nunique()                # number of distinct categories
df.describe(include=[object])      # count, unique, top (mode), freq
```

### Visualise

```python
sns.countplot(data=df, x='col')
```

---

## Handling Messy Data Before Univariate

Real datasets often have dirty values in numeric columns (e.g. Tendulkar ODI: `'DNB'`, `'82*'`).

```python
# Check what non-numeric values exist
df[~df['col'].astype(str).str.match(r'^\d+$')]['col'].unique()

# Convert — coerce non-numeric to NaN, then fill
df['col'] = pd.to_numeric(df['col'], errors='coerce').fillna(0).astype(int)
```

---

## Side-by-Side Subplots for Multiple Variables

```python
fig, axes = plt.subplots(nrows, ncols, figsize=(12, 6))

plt.subplot(3, 2, 1)
sns.histplot(data=df, x='col1', ...)

plt.subplot(3, 2, 2)
sns.boxplot(data=df, x='col1', ...)

plt.tight_layout()
```

---

## Interpreting Results

| Observation | What it means |
|-------------|--------------|
| mean >> median | Right-skewed; outliers on high end pulling mean up |
| Wide IQR | High variability in middle 50% |
| Many outlier dots on box plot | Consider IQR-based removal or investigation |
| One category >> others in count plot | Data is imbalanced — may need stratified sampling |
