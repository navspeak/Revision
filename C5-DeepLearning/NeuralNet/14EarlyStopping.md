# Early Stopping

A **practical technique** (not technically regularization, but achieves the same goal) for preventing overfitting during training.

```
Train the model while monitoring VALIDATION loss.
The moment validation loss STARTS RISING → stop training.
Use the weights from the best (lowest validation loss) epoch.
```

Simple, effective, and one of the most widely used tricks in deep learning.

---

## The Problem It Solves

Networks can keep improving on the training set indefinitely. But continuing too long leads to overfitting:

```
Training loss:   keeps going down forever (model memorises noise)
Validation loss: goes down first, then starts RISING

→ Past the rise point, you're overfitting.
→ Even with regularization, this can still happen.
```

You need a way to **detect** this and **stop** at the right moment.

---

## How Early Stopping Works

```
1. Split your data: TRAIN / VALIDATION / TEST
   - Train set:      used to update weights
   - Validation set: used during training to monitor generalisation
   - Test set:       used ONCE at the end for final evaluation

2. After EACH epoch:
   - Compute validation loss (or accuracy)
   - Compare to the best so far
   - If improved: save the weights
   - If got worse for N consecutive epochs: STOP

3. Restore the best weights (lowest validation loss).
```

---

## The Classic Curve

```
Loss
  │\
  │ \                          
  │  \___                      
  │      \___                  Training loss (keeps dropping)
  │          \___              
  │              \________     
  │
  │      _______________
  │   /                  \____
  │  /                        \___    Validation loss
  │ /                              \___
  │/                                    
  └────────────────────────────────── epochs
              ↑
            best epoch
            → stop here (early stopping)
            → past this, model OVERFITS
```

- **Early epochs:** both training and validation loss decrease — model is learning real patterns.
- **Middle epochs:** validation loss flattens.
- **Late epochs:** training loss keeps dropping, but validation loss **starts rising** → overfitting begins.

The **gap** between training and validation loss grows after the best point. That's the signal.

---

## The Three Datasets

```
Training set (70%):
   Used to update weights via backprop + gradient descent.
   The model "learns from" this data.

Validation set (15%):
   Used DURING training to monitor performance on unseen data.
   Used to decide when to stop and for hyperparameter tuning.
   Model never updates weights using this — only EVALUATES on it.

Test set (15%):
   Used ONCE at the very end, after training is complete.
   Gives an honest estimate of how the model performs on unseen data.
   NEVER use the test set during training or tuning.
```

```
   Train  →  Update weights
              ↓
   Validate → Decide when to stop (monitor only, no weight updates)
              ↓
   Test    →  Final evaluation (after training finishes)
```

---

## Patience Parameter

You usually don't stop at the FIRST sign of validation loss going up — validation noise can cause false alarms. Instead:

```
"Patience" = number of epochs to wait before stopping
              after validation loss stops improving.

Patience = 3 means:
   If validation loss hasn't improved for 3 consecutive epochs → stop.
```

### Why Patience?

```
Validation loss is NOISY — small fluctuations happen normally.
A single bad epoch doesn't mean overfitting has begun.
Wait a few epochs to be sure.

Too small patience (e.g. 1)  → stops prematurely on noise
Too large patience (e.g. 50) → wastes compute, may overfit
Typical: 3-10 epochs
```

---

## Restoring the Best Weights

Critical detail: when you stop, **don't use the current weights** — they're the overfit ones.

```
1. Track the BEST validation loss seen so far.
2. Whenever it improves, save a CHECKPOINT of the weights.
3. When you stop (after patience runs out), reload the BEST checkpoint.
4. Use THOSE weights for testing / deployment.
```

Without this step, you'd actually use overfit weights — defeating the purpose.

---

## Worked Example

Suppose we're training with patience=3:

