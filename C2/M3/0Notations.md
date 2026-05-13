# Notations

## X ~ Distribution(parameters)

The **~** symbol means "follows" or "is distributed as."  
The **letter before ~** is just a name for the random variable (X, Y, Z, x̄ — anything).  
The **distribution name** tells you the family. The **parameters** in brackets define its shape.

| Notation | Distribution | Parameters |
|---|---|---|
| X ~ N(μ, σ²) | Normal | mean, variance |
| X ~ Poisson(λ) | Poisson | λ = mean = variance |
| X ~ B(n, p) | Binomial | n trials, p probability |
| X ~ U(a, b) | Uniform | min, max |
| X ~ Exp(λ) | Exponential | rate λ |

## N(μ, σ²) — Always Mean, Variance

The Normal distribution always takes **mean first, variance second.**

> x̄ ~ N(8, 0.4²) means "sample means follow a Normal distribution centred at 8, with SE = 0.4."  
> Writing 0.4² instead of 0.16 keeps the SE readable at a glance. You still use 0.4 (not 0.4²) in the Z formula.

## Why CLT Always Gives ~ N(...)

The original population can follow any distribution — Poisson, Uniform, Exponential, Binomial.  
But the CLT says the **sampling distribution of x̄** always converges to Normal as n grows.  
That is why the CLT result is always written as x̄ ~ N(μ, σ²/n), regardless of what the population looked like.
