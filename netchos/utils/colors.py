"""Color related functions."""
import numpy as np



def get_colorscale_values(cmap):
    """Get the colors composing a plotly colorscale.

    Parameter
    ---------
    cmap : str
        Name of the Plotly colorscale

    Returns
    -------
    colorscale : array_like
        Colors associated to the colormap
    """
    import plotly

    rev = '_r' if '_r' in cmap.lower() else ''
    cmap = cmap.lower().replace('_r', '')
    colorscales = plotly.colors.named_colorscales()
    assert cmap in colorscales
    ensembles = ['sequential', 'diverging', 'qualitative']
    for e in ensembles:
        cmaps = dir(eval(f'plotly.colors.{e}'))
        cmaps_lower = [c.lower() for c in cmaps]
        if cmap in cmaps_lower:
            cmap_idx = cmaps_lower.index(cmap)
            return eval(f'plotly.colors.{e}.{cmaps[cmap_idx]}{rev}')
    assert ValueError(f"{cmap} is not a predefined colorscale {colorscales}")


def hex_to_rgb(value):
    """Convert a hex-formatted color to rgb, ignoring alpha values."""
    value = value.lstrip("#")
    return [int(value[i:i + 2], 16) for i in range(0, 6, 2)]


def rbg_to_hex(c):
    """Convert an rgb-formatted color to hex, ignoring alpha values."""
    return f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}"


def plotly_map_color(vals, colorscale, vmin=None, vmax=None, return_hex=True):
    """Given a float array vals, interpolate based on a colorscale to obtain
    rgb or hex colors. Inspired by
    `user empet's answer in \
    <community.plotly.com/t/hover-background-color-on-scatter-3d/9185/6>`_."""
    from numbers import Number
    from ast import literal_eval

    if vmin is None: vmin = np.nanmin(vals)  # noqa
    if vmax is None: vmax = np.nanmax(vals)  # noqa

    if vmin >= vmax:
        raise ValueError("`vmin` should be < `vmax`.")

    if isinstance(colorscale, str):
        colorscale = get_colorscale_values(colorscale)

    if (len(colorscale[0]) == 2) and isinstance(colorscale[0][0], Number):
        scale, colors = zip(*colorscale)
    else:
        scale = np.linspace(0, 1, num=len(colorscale))
        colors = colorscale
    scale = np.asarray(scale)

    if colors[0][:3] == "rgb":
        colors = np.asarray([literal_eval(color[3:]) for color in colors],
                            dtype=np.float_)
    elif colors[0][0] == "#":
        colors = np.asarray(list(map(hex_to_rgb, colors)), dtype=np.float_)
    else:
        raise ValueError("This colorscale is not supported.")

    colorscale = np.hstack([scale.reshape(-1, 1), colors])
    colorscale = np.vstack([colorscale, colorscale[0, :]])
    colorscale_diffs = np.diff(colorscale, axis=0)
    colorscale_diff_ratios = colorscale_diffs[:, 1:] / colorscale_diffs[:, [0]]
    colorscale_diff_ratios[-1, :] = np.zeros(3)

    vals_scaled = (vals - vmin) / (vmax - vmin)

    left_bin_indices = np.digitize(vals_scaled, scale) - 1
    left_endpts = colorscale[left_bin_indices]
    vals_scaled -= left_endpts[:, 0]
    diff_ratios = colorscale_diff_ratios[left_bin_indices]

    vals_rgb = (
            left_endpts[:, 1:] + diff_ratios * vals_scaled[:, np.newaxis] + 0.5
    ).astype(np.uint8)

    if return_hex:
        return list(map(rbg_to_hex, vals_rgb))
    return [f"rgb{tuple(v)}" for v in vals_rgb]

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # print(dir(plt.get_cmap('viridis')))
    print(plt.get_cmap('viridis').colors)
    exit()
    import plotly
    colors = plotly_map_color(np.arange(10), 'thermal_r')
    print(colors)