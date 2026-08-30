# Components of Time Series Data

A time series can be **decomposed into five fundamental components**, each highlighting a specific pattern in the data. Together they explain the different forms of variation within the series and give a clearer structure for interpretation and modelling.

---

## The Five Components

### 1. Level
**Level is the mean value of a time series** — the baseline around which the series fluctuates.

- When comparing two series, the one that sits *higher* on the plot has the higher level.
- *Example:* If Series 1 lies above Series 2, then Series 1 has a higher level.

### 2. Trend
**A trend is a long-term increasing or decreasing pattern** in a time series.

- A series moving steadily upward has an *upward trend*; one moving downward has a *downward trend*.
- A flat series has *almost no trend*.
- *Example:* Series 1 trending upwards vs. Series 2 with virtually no trend.

### 3. Seasonality
**Seasonality is a periodic short-term pattern** (period **less than ~1 year**) in a time series.

- Characterised by a **seasonal period** — the length/duration of one season.
- *Example:* Company A's website traffic fluctuates every **15 days**, while Company B's fluctuates every **30 days**. The seasonal period of the first series is *shorter* than that of the second.

### 4. Cyclicity
**Cyclicity is a periodic long-term pattern** (period **more than ~1 year**), which can be **regular or irregular**.

- *Example (irregular cycle):*
  - March 2015 → October 2017: cycle ≈ **2 years**
  - March 2018 → April 2019: cycle ≈ **1.5 years**
  - The changing cycle length shows an **irregular cyclic period**.

| Aspect | Seasonality | Cyclicity |
|--------|-------------|-----------|
| Period | Short-term (< ~1 year) | Long-term (> ~1 year) |
| Regularity | Fixed / regular | Can be irregular |

### 5. Noise
**Noise refers to the random, patternless fluctuations** in a time series — also called **residuals**. It is what remains after all known components are removed.

Noise is generally expected to be:
- **Additive**
- **Normally distributed**

---

## Why Decompose?

Identifying these broad movements (level, trend, seasonality, cyclicity, noise) gives a **high-level view** of how a series evolves. However, they do **not fully describe how the values themselves behave over time** — i.e., whether the underlying behaviour stays *stable* or *changes* as time progresses.

To capture this, the next concept to study is **stationarity**, which provides a more comprehensive understanding of the variability in a time series' properties.

> **Next up:** Stationarity in time series.
