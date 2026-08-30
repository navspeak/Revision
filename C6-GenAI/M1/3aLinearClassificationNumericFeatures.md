# Linear Classification using Numeric Features

The single most important data requirement for an SVM:

```
SVMs need every attribute in NUMERIC form.
Non-numeric attributes must be converted to numbers in data preparation.
```

Why? Because an SVM draws a **line / plane / hyperplane** in feature space, and you
can only place a point in space if each coordinate is a number. See [[2SVMMotivation]].

---

## Worked Setting — Spam vs Ham

Classify emails as **spam (1)** or **ham (0)**. The features are the
**frequency of words** in the email — a very common, and sensible, choice for text.

```
Spam-leaning words : "Hurry", "FREE", "Discount", "money", "credit", "000"
Ham-leaning words  : "meeting", "PPT", "weekly report", "project", "hp", "george"
```

Intuition: spam shouts about offers; office mail talks about work.

---

## How Words Become Numbers — Word Frequency

Each email is turned into a row of numbers. One column per tracked word:

```
word_freq_WORD = 100 ×  (times WORD appears in the email)
                        ─────────────────────────────────
                          total number of words in email
```

So it's a **percentage** (0–100). The `Spam.csv` dataset does exactly this.

### A row of the dataset (conceptually)

```
         free  money  your  meeting  project  hp  ...  capital_run_total  | spam
email 1 [ 0.32  0.00  0.96   0.00     0.00    0.0 ...        278          |  1 ]   ← spam
email 2 [ 0.00  0.00  0.00   1.20     0.80    4.2 ...         45          |  0 ]   ← ham
```

Each email is now a **point in N-dimensional numeric space** — exactly what an SVM needs.

---

## The `Spam.csv` Dataset (spambase)

```
4601 emails  ×  57 features  +  1 label

Feature groups:
  • 48 × word_freq_WORD   → % of words matching WORD          (e.g. free, money, hp)
  • 6  × char_freq_CHAR   → % of chars matching CHAR          (e.g. ! $ ( ; )
  • 1  × capital_run_length_average → avg length of CAPITAL runs
  • 1  × capital_run_length_longest → longest CAPITAL run
  • 1  × capital_run_length_total   → total capital letters
  • 1  × spam              → label: 1 = spam, 0 = ham
```

Notice all 57 features are already **numeric and continuous** — no conversion needed here.
The capital-run features capture SHOUTING (e.g. "FREE!!! ACT NOW") which spam loves.

---

## What If a Feature Is NOT Numeric?

You must encode it before feeding the SVM.

| Non-numeric feature | Convert via |
|---------------------|-------------|
| Category (e.g. country) | **One-hot encoding** → 0/1 columns |
| Ordinal (e.g. low/med/high) | **Label / ordinal encoding** → 0,1,2 |
| Raw text | **Bag-of-words / TF-IDF / word frequency** (as above) |
| Boolean (yes/no) | Map to 1 / 0 |

> This conversion happens in the **data preparation stage**, before training.

---

## One More Detail — Scaling Matters

Because SVM works with **distances**, features on bigger scales dominate.

```
word_freq_free       ∈ [0, ~5]      ← small numbers
capital_run_total    ∈ [1, ~10000]  ← huge numbers  ← would dominate!
```

Standardising (mean 0, std 1) keeps every feature on equal footing.
We'll apply this in practice; remember the principle now.

```
✗ Skip scaling → big-range features hijack the boundary
✓ Standardise  → every feature gets a fair say
```

---

## Summary

```
SVM input rule:  all attributes must be NUMERIC.

Spam example:
  • Features  = word frequencies (% of email made of each word)
  • Label     = spam (1) / ham (0)
  • Each email → a point in numeric feature space

Non-numeric? → encode it (one-hot / ordinal / TF-IDF) in data prep.
Different scales? → standardise, because SVM is distance-based.
```

> **Next:** the **linear boundaries** that separate these numeric points into classes
> — the maximum-margin line. See the companion notebook
> `3a_LinearClassification_SpamFeatures.ipynb`, then [[3bHyperplaneIn2D]] for the
> hyperplane that does the separating.
