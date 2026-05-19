# Derived Metrics

Create **new variables** from existing ones to capture more meaningful business insight.

Raw data rarely tells the full story — derived metrics translate numbers into business-relevant signals.

---

## Types of Derived Metrics

| Type | Description | Example |
|------|-------------|---------|
| **Ratio / Rate** | Divide one measure by another | Strike Rate = Runs / Balls × 100 |
| **Binary flag** | 1/0 from a threshold condition | Century = 1 if Runs ≥ 100 else 0 |
| **Aggregation** | Sum/count over a group | Total centuries per player |
| **Time extraction** | Pull year/month/day from a date | Year from MatchDate |
| **Combination** | Weighted sum of multiple columns | Total score = Maths + Reading + Science |

---

## Binary Flag from Threshold

```python
df['century'] = (df['Runs'] >= 100).astype(int)   # True→1, False→0
df['high_earner'] = (df['Salary'] > 100000).astype(int)
```

---

## Ratio / Rate

```python
df['strike_rate'] = (df['Runs'] / df['Balls']) * 100
df['profit_margin'] = df['Profit'] / df['Revenue']
```

> Always check for division by zero — filter or use `where`:
> ```python
> df['sr'] = df['Runs'].where(df['Balls'] > 0) / df['Balls'] * 100
> ```

---

## Aggregation — groupby + transform/merge

```python
# Count centuries per player
df.groupby('Player')['century'].sum().sort_values(ascending=False)

# Add group-level stat back to original df
df['player_total_centuries'] = df.groupby('Player')['century'].transform('sum')
```

---

## Date/Time Parsing and Extraction

```python
df['MatchDate'] = pd.to_datetime(df['MatchDate'], format='%d-%m-%Y')

# Extract components
df['Year']  = df['MatchDate'].dt.year
df['Month'] = df['MatchDate'].dt.month
df['Day']   = df['MatchDate'].dt.day

# Or all at once using apply
df[['Year','Month','Day']] = df['MatchDate'].apply(
    lambda x: pd.Series([x.year, x.month, x.day])
)
```

---

## Combining Columns

```python
# Sum across specific columns (ignore NaN)
subject_cols = ['Maths..', 'Reading..', 'Science..', 'Social..']
df['total_score'] = df[subject_cols].sum(axis=1)

# Weighted combination
df['score'] = 0.4 * df['Maths'] + 0.3 * df['English'] + 0.3 * df['Science']
```

---

## Splitting a Column into Multiple

```python
# Split "Mar-97" into Month and Year
df[['Month', 'Year']] = df['Period'].str.split('-', expand=True)

# Split on multiple delimiters or fixed positions
df['first_name'] = df['Full Name'].str.split(' ').str[0]
```

---

## Selecting Rows Based on a Derived Condition

```python
# Centuries only
century_df = df[df['century'] == 1].copy()

# Filter by string pattern
pattern = "Tendulkar|Lara|Ponting"
df[df['Player'].str.contains(pattern, case=False, na=False)]
```

---

## Workflow

1. Understand the business question
2. Identify which raw columns are inputs
3. Define the formula / logic
4. Create the column: `df['new_col'] = ...`
5. Validate: check a few rows manually, check for nulls/zeros
6. Use for segmented or bivariate analysis
