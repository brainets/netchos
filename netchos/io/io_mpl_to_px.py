"""Conversion of Matplotlib / Seaborn inputs to plotly."""
import os.path as op
from pkg_resources import resource_filename
import json


def mpl_to_px_inputs(inputs, plt_types=None):
    """Convert typical matplotlib inputs to plotly to simplify API.

    Parameters
    ----------
    inputs : dict
        Dictionary of inputs
    plt_types : string or list or None
        Sub select some plotting types (e.g heatmap, line etc.). If None, all
        types are used

    Returns
    -------
    outputs : dict
        Dictionary of converted inputs
    """
    # load reference table
    file = op.join(op.dirname(__file__), "io_mpl_to_px.json")
    with open(file, 'r') as f:
        table = json.load(f)

    # go through the desired plotting types for conversion
    if plt_types is None:
        plt_types = list(table.keys())
    if isinstance(plt_types, str):
        plt_types = [plt_types]
    ref = {}
    for plt_type in plt_types:
        ref.update(table[plt_type])

    # convert inputs
    outputs = {}
    for k, v in inputs.items():
        if k in ref.keys():
            k = ref[k]
        outputs[k] = v

    return outputs
