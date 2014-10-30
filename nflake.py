from __future__ import division
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon as RegPol
import numpy
from numpy import cos, sin, pi      # Convenience


def scale_factor(n):
    """
    Return the scale factor for subsequent iterations of an n-flake.

    :param n: The number of sides of on the polygon.

    :return: Returns the factor by which each child polygon is reduced - divide parent radius by the
             scale factor to get the child radius.
    """

    return 2*(1+numpy.sum([cos(2*pi*ii/n) for ii in range(1, int(n/4)+1)]))


def subflake_n(n, parent_rxy, phase_offset=False, center_gon=False):
    """
    Return the radius and (x, y) center locations of an n-flake based on the parent polygon,
    assuming the use of regular polygons.

    :param n: The number of sides in the polygon
    :param parent_radius: The radius of the parent polygon
    :param parent_center: The center (x, y) tuple of the parent polygon

    Optional
    :param phase_offset: For polygons with number of sides n where n = 6+4*i, a second n-flake
                         configuration is available.

    :raises: ValueError

    :return: Returns a tuple containing the new radius and a list of (x,y) tuples for each of the
             child polygons.
    """
    if n < 3:
        raise ValueError('Polygons must have at least 3 sides.')

    if phase_offset and numpy.mod(n-6, 4) != 0:
        raise ValueError('Phase offset n-flake only available for polygons where n = 6 + 4*i')

    parent_radius = parent_rxy[0]

    new_radius = parent_radius/(scale_factor(n))
    cr = parent_radius-new_radius
    ocr = cr

    rxys = []
    pcx = parent_rxy[1]
    pcy = parent_rxy[2]

    ph = pi/n if phase_offset else 0
    cr *= cos(ph)

    for ii in range(0, n):
        rxys.append((new_radius, pcx+cr*sin(ii*2*pi/n+ph), pcy+cr*cos(ii*2*pi/n+ph)))

    if center_gon:
        if numpy.mod(n, 2):
            rxys.append((-parent_radius*(1-(1+cos(pi/n))/scale_factor(n))/cos(pi/n),
                     pcx, pcy))
        else:
            rxys.append((ocr-new_radius, pcx, pcy))
    return rxys


def plot_nflake(n, n_iterations, top_rad=1, color='k', ec='k', elw=0.5, alpha=1.0,
                phase_offset=False, center_polygon=False, fig=None):
    """
    Plots an n-flake where n is the number of sides on the polygons which comprise the flake.

    :param n: The number of sides of the polygon
    :param n_iterations: The number of iterations in the flake (caution: the number of shapes
                         rendered is an exponential function of n_iterations)

    :return: Returns the figure on which this is rendered.
    """
    if fig is None:
        fig = plt.figure(figsize=(8, 8), dpi=120, frameon=False)
        ax = fig.add_subplot(111, axis_bgcolor='none', frameon=False, aspect='equal')
    else:
        ax = fig.gca()

    o_rxys = [(top_rad, 0, 0)]

    gon_kwargs = {'color': color, 'lw': elw, 'ec': ec, 'alpha': alpha}
    if n_iterations == 0:
        gons = [RegPol((o_rxys[0][1], o_rxys[0][2]), n, o_rxys[0][0], **gon_kwargs)]
    else:
        gons = []

    for ii in range(0, n_iterations):
        n_rxys = []
        for rxy in o_rxys:
            c_rxys = subflake_n(n, rxy, phase_offset=phase_offset, center_gon=center_polygon)
            for nrxy in c_rxys:
                n_rxys.append(nrxy)

                if ii == n_iterations-1:
                    gons.append(RegPol((nrxy[1], nrxy[2]), n, nrxy[0], **gon_kwargs))

        o_rxys = n_rxys

    for cgon in gons:
        ax.add_patch(cgon)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    
    ax.relim()
    ax.autoscale_view(True, True, True)

    # Getting cut off at the edges for whatever reason, add a view buffer
    view_buff = 0.02
    ylims = ax.get_ylim()
    xlims = ax.get_xlim()

    yrang = abs(ylims[1]-ylims[0])
    xrang = abs(xlims[1]-xlims[0])

    ybuff = view_buff*yrang
    xbuff = view_buff*xrang

    ax.set_ylim([ylims[0]-ybuff, ylims[1]+ybuff])
    ax.set_xlim([xlims[0]-xbuff, xlims[1]+xbuff])

    return fig
