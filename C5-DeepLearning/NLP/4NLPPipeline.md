# The NLP Pipeline — From Raw Text to Deployment

A standardised sequence of stages that turns raw language into actionable insight.

```
Raw Text → Cleaning → Preprocessing → Feature Extraction → Modelling → Evaluation → Deployment
```

Six stages, all modular but interdependent — quality at later stages depends on the earlier ones.

---

## Stage 1 — Data Collection

The first step: **acquire the language data**.

### Sources

```
Structured repositories  → digital libraries, news archives, annotated corpora
Unstructured text        → blogs, social media, transcribed conversations
Speech recordings        → converted via ASR (Automatic Speech Recognition)
```

### Considerations

| Issue | Why it matters |
|-------|----------------|
| Ethical compliance | Privacy, copyright, consent |
| Domain relevance | Medical text needs medical corpora |
| Diversity | Cover dialects, styles, registers |

Garbage in → garbage out. The corpus shapes everything that follows.

---

## Stage 2 — Data Cleaning

Raw text is **noisy**. Cleaning removes anything that won't help the model.

### Common operations

```
1. Remove non-linguistic elements   → HTML tags, URLs, emojis, special chars
2. Standardise format               → lowercasing (when appropriate), spacing
3. Fix encoding                     → UTF-8 issues, multiple spaces, line breaks
4. Spelling correction              → use edit distance / noisy channel
5. Handle missing/corrupt data      → filter or impute
```

Result: clean, consistent text ready for systematic analysis.

---

## Stage 3 — Text Preprocessing

Decompose text into analysable units and reduce variation.

### Key steps

```
1. Tokenisation
   "Natural Language Processing is fascinating."
   → ['Natural', 'Language', 'Processing', 'is', 'fascinating']

2. Stopword Removal
   Remove high-frequency function words ('the', 'is', 'at')
   ⚠ Don't remove sentiment-carrying words like 'not' or 'never'

3. Normalisation
   - Expand contractions ("don't" → "do not")
   - Remove diacritics
   - Convert to lowercase (but careful — "Apple" company vs "apple" fruit)

4. Stemming and Lemmatisation
   Stemming    → truncate to stem ("running" → "run")
   Lemmatisation → linguistic root ("better" → "good")
   Lemmatisation is more accurate; stemming is faster
```

Each step is covered in detail in its own file (`6` through `11`).

---

## Stage 4 — Feature Extraction

Convert preprocessed text into **numerical form** for ML models.

### Traditional methods

```
Bag-of-Words (BoW):
   Document = collection of word counts (order ignored)
   "the cat sat" and "sat cat the" → same representation
   ✓ Simple, interpretable
   ✗ Loses context and word relationships

TF-IDF (Term Frequency × Inverse Document Frequency):
   Weight = how often the word appears here × how rare across the corpus
   ✓ Reduces influence of common words ("the", "is")
   ✓ Highlights distinctive terms
```

### Modern methods

```
Word Embeddings (Word2Vec, GloVe):
   Words → dense vectors in continuous space
   Similar words have similar vectors
   Captures: king - man + woman ≈ queen

Contextual Embeddings (BERT, GPT):
   Same word can have different vectors depending on context
   "bank" in "river bank" vs "bank account" → different embeddings
```

Traditional methods are interpretable; modern embeddings capture meaning better.

---

## Stage 5 — Model Building

Train an algorithm to detect patterns in the numerical features.

### Classical ML approaches

```
Logistic Regression    → sentiment analysis, topic classification
Naive Bayes            → spam detection, document classification
Hidden Markov Models   → sequence tasks (POS tagging, NER)
SVM                    → text classification
```

### Deep learning approaches

```
RNNs / LSTMs           → sequence modelling
CNNs                   → sentence classification
Transformers           → state-of-the-art (BERT, GPT)
```

### Workflow regardless of algorithm

```
1. Feature Selection  → identify most informative features
2. Training           → fit model to corpus
3. Validation         → tune on held-out validation set
4. Testing            → evaluate on unseen data
5. Interpretation     → analyse what the model learned
```

---

## Stage 6 — Evaluation and Deployment

### Evaluation metrics

| Metric | When to use |
|--------|-------------|
| Accuracy | Balanced classification |
| Precision | When false positives are costly (spam filter) |
| Recall | When false negatives are costly (medical text retrieval) |
| F1-score | Balance precision and recall |
| Confusion matrix | Diagnostic — see which classes are confused |
| Perplexity | Language modelling |
| BLEU / ROUGE | Machine translation, summarisation |

### Qualitative evaluation

Beyond numbers — examine actual outputs:
- Error categorisation
- Confusion patterns (which classes get mixed up)
- Lexical / contextual failures (idioms, negations)
- Human evaluation for fluency and coherence

### Overfitting and underfitting

```
Overfitting  → great on training, poor on unseen data
              → fix: regularisation, more data, dropout
Underfitting → too simple, misses real patterns
              → fix: more features, more complex model
```

Use **k-fold cross-validation** to estimate generalisation.

### Deployment

After evaluation passes:

```
Integration   → search engines, chatbots, recommendation systems
Monitoring    → track performance over time (language drifts!)
Feedback      → user interactions for retraining
Scalability   → balance accuracy with latency and cost
```

Language evolves. Slang, new entities, cultural shifts — a model fixed in 2022 will degrade by 2025. **Continuous monitoring is essential**.

---

## Fairness and Interpretability

Modern evaluation goes beyond accuracy:

- Does the model treat demographic groups equally?
- Can decisions be explained (SHAP, LIME)?
- Does training data bias propagate into predictions?

Robust NLP must be transparent, unbiased, and accountable.

---

## Summary

```
1. Data Collection     → get the text
2. Data Cleaning       → strip noise
3. Preprocessing       → tokenise, normalise, lemmatise
4. Feature Extraction  → BoW, TF-IDF, embeddings
5. Model Building      → classical ML or deep learning
6. Evaluation + Deploy → metrics, error analysis, monitoring
```

> The pipeline is the backbone of every NLP project — from sentiment analysis to chatbots to translation engines.
