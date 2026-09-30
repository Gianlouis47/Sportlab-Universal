import numpy as np
from sportlab.simulations.monte_carlo import gamma_poisson_counts, line_probabilities

def test_seed_reproducibility():
    a=gamma_poisson_counts(np.random.default_rng(42),4.5,1000)
    b=gamma_poisson_counts(np.random.default_rng(42),4.5,1000)
    assert np.array_equal(a,b)

def test_integer_line_has_push_probability():
    x=np.array([6,7,7,8])
    p=line_probabilities(x,[7.0])["7.0"]
    assert p["over"]==0.25 and p["under"]==0.25 and p["push"]==0.50
