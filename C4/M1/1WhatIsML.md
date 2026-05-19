# What is Machine Learning?

---

## AI vs ML vs Data Science vs Deep Learning

These terms are often used interchangeably — they are not the same.

```
Artificial Intelligence  (broadest — any system that mimics human intelligence)
└── Machine Learning     (systems that learn from data without being explicitly programmed)
    └── Deep Learning    (ML using multi-layer neural networks)

Data Science             (extracts insight from data — uses ML as one of its tools)
```

| Term | Definition | Example |
|------|-----------|---------|
| **AI** | Any technique enabling machines to mimic human behaviour | Chess engine, chatbot |
| **Machine Learning** | Algorithms that improve with experience/data | Spam filter, recommendation system |
| **Deep Learning** | ML with neural networks (many layers) | Image recognition, LLMs |
| **Data Science** | Broader discipline: data collection, EDA, modelling, communication | A/B testing, dashboards, forecasting |

---

## How Machines Learn

Traditional programming: **rules + data → output**  
Machine learning: **data + output → rules (model)**

The model learns patterns from examples and uses them to make predictions on new, unseen data.

---

## Learning Paradigms

### 1. Supervised Learning
- **Data:** Labelled (input → known output)
- **Goal:** Learn a mapping from inputs to outputs
- **Examples:** Spam detection (email → spam/not spam), house price prediction
- **Algorithms:** Linear regression, logistic regression, decision trees

### 2. Unsupervised Learning
- **Data:** Unlabelled (inputs only, no known outputs)
- **Goal:** Find hidden structure or patterns
- **Examples:** Customer segmentation, topic modelling, anomaly detection
- **Algorithms:** K-means clustering, PCA, autoencoders

### 3. Semi-Supervised Learning
- **Data:** Small labelled set + large unlabelled set
- **Goal:** Use the unlabelled data to improve learning
- **Why:** Labelling data is expensive; unlabelled data is abundant
- **Example:** Medical imaging (few annotated scans, many unannotated)

### 4. Reinforcement Learning (RL)
- **Data:** No fixed dataset — agent interacts with an environment
- **Goal:** Learn a policy (sequence of actions) that maximises cumulative reward
- **Mechanism:** Trial and error — good actions are rewarded, bad ones penalised
- **Examples:** AlphaGo, game-playing agents, robotic control

### 5. Self-Supervised Learning
- **Data:** Raw unlabelled data — but labels are **generated from the data itself**
- **Goal:** Learn rich representations without human-annotated labels
- **Mechanism:** Predict part of the input from the rest (e.g. predict next word, masked word)
- **Why it matters:** This underpins LLMs (GPT, Gemini) — trained by predicting the next token in text
- **Example:** "The cat sat on the ___" → model predicts "mat", checks against actual, updates weights

---

## Paradigm Comparison

| Paradigm | Labels needed? | What it learns | Real-world trigger |
|----------|---------------|----------------|-------------------|
| Supervised | Yes (all data) | Input → output mapping | Prediction, classification |
| Unsupervised | No | Hidden structure | Grouping, compression |
| Semi-supervised | Few | Leverages unlabelled bulk | Limited annotation budget |
| Reinforcement | No (uses rewards) | Policy via trial & error | Sequential decisions |
| Self-supervised | No (auto-generated) | General representations | Foundation models, LLMs |

---

## Why Classical ML Still Matters in the LLM Era

LLMs (ChatGPT, Gemini) dominate headlines — but:

- LLMs **are built on** ML principles: gradient descent, loss functions, regularisation, overfitting
- Classical models are **interpretable** — you can explain a decision tree; not so easy for a 70B parameter model
- Classical models are **efficient** — logistic regression runs on a laptop; LLMs need GPUs/TPUs
- Many real-world problems don't need LLMs — tabular data, structured predictions, small datasets
- **Understanding classical ML = understanding what LLMs are doing underneath**

---

## Key Challenges in ML

| Challenge | Description | Example |
|-----------|-------------|---------|
| **Data quality** | Garbage in, garbage out — biased/noisy/incomplete data leads to bad models | Training on historical hiring data that reflects past bias |
| **Overfitting** | Model memorises training data, fails on new data | 100% train accuracy, 60% test accuracy |
| **Blind application** | Using a model without understanding its assumptions | Applying linear regression to non-linear data |
| **Bias & fairness** | Model reflects and amplifies societal biases in training data | Facial recognition worse on darker skin tones |
| **Interpretability** | Complex models (deep learning) are black boxes | Can't explain why a loan was rejected |
| **Ethical responsibility** | Deployed models affect real people | Medical diagnosis, criminal justice, credit scoring |

> ML progress must be matched with care and thoughtfulness — powerful models carry real responsibility.
