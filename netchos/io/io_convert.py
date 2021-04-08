"""DataFrame, DataArray and NumPy conversions."""
import numpy as np
import pandas as pd
import xarray as xr

def io_to_df(x, xr_pivot=False):
    """Convert an input array to a DataFrame.

    Parameters
    ----------
    x : array_like or DataFrame or DataArray
        The object to convert
    xr_pivot : bool
        When using xarray.DataArray, use True for converting an already pivoted
        table or False for a table with categories in the columns

    Returns
    -------
    x_df : DataFrame
        Converted input to a DataFrame
    """
    if isinstance(x, xr.DataArray):
        if xr_pivot:
            x = x.to_pandas()
        else:
            x = x.to_dataframe('values').reset_index()
    if isinstance(x, np.ndarray):
        x = pd.DataFrame(x)
    assert isinstance(x, pd.DataFrame)

    return x