```
Epoch | Train Loss | Val Loss
 1    | 1.500       | 1.400   ← saved as best
 2    | 0.900       | 1.100   ← saved as best
 3    | 0.600       | 0.950   ← saved as best
 4    | 0.400       | 0.900   ← saved as best (BEST!)
 5    | 0.300       | 0.920   ← worse (1)
 6    | 0.220       | 0.940   ← worse (2)
 7    | 0.180       | 0.960   ← worse (3) → STOP
        
Restore weights from epoch 4 (best validation loss).
```

The model saved the best weights at epoch 4. After three worsening epochs, training stops and those weights are restored.

---

## In PyTorch

```python
best_val_loss = float('inf')
patience = 5
counter = 0

for epoch in range(max_epochs):
    # Training phase
    model.train()
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(batch_x), batch_y)
        loss.backward()
        optimizer.step()
    
    # Validation phase
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch_x, batch_y in val_loader:
            val_loss += criterion(model(batch_x), batch_y).item()
    val_loss /= len(val_loader)
    
    # Early stopping check
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), 'best_model.pt')   # save best
    else:
        counter += 1
        if counter >= patience:
            print(f'Stopped at epoch {epoch+1}')
            break

# Restore best weights
model.load_state_dict(torch.load('best_model.pt'))
```

PyTorch Lightning, Keras, and other frameworks have built-in callbacks for this:

```python
# Keras / TF
from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# PyTorch Lightning
from pytorch_lightning.callbacks import EarlyStopping
trainer = Trainer(callbacks=[EarlyStopping(monitor='val_loss', patience=5)])
```

---

## Why Early Stopping Works

```
✓ Implicitly regularises — limits how complex the model can become
✓ Saves compute — no point training beyond the optimum
✓ Selects the best epoch automatically
✓ No new hyperparameters to tune (well, just patience)
✓ Works with any model architecture and any other regularization
```

It's basically free — costs nothing extra besides keeping track of validation loss.

---

## When Not to Use Early Stopping

```
✗ Very small datasets where validation noise is huge
   → patience might trigger spuriously
   → use cross-validation to assess overfitting instead

✗ Online learning / streaming data
   → no fixed dataset to validate against

✗ When using cross-validation already
   → each fold has its own training, harder to share early stopping logic
```

For most standard deep learning workflows, **always use early stopping**.

---

## Once You Stop, You Can't Reverse

> "If you let the model train beyond this point, your model will start to overfit and there is no going back."

This is important:

```
Once the weights have been updated past the best point,
those overfit values are LOCKED IN.

You can't "undo" gradient updates.
You can only:
   1. Reload an earlier checkpoint, OR
   2. Start training from scratch
```

That's why you **save the best model** during training — not just at the end.

---

## Combining with Other Techniques

Early stopping plays well with everything:

```
Early stopping  +  L2 regularization     → both fight overfitting
Early stopping  +  Dropout               → both reduce reliance on noise
Early stopping  +  Data augmentation     → augmentation reduces overfitting risk;
                                            early stopping catches what remains
Early stopping  +  Learning rate schedule → LR decay + early stop = standard combo
```

Modern training pipelines almost always include early stopping by default.

---

## Validation Set Pitfalls

```
✗ Tuning hyperparameters using the TEST set
   → you're now overfitting to the test set indirectly
   → use validation set only for that

✗ Using the same validation set repeatedly with different models
   → "validation set overfitting" — models tuned to do well on this one set
   → fix: use cross-validation, or split data carefully

✗ Validation set too small
   → noisy estimates of true performance
   → patience triggers spuriously
   → fix: larger validation set or use k-fold CV
```

---

## Summary

```
Early stopping = stop training when validation loss starts rising.

How it works:
   1. Monitor validation loss after each epoch
   2. Save weights whenever val loss improves
   3. Stop after `patience` epochs of no improvement
   4. Restore the best weights

Why it works:
   - Implicit regularization (limits training time)
   - Picks the optimal epoch automatically
   - Free (just monitor a metric)
   - Combines with any other technique

When to use:
   - ALMOST ALWAYS in modern deep learning
   - Especially when overfitting risk is real
```

> Early stopping is the simplest, most effective overfitting safeguard. **Always have a validation set**, always **monitor validation loss**, always **save the best model**, and **restore it before testing**.
