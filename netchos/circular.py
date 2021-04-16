"""Circular plotting layout."""
import pandas as pd
import numpy as np

from netchos.io import io_to_df
from netchos.utils import (normalize, extract_df_cols, prepare_to_plot,
                           categorize)


def circular(
    conn, nodes_data=None, categories=None, nodes_name=None, nodes_color=None,
    nodes_size=None, nodes_size_min=1, nodes_size_max=10, nodes_cmap='plasma',
    nodes_text_offset=1., edges_min=None, edges_max=None, edges_width_min=.5,
    edges_width_max=6, edges_opacity_min=0.1, edges_cmap='plasma', cbar=True,
    cbar_title='Edges', directed=False, angle_start=90, angle_range=360,
    fig=None, kw_trace={}):
    """Network plotting within a circular layout.

    Parameters
    ----------
    conn : array_like or DataFrame or DataArray
        2D Connectivity matrix of shape (n_rows, n_cols). If conn is a
        DataFrame or a DataArray, the indexes and columns are used for the conn
        and y tick labels
    nodes_data : pd.DataFrame
        DataFrame that can contains nodes informations (e.g the name of the
        nodes, the x, y and z coordinates, values assign to the nodes etc.)
    categories : dict, str | None
        Nodes categories. If a dict is passed, the keys should corresponds
        to the name of the nodes and the values to the category name.
        Alternatively, if `nodes_data` is provided, a string referring to a
        column name can be provided instead
    nodes_name : list, array_like, str | None
        List of names of the nodes. Alternatively, if `nodes_data` is provided,
        a string referring to a column name can be provided instead
    nodes_color, nodes_size : list, array_like, str | None
        List of values assign to each node in order to modulate respectively
        the color and the size of the nodes. If None, the degree of each node
        is going to be used instead. Alternatively, if `nodes_data` is
        provided, a string referring to a column name can be provided instead
    nodes_size_min, nodes_size_max : float | 1, 30
        Respectively, the minimum and maximum size to use for the markers
    nodes_cmap : str | 'plasma'
        Colormap to use in order to infer the color of each node
    nodes_text_offset : float | 1.
        Floating point indicating the offset to apply to the name of each node
    edges_min, edges_max : float | None
        Respectively the minimum and maximum to use for clipping edges values
    edges_width_min, edges_width_max : float | .5, .8
        Respectively the minimum and maximum width to use fot the edges
    edges_opacity_min : float | 0.1
        Minimum opacity for low strength edges
    edges_cmap : str | 'plasma'
        Colormap to use to infer the color of each edge
    cbar : bool | True
        Add a colorbar to the plot.
    cbar_title : str | 'Edges
        Default colorbar title 
    directed : bool | False
        Specify if the graph is undirected (False) or directed (True)
    angle_start : float | 90
        The angle (in degree) at which to start setting nodes names
    angle_range : float | 360
        Angle range coverered (in degree). For example, if 180 is given, half
        of the circle is going to be displayed
    fig : go.Figure | None
        plotly.graph_objects.Figure object
    kw_trace : dict | {}
        Additional arguments to pass to the
        plotly.graph_objects.Figure.add_trace method

    Returns
    -------
    fig : go.Figure | None
        A plotly.graph_objects.Figure object
    """
    import plotly.graph_objects as go

    # -------------------------------------------------------------------------
    #                                  I/O
    # -------------------------------------------------------------------------
    # connectivity matrix conversion
    conn = io_to_df(conn, xr_pivot=True)

    # get node names and coordinates in case of dataframe
    kw_nodes = dict(nodes_name=nodes_name, nodes_size=nodes_size,
                    nodes_color=nodes_color)
    if isinstance(nodes_data, pd.DataFrame):
        kw_nodes = extract_df_cols(nodes_data, **kw_nodes)

    # get useful variables for plotting
    df_nodes, df_edges = prepare_to_plot(
        conn, nodes_size_min=nodes_size_min, nodes_size_max=nodes_size_max,
        edges_min=edges_min, edges_max=edges_max,
        edges_width_min=edges_width_min, edges_width_max=edges_width_max,
        edges_opacity_min=edges_opacity_min, directed=directed,
        edges_cmap=edges_cmap, edges_sorted=True, edges_rm_missing=True,
        **kw_nodes
    )

    # extract categories when combined with dataframe
    nodes_name = df_nodes['name'].values
    if isinstance(categories, str) and isinstance(nodes_data, pd.DataFrame):
        categories = {k: v for k, v in zip(nodes_name, nodes_data[categories])}
    n_nodes = len(df_nodes)

    # -------------------------------------------------------------------------
    #                               LAYOUT
    # -------------------------------------------------------------------------
    # degree to rad conversion
    angle_start_rad = np.deg2rad(angle_start)
    angle_range_rad = np.deg2rad(angle_range)

    # categories
    if isinstance(categories, dict):
        cuts = np.r_[categorize(nodes_name, categories), len(nodes_name)]
    else:
        cuts = []
    n_cat = len(cuts)

    # compute position in circle
    r = np.full((n_nodes,), 10.)
    angle = np.linspace(0, angle_range_rad, n_nodes + 1 + n_cat)[0:-1]
    delta = (angle[1] - angle[0]) / 2.
    angle = angle + angle_start_rad + delta
    if n_cat:
        angle = np.delete(angle, cuts + np.arange(n_cat))

    # infer x and y positions
    x = np.multiply(r, np.cos(angle))
    y = np.multiply(r, np.sin(angle))

    # node names position
    x_names = np.multiply(r + nodes_text_offset, np.cos(angle))
    y_names = np.multiply(r + nodes_text_offset, np.sin(angle))

    # -------------------------------------------------------------------------
    #                           PLOT VARIABLES
    # -------------------------------------------------------------------------
    if fig is None:
        fig = go.Figure()

    sizeref = np.max(df_nodes['size_plt']) / nodes_size_max ** 2

    # prepare hover data
    hovertemplate = (
        "<b>Node :</b> %{text} <br><b>Size :</b> %{customdata[0]:.3f} <br>"
        "<b>Color :</b> %{customdata[1]:.3f}<br>"
        "<b>Degree :</b> %{customdata[2]}")

    # hover custom data
    customdata = np.stack(
        (df_nodes['size'], df_nodes['color'], df_nodes['degree']), axis=-1)

    # -------------------------------------------------------------------------
    #                              NODES PLOT
    # -------------------------------------------------------------------------
    trace = go.Scatter(
        x=x, y=y, mode='markers', text=list(df_nodes['name']),
        hovertemplate=hovertemplate, customdata=customdata, name='Nodes',
        marker=dict(
            sizemode='area', color=df_nodes['color_plt'], sizeref=sizeref,
            size=df_nodes['size_plt'], colorscale=nodes_cmap, opacity=1.
            ),
    )
    fig.add_trace(trace)

    # -------------------------------------------------------------------------
    #                           NODES NAMES PLOT
    # -------------------------------------------------------------------------
    for k in range(n_nodes):
        off = np.pi if x_names[k] < 0 else 0.
        fig.add_annotation(
            x=x_names[k], y=y_names[k], text=nodes_name[k], showarrow=False,
            textangle=np.rad2deg(off - angle[k])
            )

    # -------------------------------------------------------------------------
    #                             EDGES PLOT
    # -------------------------------------------------------------------------
    width, color = list(df_edges['width']), list(df_edges['color'])
    opacity = list(df_edges['opacity'])
    edges_ref = np.c_[df_edges['s'].values, df_edges['t'].values]
    shapes = []
    for n_p, (k, i) in enumerate(edges_ref):
        # path creation
        _path = dict(type='path', path=f"M {x[k]},{y[k]} Q 0,0 {x[i]},{y[i]}",
                    line_color=color[n_p], line=dict(width=width[n_p]),
                    opacity=opacity[n_p], layer="below")
        # add to the list of all path
        shapes += [_path]
    fig.update_layout(shapes=shapes)

    # -------------------------------------------------------------------------
    #                           COLORBAR PLOT
    # -------------------------------------------------------------------------
    cbar_trace = go.Scatter(
        x=[0.], y=[0.], mode='markers', hoverinfo='none', showlegend=False,
        marker=dict(
            size=[0.], color=list(df_edges['values']), colorscale=edges_cmap,
            showscale=True, colorbar=dict(title=cbar_title, lenmode='fraction',
            len=0.75)
            )
    )
    fig.add_trace(cbar_trace)

    axis = dict(showgrid=False, visible=False, scaleanchor="x", scaleratio=1)
    width = min(angle_range * 500 / 180, 800)
    fig.update_layout(width=width, height=800, xaxis=axis, yaxis=axis)

    return fig
