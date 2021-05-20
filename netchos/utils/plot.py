"""Plotting utility function."""
import pandas as pd
import numpy as np

from collections import OrderedDict

from .misc import normalize, norm_range

def prepare_to_plot(
        conn, nodes_name=None, nodes_size=None, nodes_size_min=1,
        nodes_size_max=10, nodes_color=None, nodes_x=None, nodes_y=None,
        nodes_z=None, nodes_text=None, edges_min=None, edges_max=None,
        edges_width_min=.5, edges_width_max=8, edges_opacity_min=.1,
        edges_opacity_max=1., edges_cmap='plasma', edges_sorted=True,
        edges_rm_missing=True, directed=False, backend='plotly'):
    """Function to extract variables that are then used for plotting graph.

    Parameters
    ----------
    conn : pd.DataFrame
        2D connectivity array
    node_names : list | None
        List of node names. If None, the index of the dataframe are used
    nodes_size : list | None
        List of values to use in order to modulate marker's sizes. If None, the
        density of the graph is used in place
    node_size_min, node_size_max : float | 1, 10
        Respectively, the minimum and maximum size to use for the markers
    nodes_color : list | None
        List of values to use in order to modulate marker's color. If None, the
        density of the graph is used in place
    nodes_x, nodes_y, nodes_z : list | None
        List of values to use respectively for the x, y and z coordinates
    edges_min, edges_max : float | None
        Respectively the minimum and maximum to use for clipping edges values
    edges_width_min, edges_width_max : float | .5, .8
        Respectively the minimum and maximum width to use fot the edges
    edges_opacity_min, edges_opacity_max : float | .1, 1.
        Respectively the minimum and maximum opacity to use for the edges
    edges_sorted : bool | True
        Specify whether the edges should be sorted according to their values
    edges_rm_missing : bool | True
        Specify whether missing connections should be removed
    directed : bool | False
        Specify if the graph is undirected (False) or directed (True)

    Returns
    -------
    df_nodes : pd.DataFrame
        Pandas DataFrame containing relevant informations about nodes
    df_edges : pd.DataFrame
        Pandas DataFrame containing relevant informations about edges
    """
    # -------------------------------------------------------------------------
    #                             NODES DATAFRAME
    # -------------------------------------------------------------------------
    n_nodes = conn.shape[0]
    df_nodes = OrderedDict()

    # nodes names
    if nodes_name is None:
        if isinstance(conn, pd.DataFrame):
            nodes_name = [str(k) for k in conn.index]
        else:
            nodes_name = [str(k) for k in range(n_nodes)]
    df_nodes['name'] = nodes_name

    # compute node degree
    if directed:
        raise NotImplementedError("degree of directed graph")
    else:
        df_nodes['degree'] = (~np.isnan(conn)).sum(axis=0).astype(int)

    # nodes marker size (default=degree)
    if nodes_size is None:
        df_nodes['size'] = df_nodes['degree']
    else:
        df_nodes['size'] = nodes_size
    df_nodes['size_plt'] = normalize(
        df_nodes['size'], nodes_size_min, nodes_size_max)

    # nodes marker color (default=degree)
    if nodes_color is None:
        df_nodes['color'] = df_nodes['degree']
    else:
        df_nodes['color'] = nodes_color
    df_nodes['color_plt'] = normalize(df_nodes['color'], 0., 1.)

    # nodes coordinates
    if nodes_x is None:
        nodes_x = np.full((n_nodes,), np.nan)
    if nodes_y is None:
        nodes_y = np.full((n_nodes,), np.nan)
    if nodes_z is None:
        nodes_z = np.full((n_nodes,), np.nan)
    df_nodes['x'], df_nodes['y'], df_nodes['z'] = nodes_x, nodes_y, nodes_z

    # nodes text
    if nodes_text is None:
        nodes_text = {n: n for n in list(df_nodes['name'])}
    df_nodes['text'] = [nodes_text[n] for n in list(df_nodes['name'])]

    # dataframe conversion
    df_nodes = pd.DataFrame(df_nodes)

    # -------------------------------------------------------------------------
    #                             EDGES DATAFRAME
    # -------------------------------------------------------------------------
    df_edges = OrderedDict()

    # get triangle indices
    if directed:
        raise NotImplementedError("Not implemented for directed graph")
    else:
        tri_s, tri_t = np.triu_indices_from(conn, k=1)

    # if required, drop edges with nan values
    if edges_rm_missing:
        _is_nan = ~np.isnan(np.array(conn)[tri_s, tri_t])
        tri_s, tri_t = tri_s[_is_nan], tri_t[_is_nan]
    df_edges['s'], df_edges['t'] = tri_s, tri_t

    # edges names
    sep = '->' if directed else '-'
    s_names, t_names = df_nodes['name'][tri_s], df_nodes['name'][tri_t]
    df_edges['names'] = [f"{s}{sep}{t}" for s, t in zip(s_names, t_names)]

    # edges values
    edges_val = np.array(conn)[tri_s, tri_t]
    df_edges['values'] = edges_val
    df_edges['colorbar'] = normalize(
        edges_val, to_min=edges_min, to_max=edges_max)

    # plotting edges values
    values = norm_range(edges_val, vmin=edges_min, vmax=edges_max)
    df_edges['values_plt'] = values
    df_edges['order'] = np.argsort(values)

    # plotting edges width
    df_edges['width'] = (values * (edges_width_max - edges_width_min)) + \
        edges_width_min

    # plotting edge opacity
    df_edges['opacity'] = (values * (edges_opacity_max - \
        edges_opacity_min)) + edges_opacity_min

    # plotting color
    if backend == 'mpl':
        from matplotlib.colors import to_hex
        import matplotlib.pyplot as plt

        cmap = plt.get_cmap(edges_cmap)
        df_edges['color'] = [to_hex(cmap(k)) for k in df_edges['values_plt']]
    elif backend == 'plotly':
        from netchos.utils.colors import plotly_map_color

        df_edges['color'] = plotly_map_color(
            df_edges['values'], edges_cmap, vmin=edges_min, vmax=edges_max)

    # edges coordinates
    df_edges['x_s'], df_edges['x_t'] = nodes_x[tri_s], nodes_x[tri_t]
    df_edges['y_s'], df_edges['y_t'] = nodes_y[tri_s], nodes_y[tri_t]
    df_edges['z_s'], df_edges['z_t'] = nodes_z[tri_s], nodes_z[tri_t]

    # dataframe conversion
    df_edges = pd.DataFrame(df_edges)


    if edges_sorted:
        df_edges = df_edges.loc[
            df_edges['order'].values].reset_index(drop=True)

    return df_nodes, df_edges
