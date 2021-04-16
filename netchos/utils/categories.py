"""Utility plotting functions to detect categories."""
import numpy as np

def categorize(x, cat):
    """Find categories bounds in a vector 

    Parameters
    ----------
    x : array_like or list
        Array to convert
    cat : dict
        Dictionary in order to convert values of x

    Returns
    -------
    bounds : array_like
        Bounds where the category change
    """
    val = [cat[k] for k in x]
    _, u_int = np.unique(val, return_inverse=True)
    return np.where(np.diff(u_int) != 0)[0] + 1
