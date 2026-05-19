# Type I and Type II Errors

## The Two Errors

| | H₀ is actually True | H₀ is actually False |
|---|---|---|
| **Reject H₀** | Type I Error (α) ✗ | Correct ✓ |
| **Fail to reject H₀** | Correct ✓ | Type II Error (β) ✗ |

- **Type I** — false alarm. You acted when you shouldn't have.
- **Type II** — missed signal. You didn't act when you should have.

---

## How to Approach These Problems

### Step 1 — Identify H₀ (the default/safe assumption)

H₀ is always the status quo — what you assume is true until proven otherwise.

Ask: *what is the default assumption here?*

| Scenario | H₀ |
|---|---|
| Court | Defendant is innocent |
| Medical test | Patient does not have the disease |
| Spam filter | Email is not spam |
| Factory | Machine is working correctly |

### Step 2 — Map the Two Errors

| Error | Question to ask |
|---|---|
| **Type I** | What happens if you wrongly **reject** H₀? (H₀ was true but you said H₁) |
| **Type II** | What happens if you wrongly **fail to reject** H₀? (H₁ was true but you missed it) |

### Step 3 — Ask Which Error is More Costly

This decides how α should be set:

| If... | Then... |
|---|---|
| Type I is more costly | Set α **low** — be strict, hard to reject H₀ |
| Type II is more costly | Set α **high** — be lenient, easier to reject H₀ |

| Scenario | More Costly Error | Reason |
|---|---|---|
| Court | Type I | Convicting an innocent person is worse than acquitting a guilty one |
| Medical diagnosis | Type II | Missing a disease is worse than a false alarm |
| Spam filter | Type I | Losing a real email is worse than seeing some spam |

---

## Test Naming — Alternate Terms

| Common Name | Alternate Name | H₁ |
|---|---|---|
| Right-tailed | Upper-tailed | μ > μ₀ |
| Left-tailed | Lower-tailed | μ < μ₀ |
| Two-tailed | Two-sided | μ ≠ μ₀ |

Just different textbooks using different names — same thing.

---

## Fail to Reject ≠ H₀ is True

This is the most common mistake in hypothesis testing.

**Example:** H₀: food is good. H₁: food is contaminated.  
If you fail to reject H₀, you cannot say "the food is good."

> Correct conclusion: *"There is not enough evidence to conclude the food is contaminated."*

The food could still be contaminated — your sample just wasn't strong enough to detect it. H₀ is never proved true, it is only ever:
- **Rejected** — enough evidence against it
- **Not rejected** — insufficient evidence against it

Same logic as a court verdict: **"not guilty"** ≠ **"innocent."**

---

## H₀ Framing Depends on Perspective

H₀ is not always the "good" or "safe" state. It is whatever you assume **until evidence proves otherwise.** The burden of proof is always on H₁.

**Example — Goodyear claims tyres last more than 7,500 miles:**

| Who is testing | H₀ | H₁ | Test type |
|---|---|---|---|
| Skeptical buyer / regulator | μ ≤ 7,500 (claim is false) | μ > 7,500 (claim holds) | Right-tailed |
| Goodyear itself | μ > 7,500 (tyres are good) | μ ≤ 7,500 (something went wrong) | Left-tailed |

Same situation, opposite hypotheses — because the two parties have different defaults and different things to prove.

> **Rule:** Whatever you need evidence to establish goes into H₁. H₀ is what you're stuck with if the evidence isn't strong enough.

---

## Trade-off

Reducing α (stricter) → fewer Type I errors → more Type II errors.  
Increasing α (lenient) → fewer Type II errors → more Type I errors.

You cannot reduce both simultaneously without increasing sample size.

---

## Sample Size and Type II Error

Increasing **n** reduces Type II error. Here's why:

```
Larger sample → smaller standard error (SE = σ/√n)
              → more precise estimates
              → real effects are easier to detect
              → POWER goes UP
              → β (Type II error rate) goes DOWN

Power = 1 − β

More n → more power → less Type II error
```

### Intuition with a biased coin

```
True bias: 55% heads (a slight, real effect)

n = 10 flips:
   You might get 5 or 6 heads — looks random
   → fail to reject "coin is fair" → Type II error

n = 10,000 flips:
   The slight bias becomes statistically obvious
   → reject "coin is fair" → no Type II error
```

### Why this matters

Big samples reduce **both** error types simultaneously:

```
For fixed α: increase n → β drops
For fixed β: increase n → α can be reduced
```

That's why well-designed studies aim for **adequate sample size first** — power calculations tell you how much data you need to reliably detect an effect of a given size.

---

## Quick Reference

```
Type I  → α  → P(reject H₀ | H₀ true)   → FALSE POSITIVE
Type II → β  → P(fail to reject | H₀ false) → FALSE NEGATIVE

Power   = 1 − β = ability to detect a true effect

α and β have a trade-off (for fixed n).
n is the lever that reduces BOTH.
```

---

## Common Quiz Questions

**Q: Which is correct?**

```
A) Type I error: a true H₀ is rejected         ✓ (definition)
B) Type II error: a false H₀ is accepted       ✓ (definition)
C) Increasing sample size reduces Type II       ✓ (power increases)
D) All of the above                              ← typically the answer
```

All three are correct definitions / facts. The "trick" of these multi-choice questions is that **all the individual statements are true** — so "All of the above" is right.

> Memory trick: Type I = "one mistake = false alarm". Type II = "two mistakes = missed it".
