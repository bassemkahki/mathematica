from engine.math_core.primes import generate_primes, generate_ulam_cylinder
import math

def test_generate_primes():
    primes = generate_primes(5)
    assert len(primes) == 5
    assert primes == [2, 3, 5, 7, 11]

def test_generate_ulam_cylinder():
    points = generate_ulam_cylinder(5, radius=10.0)
    assert len(points) == 5
    for p in points:
        assert "x" in p
        assert "y" in p
        assert "z" in p
