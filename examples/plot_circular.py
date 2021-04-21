"""
Circular layout
===============

Example illustrtaing the circular layout
"""
import os

import numpy as np
import pandas as pd

from netchos import circular

import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# pio.renderers.default = 'sphinx_gallery'
pio.templates.default = 'plotly_white'


###############################################################################
# Load the data
# -------------
#

ma = pd.read_excel('ma.xlsx')
ufc = pd.read_excel('ufc.xlsx', index_col=0)

###############################################################################
# Default layout
# --------------

title = "Default layout (nodes degree represented by marker size and color)"
fig = circular(
    ufc
)
fig.update_layout(title=title)
fig

###############################################################################
# Passing data to the nodes
# -------------------------

# computes nodes' degree
ma['degree'] = (~np.isnan(ufc.values)).sum(0)
# compute node's strength
ma['strength'] = np.nansum(ufc, axis=0)

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
fig

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


fig = circular(
    ufc, nodes_data=ma, nodes_name='Name', nodes_size='degree',
    nodes_color='strength', categories='Lobe', **kw_circ
)
fig.update_layout(width=600, height=700, title='<b>Control of aesthetics</b>',
                  title_x=0.5, template='plotly_dark')

fig
