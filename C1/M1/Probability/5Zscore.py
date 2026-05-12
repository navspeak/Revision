from scipy.stats import norm

def z_score(x, mu, sigma):
    return (x - mu) / sigma

def p_less_than(z):
    """P(Z <= z)"""
    return norm.cdf(z)

def p_greater_than(z):
    """P(Z > z)"""
    return 1 - norm.cdf(z)

def p_between(z1, z2):
    """P(z1 < Z < z2)"""
    return norm.cdf(z2) - norm.cdf(z1)

def z_from_probability(p):
    """Inverse: find Z such that P(Z <= z) = p"""
    return norm.ppf(p)


if __name__ == "__main__":
    mu, sigma = 170, 10   # e.g. heights: mean=170cm, sd=10cm
    x = 185

    z = z_score(x, mu, sigma)
    print(f"X={x}, μ={mu}, σ={sigma}")
    print(f"Z-score        : {z:.4f}")
    print(f"P(X ≤ {x})     : {p_less_than(z):.4f}")
    print(f"P(X > {x})     : {p_greater_than(z):.4f}")
    print(f"P(160 < X < 185): {p_between(z_score(160, mu, sigma), z):.4f}")
    print()
    print(f"Z for top 5%   : {z_from_probability(0.95):.4f}")
    print(f"Z for 95% CI   : ±{z_from_probability(0.975):.4f}")
