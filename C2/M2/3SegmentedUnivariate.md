# Segmented Univariate Analysis

Compare the distribution of a **numeric variable** across different **subgroups** (categories).

Same as univariate, but done separately for each segment — reveals patterns hidden in overall summaries.

---

## The Core Tool — groupby + describe

```python
df.groupby('category_col')['numeric_col'].describe()
```

Returns count, mean, std, min, Q1, Q2, Q3, max **for each category**.

### Examples from NAS education dataset

```python
# How does TV watching relate to science scores?
df.groupby('Watch.TV')['Science..'].describe()

# Does father's education affect maths scores?
df.groupby('Father.edu')['Maths..'].describe()

# Mother's education vs reading scores
df.groupby('Mother.edu')['Reading..'].describe()
# Result: Degree & above → mean 70 vs Illiterate → mean 49
```

### Other aggregations

```python
df.groupby('cat')['num'].mean()     # just the mean per group
df.groupby('cat')['num'].median()
df.groupby('cat')['num'].agg(['mean', 'std', 'count'])
```

---

## Visualisation — Grouped Plots

### Box plot by category (best for segmented analysis)

```python
sns.boxplot(data=df, x='category_col', y='numeric_col')
```

Shows median, IQR, outliers for each group side by side — easy to compare spread and centre.

### Histogram per group

```python
# overlapping histograms
sns.histplot(data=df, x='numeric_col', hue='category_col', bins=10)
```

### Violin plot — box plot + density shape

```python
sns.violinplot(data=df, x='category_col', y='numeric_col')
```

Wider sections = more data there; shows full distribution shape per group.

---

## What to Look For

| Pattern | Interpretation |
|---------|---------------|
| Means differ significantly across groups | The category has an effect on the numeric variable |
| Medians differ but means don't | Skewed distributions per group — look at median |
| One group has much wider IQR | More variability in that segment |
| Mean increases monotonically across ordered categories | Likely a real relationship (e.g. higher education → higher scores) |

---

## Subsetting for Comparison

```python
# Filter to a specific segment then analyse
segment = df[df['category_col'] == 'value']
segment['numeric_col'].describe()
```

---

## Example — Interview Candidate Tiering with Q1/Q3

```python
# Get Q1 and Q3 for all numeric subjects at once
q1 = df.select_dtypes('number').quantile(0.25)
q3 = df.select_dtypes('number').quantile(0.75)

# Direct to final: above Q3 in ALL subjects
final  = df[(df[subjects] >= q3).all(axis=1)]

# Second stage: between Q1 and Q3 in ALL subjects
second = df[(df[subjects] >= q1).all(axis=1) & (df[subjects] < q3).all(axis=1)]

# Reject: below Q1 in ANY subject
reject = df[(df[subjects] < q1).any(axis=1)]
```
