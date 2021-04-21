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
    if to_min is None: to_min = np.nanmin(x)  # noqa
    if to_max is None: to_max = np.nanmax(x)  # noqa
    if x.size:
        xm, xh = np.nanmin(x), np.nanmax(x)
        if xm != xh:
            return to_max - (((to_max - to_min) * (xh - x)) / (xh - xm))
        else:
            return x * to_max / xh
    else:
        return x


def norm_range(x, vmin=None, vmax=None, clip_min=0., clip_max=1.):
    if vmin is None: vmin = np.nanmin(x)  # noqa
    if vmax is None: vmax = np.nanmax(x)  # noqa

    return np.clip((x - vmin) / (vmax - vmin), clip_min, clip_max)


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
