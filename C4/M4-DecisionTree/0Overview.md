# M4 — Decision Trees

Decision Trees are non-linear, rule-based models. Instead of fitting equations, they **split data into branches** based on feature values — creating a flowchart-like structure that's easy to follow.

Decision Trees are versatile:
- **Classification** (yes/no, pass/fail, disease class)
- **Regression** (predicting continuous outcomes)
- Handle both numerical and categorical features natively
- Don't need feature scaling

They're also the foundation for ensemble methods (Random Forest, Gradient Boosting).

---

## Learning Objectives

By the end of this module you should be able to:

- Understand how decision trees differ from regression models (recursive splits, not equations)
- Apply decision trees to both classification and regression problems
- Describe splitting criteria — **Gini impurity, entropy, information gain**
- Recognise overfitting in deep trees and use **depth, min_samples, and pruning** to control complexity
- Interpret a decision tree by following its structure from root to leaf
- Appreciate the strengths (interpretability, flexibility) and limitations (overfitting, instability) of trees

---

## Module Agenda (planned)

| # | Topic | Key Ideas |
|---|-------|-----------|
| 1 | Introduction to Decision Trees | What they are, why use them, classification vs regression |
| 2 | How Trees Split | Gini impurity, entropy, information gain |
| 3 | Regression Trees | MSE-based splits, predicting numbers |
| 4 | Stopping Criteria | max_depth, min_samples_split, min_samples_leaf |
| 5 | Pruning | Pre-pruning vs post-pruning, cost complexity |
| 6 | Hyperparameter Tuning | GridSearchCV with tree-specific parameters |
| 7 | Visualisation & Interpretation | Plotting trees, reading splits |
| 8 | Ensembles Preview | Bagging, Random Forest intuition |

---

## Files

| File | Content |
|------|---------|
| `1Intro.md` | Why trees, umbrella analogy, trees vs linear models |
| `2Structure.md` | Root / internal / leaf nodes, depth, decision boundaries |
| `3Splitting.md` | Splitting on categorical, numerical, and multiple predictors |
| `4Gini.md` | Gini index for classification splits |
| `5Entropy.md` | Entropy and information gain |
| `6RegressionSplits.md` | Variance reduction for regression trees |
| `7Training.md` | CART algorithm — recursive partitioning |
| `8Predictions.md` | Making predictions (majority vote, probability, mean) |
| `9Overfitting.md` | Why trees overfit, symptoms, bias-variance trade-off |
| `10PrePruning.md` | max_depth, min_samples_*, min_impurity_decrease |
| `11PostPruning.md` | Cost complexity pruning, ccp_alpha |
| `12FeatureImportance.md` | feature_importances_, interpretation, limitations |
| `13StrengthsWeaknesses.md` | Strengths, weaknesses, when to use trees |
| `14Ensembles.md` | Bagging, Random Forest, Boosting — why ensembles beat single trees |
| `DecisionTree.ipynb` | Runnable demo — classification (breast cancer) + regression (diabetes) |

---

## Key Differences from Linear/Logistic Models

| | Linear/Logistic | Decision Tree |
|-|-----------------|---------------|
| Type | Parametric (β coefficients) | Non-parametric (tree structure) |
| Decision boundary | Linear (or sigmoid) | Axis-aligned rectangles |
| Feature scaling | Required | Not needed |
| Handles non-linearity | No (without feature engineering) | Yes, natively |
| Interpretability | Coefficients → odds ratios | Rules → if/then/else |
| Risk | Underfitting | Overfitting (deep trees memorise) |
