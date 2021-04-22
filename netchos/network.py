"""Network plotting layout."""
import pandas as pd
import numpy as np

from netchos.io import io_to_df
from netchos.utils import normalize, extract_df_cols, prepare_to_plot


def network(
    conn, nodes_data=None, nodes_name=None, nodes_x=None, nodes_y=None,
    nodes_z=None, nodes_color=None, nodes_size=None, nodes_size_min=1,
    nodes_size_max=30, nodes_cmap='plasma', edges_min=None, edges_max=None,
    edges_width_min=.5, edges_width_max=8, edges_opacity_min=0.1,
    edges_opacity_max=1., edges_cmap='plasma', cbar=True, cbar_title='Edges',
    directed=False, fig=None, kw_trace={}, kw_cbar={}):
    """Network plotting, either in 2D or 3D.

    Parameters
    ----------
    conn : array_like or DataFrame or DataArray
        2D Connectivity matrix of shape (n_rows, n_cols). If conn is a
        DataFrame or a DataArray, the indexes and columns are used for the conn
        and y tick labels
    nodes_data : pd.DataFrame
        DataFrame that can contains nodes informations (e.g the name of the
        nodes, the x, y and z coordinates, values assign to the nodes etc.)
    nodes_name : list, array_like, str | None
        List of names of the nodes. Alternatively, if `nodes_data` is provided,
        a string referring to a column name can be provided instead
    nodes_x, nodes_y, nodes_z : list, array_like, str | None
        The x, y and potentially z coordinates of each node. Alternatively, if
        `nodes_data` is provided, a string referring to a column name can be
        provided instead
    nodes_color, nodes_size : list, array_like, str | None
        List of values assign to each node in order to modulate respectively
        the color and the size of the nodes. If None, the degree of each node
        is going to be used instead. Alternatively, if `nodes_data` is
        provided, a string referring to a column name can be provided instead
    nodes_size_min, nodes_size_max : float | 1, 30
        Respectively, the minimum and maximum size to use for the markers
    nodes_cmap : str | 'plasma'
        Colormap to use in order to infer the color of each node
    edges_min, edges_max : float | None
        Respectively the minimum and maximum to use for clipping edges values
    edges_width_min, edges_width_max : float | .5, .8
        Respectively the minimum and maximum width to use fot the edges
    edges_opacity_min, edges_opacity_max : float | 0.1, 1.
        Respectively the minimum and maximum opacity for edges
    edges_cmap : str | 'plasma'
        Colormap to use to infer the color of each edge
    cbar : bool | True
        Add a colorbar to the plot.
    cbar_title : str | 'Edges
        Default colorbar title 
    directed : bool | False
        Specify if the graph is undirected (False) or directed (True)
    fig : go.Figure | None
        plotly.graph_objects.Figure object
    kw_trace : dict | {}
        Additional arguments to pass to the
        plotly.graph_objects.Figure.add_trace method

    Returns
    -------
    fig : go.Figure | None
        A plotly.graph_objects.Figure object containing either the 2D network
        or a 3D network if the z coordinate is provided
    """
    import plotly.graph_objects as go

    # -------------------------------------------------------------------------
    #                                  I/O
    # -------------------------------------------------------------------------
    # connectivity matrix conversion
    conn = io_to_df(conn, xr_pivot=True)
    plt_in = '3D' if nodes_z is not None else '2D'

    # get node names and coordinates in case of dataframe
    kw_nodes = dict(nodes_name=nodes_name, nodes_size=nodes_size,
                    nodes_x=nodes_x, nodes_y=nodes_y, nodes_z=nodes_z,
                    nodes_color=nodes_color)
    if isinstance(nodes_data, pd.DataFrame):
        kw_nodes = extract_df_cols(nodes_data, **kw_nodes)

    # get useful variables for plotting
    df_nodes, df_edges = prepare_to_plot(
        conn, nodes_size_min=nodes_size_min, nodes_size_max=nodes_size_max,
        edges_min=edges_min, edges_max=edges_max,
        edges_width_min=edges_width_min, edges_width_max=edges_width_max,
        edges_opacity_min=edges_opacity_min,
        edges_opacity_max=edges_opacity_max, directed=directed,
        edges_cmap=edges_cmap, edges_sorted=True, edges_rm_missing=True,
        **kw_nodes
    )

    # -------------------------------------------------------------------------
    #                              PLOT VARIABLES
    # -------------------------------------------------------------------------
    # build edges lines
    edges_x = np.c_[df_edges['x_s'], df_edges['x_t']]
    edges_y = np.c_[df_edges['y_s'], df_edges['y_t']]
    edges_z = np.c_[df_edges['z_s'], df_edges['z_t']]

    # automatic nodes_size ratio
    sizeref = np.max(df_nodes['size_plt']) / nodes_size_max ** 2

    # prepare hover data
    hovertemplate = (
        "<b>Node :</b> %{text} <br><b>Size :</b> %{customdata[0]:.3f} <br>"
        "<b>Color :</b> %{customdata[1]:.3f}<br>"
        "<b>Degree :</b> %{customdata[2]}")

    # hover custom data
    customdata = np.stack(
        (df_nodes['size'], df_nodes['color'], df_nodes['degree']), axis=-1)

    if fig is None:
        fig = go.Figure()

    # switch between 2D and 3D representations
    Scatter = go.Scatter3d if plt_in == '3D' else go.Scatter

    # -------------------------------------------------------------------------
    #                             NODES PLOT
    # -------------------------------------------------------------------------
    # node plot
    kw_nodes = dict(x=list(df_nodes['x']), y=list(df_nodes['y']))
    if plt_in == '3D':
        kw_nodes['z'] = list(df_nodes['z'])
    node_trace = Scatter(
        mode='markers+text', text=list(df_nodes['name']), name='Nodes',
        textposition="top center", hovertemplate=hovertemplate,
        customdata=customdata, marker=dict(
            showscale=False, colorscale=nodes_cmap, sizemode='area',
            sizeref=sizeref, opacity=1., size=list(df_nodes['size_plt']),
            color=list(df_nodes['color_plt']),
            ), **kw_nodes
    )

    # -------------------------------------------------------------------------
    #                             EDGES PLOT
    # -------------------------------------------------------------------------
    # get dataframe variables
    opacity, width = list(df_edges['opacity']), list(df_edges['width'])
    color = list(df_edges['color'])
    # edges plot
    for k in range(edges_x.shape[0]):
        # switch between 2D / 3D plot
        kw_edges = dict(x=edges_x[k, :], y=edges_y[k, :])
        if plt_in == '3D':
            kw_edges['z'] = edges_z[k, :]
        # single line trace
        _line = Scatter(
            mode='lines', showlegend=False, hoverinfo='none', name='edges',
            opacity=opacity[k], line=dict(width=width[k], color=color[k]),
            **kw_edges
        )
        fig.add_trace(_line, **kw_trace)
    fig.add_trace(node_trace, **kw_trace)

    # -------------------------------------------------------------------------
    #                             COLORBAR
    # -------------------------------------------------------------------------
    # edges colorbar (dirty but working solution...)
    if cbar:
        cbar_trace = go.Scatter(
            x=[0.], y=[0.], mode='markers', hoverinfo='none', showlegend=False,
            marker=dict(size=[0.], color=list(df_edges['values']),
            colorscale=edges_cmap, showscale=True,
            colorbar=dict(title=cbar_title, lenmode='fraction', len=0.75,
                          **kw_cbar))
        )
        fig.add_trace(cbar_trace)
    
    fig.update_xaxes(showgrid=False, visible=False, **kw_trace)
    fig.update_yaxes(showgrid=False, visible=False, **kw_trace)
    if not len(kw_trace):
        fig.update_layout(width=900, height=800)

    return fig
