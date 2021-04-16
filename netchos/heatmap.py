import numpy as np
import pandas as pd

from netchos.io import io_to_df, mpl_to_px_inputs
from netchos.utils import categorize


def heatmap(conn, catline_x=None, catline_y=None, catline=None,
            backend='plotly', kw_trace={}, fig=None, **kwargs):
    """Heatmap plot.

    Parameters
    ----------
    conn : array_like or DataFrame or DataArray
        2D Connectivity matrix of shape (n_rows, n_cols). If conn is a
        DataFrame or a DataArray, the indexes and columns are used for the conn
        and y tick labels
    catline_x, catline_y : dict or None
        Dictionary in order to plot categorical lines along the conn and y
        axis. The keys should correspond to the index or column elements and
        the values to the category.
    catline : dict or None
        Additional arguments when plotting the line
        (e.g dict(color='red', lw=2))
    backend : {'mpl', 'plotly'}
        Backend to use for plotting. Use either 'mpl' for using matplotlib or
        'plotly' for interactive figures using Plotly.
    fig : mpl.figure or go.Figure or None
        Figure object. Use either :

            * plt.figure when using matplotlib backend
            * plotly.graph_objects.Figure when using plotly backend

    kwargs : dict or {}
        Additional arguments are sent to :

            * seaborn.heatmap when using matplotlib backend
            * plotly.graph_objects.Heatmap when using plotly backend

    Returns
    -------
    fig : figure
        A matplotlib or plotly figure depending on the backend
    """
    if not isinstance(catline, dict):
        catline = {}
    catline['color'] = catline.get('color', 'white')

    # conn input conversion
    conn = io_to_df(conn, xr_pivot=True)
    index, columns = conn.index, conn.columns

    if backend == 'mpl':  # -------------------------------- Matplotlib backend
        import seaborn as sns
        import matplotlib.pyplot as plt
        if fig is None:
            fig = plt.figure(figsize=(12, 9))
        kwargs['xticklabels'] = kwargs.get('xticklabels', True)
        kwargs['yticklabels'] = kwargs.get('yticklabels', True)
        # main heatmap
        ax = sns.heatmap(conn, **kwargs)
        # categorical lines
        if isinstance(catline_x, dict):
            for k in categorize(columns, catline_x):
                ax.axvline(k, **catline)
        if isinstance(catline_y, dict):
            for k in categorize(index, catline_y):
                ax.axhline(k, **catline)
    elif backend == 'plotly':  # ------------------------------- Plotly backend
        import plotly.graph_objects as go
        if fig is None:
            fig = go.Figure()
        # main heatmap
        kwargs = mpl_to_px_inputs(kwargs, "go.heatmap")
        catline = mpl_to_px_inputs(catline, "line")
        trace = go.Heatmap(z=conn, x=conn.columns, y=conn.index, **kwargs)
        fig.add_trace(trace, **kw_trace)
        fig.update_yaxes(tickmode='linear', autorange='reversed')
        fig.update_xaxes(tickmode='linear')
        fig.update_layout(width=900, height=850)

        # categorical lines
        if isinstance(catline_x, dict):
            for k in categorize(columns, catline_x):
                fig.add_vline(k - .5, line=catline)
        if isinstance(catline_y, dict):
            for k in categorize(index, catline_y):
                fig.add_hline(k - .5, line=catline)

        return fig
