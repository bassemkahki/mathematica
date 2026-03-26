import math

def generate_primes(n: int) -> list[int]:
    """Returns exactly n primes using trial division."""
    if n <= 0:
        return []
    
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes

def generate_ulam_cylinder(n: int, radius: float = 10.0) -> list[dict]:
    """
    Calculates n primes, maps them to (u, v) where u is prime value and v is index integer,
    and projects to 3D cylinder coordinates.
    """
    primes = generate_primes(n)
    points = []
    for v, u in enumerate(primes):
        x = radius * math.cos(u / radius)
        z = radius * math.sin(u / radius)
        y = float(v)
        points.append({"x": x, "y": y, "z": z})
    return points
