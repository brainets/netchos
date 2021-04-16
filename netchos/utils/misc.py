"""Miscellaneous functions."""
import numpy as np
import pandas as pd


def normalize(x, to_min=0., to_max=1.):
    """Normalize the array x between to_min and to_max.

    Parameters
    ----------
    x : array_like
        The array to normalize
    to_min : int/float | 0.
        Minimum of returned array

    to_max : int/float | 1.
        Maximum of returned array

    Returns
    -------
    xn : array_like
        The normalized array
    """
    if x.size:
        xm, xh = np.nanmin(x), np.nanmax(x)
        if xm != xh:
            return to_max - (((to_max - to_min) * (xh - x)) / (xh - xm))
        else:
            return x * to_max / xh
    else:
        return x


def extract_df_cols(data, **kwargs):
    """Extract DataFrame columns."""
    assert isinstance(data, pd.DataFrame)
    outs = {}
    for k, v in kwargs.items():
        if isinstance(v, str):
            outs[k] = data[v].values
        else:
            outs[k] = v
    return outs
