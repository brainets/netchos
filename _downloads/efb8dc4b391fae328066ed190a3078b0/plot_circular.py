"""
Circular layout
===============

Example illustrating the circular layout
"""
import os

import numpy as np
import pandas as pd

from netchos import circular

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
# Default layout
# --------------

title = "Default layout (nodes degree represented by marker size and color)"
fig = circular(
    ufc
)
fig.update_layout(title=title)
pio.show(fig)

###############################################################################
# Passing data to the nodes
# -------------------------

"""
Here, we use the `nodes_data` input to provide a pandas DataFrame containing
nodes informations, namely :
- The name of the nodes ('Name')
- The number of connections per node ('degree')
- The connectivity strength ('strength')
- Additional categorization (each node is a brain region that belong to a lobe)
"""
fig = circular(
    ufc, nodes_data=ma, nodes_name='Name', nodes_size='degree',
    nodes_color='strength', categories='Lobe'
)
pio.show(fig)

###############################################################################
# Control of aesthetics
# ---------------------

kw_circ = dict()

# nodes settings
kw_circ['nodes_size_min'] = 0.2
kw_circ['nodes_size_max'] = 10
kw_circ['nodes_cmap'] = 'plasma'    # colormap for the nodes

# edges settings
kw_circ['edges_width_min'] = .5
kw_circ['edges_width_max'] = 9.
kw_circ['edges_opacity_min'] = 0.2  # opacity for weakest connections
kw_circ['edges_opacity_max'] = 1.   # opacity for strongest connections
kw_circ['edges_cmap'] = 'agsunset'  # colormap for the edges

# layout settings
kw_circ['angle_start'] = 90         # start circle at 90°
kw_circ['angle_range'] = 180        # use only half of the circle
kw_circ['cbar_title'] = 'Significant links (p<0.05)'

# sphinx_gallery_thumbnail_number = 3
fig = circular(
    ufc, nodes_data=ma, nodes_name='Name', nodes_size='degree',
    nodes_color='strength', categories='Lobe', **kw_circ
)
fig.update_layout(width=600, height=700, title='<b>Control of aesthetics</b>',
                  title_x=0.5, template='plotly_dark')
pio.show(fig)

###############################################################################
# Circular layout in subplots
# ---------------------------

fig = make_subplots(rows=1, cols=2, subplot_titles=('Subplot 1', 'Subplot 2'))

# configuring the first subplot
circular(
    ufc, nodes_data=ma, nodes_name='Name', nodes_size='degree',
    nodes_color='degree', categories='Lobe', nodes_cmap='plasma_r',
    edges_cmap='plasma_r', angle_range=180, fig=fig,
    kw_trace=dict(row=1, col=1), kw_cbar=dict(x=0.4)
)

# configuring the second subplot
circular(
    ufc, nodes_data=ma, nodes_name='Name', nodes_size='strength',
    nodes_color='strength', categories='Lobe', nodes_cmap='magma_r',
    edges_cmap='magma_r', angle_range=180, fig=fig,
    kw_trace=dict(row=1, col=2), kw_cbar=dict(x=0.95)
)

title = "<b>Illustration of adding circular layouts to subplots</b>"
fig.update_layout(width=1000, height=800, title=title, title_x=0.5)
pio.show(fig)