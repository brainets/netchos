"""
Network layout
==============

Example illustrating the network layout
"""
import os

import numpy as np
import pandas as pd

from netchos import network

import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pio.templates.default = 'plotly_white'


###############################################################################
# Load the data
# -------------
#

# load the connectivity 2D matrix
ufc = pd.read_excel('ufc.xlsx', index_col=0)
print(ufc)

# load a table that contains informations about the nodes
ma = pd.read_excel('ma.xlsx')
print(ma)

# computes nodes' degree
ma['degree'] = (~np.isnan(ufc.values)).sum(0)
# compute node's strength
ma['strength'] = np.nansum(ufc, axis=0)


###############################################################################
# Default 2D layout
# -----------------

fig = network(
    ufc,                  # 2D connectivity matrix
    nodes_data=ma,        # dataframe with data attached to each node
    nodes_x='xcoord_2D',  # x-coordinate name in nodes_data table
    nodes_y='ycoord_2D'   # y-coordinate name in nodes_data table
)
fig

###############################################################################
# Default 3D layout
# -----------------

fig = network(
    ufc,                  # 2D connectivity matrix
    nodes_data=ma,        # dataframe with data attached to each node
    nodes_x='xcoord_3D',  # x-coordinate name in nodes_data table
    nodes_y='ycoord_3D',  # y-coordinate name in nodes_data table
    nodes_z='zcoord_3D'   # z-coordinate name in nodes_data table
)
fig

###############################################################################
# Control of aesthetics
# ---------------------

fig = network(
    ufc, nodes_data=ma,
    nodes_x='xcoord_2D',      # x-coordinate (column name in ma)
    nodes_y='ycoord_2D',      # y-coordinate (column name in ma)
    nodes_color='degree',     # color of the node given by the degree
    nodes_size='strength',    # marker size proportional to the strentgh
    nodes_size_min=1.,        # minimum size of the nodes
    nodes_size_max=30.,       # maximum size of the nodes
    nodes_cmap='agsunset_r',  # colormap associated to the nodes
    edges_cmap='agsunset_r',  # colormap associated to the edges
    edges_opacity_min=.5,     # weak connections semi-transparents
    edges_opacity_max=1.,     # strong connections opaques
    cbar_title='UFC'
)

title = '<b>Control of aesthetics</b>'
fig.update_layout(template='plotly_dark', title=title, title_x=.5)
fig

###############################################################################
# Network layout in subplots
# --------------------------

fig = make_subplots(rows=1, cols=2, subplot_titles=('Subplot 1', 'Subplot 2'))

# configuring the first subplot
network(
    ufc, nodes_data=ma, nodes_x='xcoord_2D', nodes_y='ycoord_2D',
    nodes_name='Name', nodes_size='degree', nodes_color='degree',
    nodes_cmap='plasma_r', edges_cmap='plasma_r', fig=fig,
    edges_opacity_min=0., edges_opacity_max=1., kw_trace=dict(row=1, col=1),
    kw_cbar=dict(x=0.45)
)

# configuring the second subplot
network(
    ufc, nodes_data=ma, nodes_x='xcoord_2D', nodes_y='ycoord_2D',
    nodes_name='Name', nodes_size='strength', nodes_color='strength',
    nodes_cmap='magma_r', edges_cmap='magma_r', fig=fig,
    edges_opacity_min=.6, edges_opacity_max=.8, kw_trace=dict(row=1, col=2),
    kw_cbar=dict(x=1.)
)

title = "<b>Illustration of adding network layouts to subplots</b>"
fig.update_layout(width=1200, height=600, title=title, title_x=0.5)
fig
