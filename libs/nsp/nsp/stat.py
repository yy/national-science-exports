import numpy as np


def bootstrap_resample(pop, num_samples=None):
    """Resample :num_samples: from :pop:.

    Parameters
    ----------
    pop : array-like
        Population from which we sample.

    num_samples : an integer (optional)
        When not provided, it uses the size of the population.

    Returns
    -------
    array-like
        Bootstrapped ensemble.
    """
    if num_samples is None:
        num_samples = len(pop)
    return pop[np.random.randint(low=0, high=num_samples, size=num_samples)]
