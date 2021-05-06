"""
Heatmap layout
==============

Example illustrating the heatmap layout.
"""
import os

import numpy as np
import pandas as pd

from netchos import heatmap

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

###############################################################################
# Default layout
# --------------

fig = heatmap(
    ufc
)
fig

###############################################################################
# Adding categorical lines
# ------------------------

# # define manual boundaries
vmin, vmax = 0., 0.02

# create the categories (node_name: category_name)
cat = {n: c for n, c in zip(ma['Name'], ma['Lobe'])}

fig = heatmap(
    ufc, catline_x=cat, catline_y=cat, catline=dict(lw=2., color='white'),
    cmap='agsunset_r', vmin=vmin, vmax=vmax
)
fig.update_layout(title='<b>Categorical lines</b>', title_x=.5,
                  template='plotly_dark')
fig

###############################################################################
# Heatmap layout in subplots
# --------------------------

fig = make_subplots(rows=1, cols=2, subplot_titles=('Subplot 1', 'Subplot 2'))

# configuring the first subplot
heatmap(
    ufc, catline_x=cat, catline_y=cat, catline=dict(lw=2., color='red'),
    vmin=vmin, vmax=vmax, cmap='plasma', fig=fig, kw_trace=dict(row=1, col=1)
)

# configuring the second subplot
heatmap(
    ufc, catline_x=cat, catline_y=cat, catline=dict(lw=2., color='orange'),
    vmin=vmin, vmax=vmax, cmap='magma', fig=fig, kw_trace=dict(row=1, col=2)
)
fig.update_layout(width=1200, height=600)
fig
