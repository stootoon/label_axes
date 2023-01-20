import numpy as np
from matplotlib import pyplot as plt
from matplotlib.transforms import TransformedBbox, Bbox

def label_axes(ax_list, labs, dx=0, dy=0, x = None, y = None,
               align_x = [], align_x_fun = np.mean,
               align_y = [], align_y_fun = np.mean,
               *args, **kwargs):
    fig = plt.gcf()
    renderer = fig.canvas.get_renderer()
    trans    = fig.transFigure
    itrans   = trans.inverted()
    h = []
    x_vals = []
    y_vals = []
    for i, (ax, lab) in enumerate(zip(ax_list, labs)):
        bb = ax.get_tightbbox(renderer)
        bb = TransformedBbox(bb, itrans)
        dxi = dx[i] if hasattr(dx, "__len__") else dx
        dyi = dy[i] if hasattr(dy, "__len__") else dy
        xi = bb.x0 + dxi if x is None else x[i]
        yi = bb.y1 + dyi if y is None else y[i]
        x_vals.append(xi)
        y_vals.append(yi)
        h.append(fig.text(xi, yi, lab, *args, transform=trans, **kwargs))

    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    if len(align_x):
        for grp in align_x:
            x_vals[grp] = align_x_fun(x_vals[grp])
            
    if len(align_y):
        for grp in align_y:
            y_vals[grp] = align_y_fun(y_vals[grp])

    for hi, x,y in zip(h, x_vals, y_vals):
        hi.set_position((x,y))
