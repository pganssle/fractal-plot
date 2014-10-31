from __future__ import division
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon as RegPol
import numpy as npy
from numpy import cos, sin, pi      # Convenience


def scale_factor(n, edge_center=False):
    """
    Return the scale factor for subsequent iterations of an n-flake.

    :param n: The number of sides of on the polygon.

    Optional:
    :param edge_center: Whether the scale factor is being calculated for a vertex-centered flake
                         (edge_center=False, default) or an edge-centered flake.

    :return: Returns the factor by which each child polygon is reduced - divide parent radius by the
             scale factor to get the child radius.
    """

    if edge_center:
        return 3+(2/cos(pi/n))*npy.sum([cos((2*ii+1)*pi/n) for ii in range(1, int((n-2)/4)+1)])
    else:
        return 2*(1+npy.sum([cos(2*pi*ii/n) for ii in range(1, int(n/4)+1)]))


def subflake_n(n, parent_rxy, edge_center=False, center_gon=False):
    """
    Return the radius and (x, y) center locations of an n-flake based on the parent polygon,
    assuming the use of regular polygons.

    :param n: The number of sides in the polygon
    :param parent_radius: The radius of the parent polygon
    :param parent_center: The center (x, y) tuple of the parent polygon

    Optional
    :param edge_center: If edge_center is true (default False), each child polygon will have its
                         edge centered on an edge of the parent polygon. For polygons where
                         n = 6+4*k, this results in child polygons which share an edge rather than
                         a vertex, and as such this can be iterated without introducing gaps. For
                         polygons with even numbers of sides, each face of the center polygon (if
                         present) will be collinear with the face of one of the edge/child polygons,
                         and so a continuous shape will result only when center polygons are
                         present. For odd-numbered polygons, continuous shapes are produced only for
                         iterations 0, 1 and 2.
    :param center_gon: If true, a polygon will be inscribed at the center of the shape, sharing
                       either an edge, a vertex or both with each of the other child polygons.
                       For polygons of size 3, 5 and 6, the center polygon is the same size as all
                       the other child polygons. For all other sizes, the center polygon will be a
                       different size.

    :raises: ValueError

    :return: Returns a tuple containing the new radius and a list of (x,y) tuples for each of the
             child polygons.
    """
    if n < 3:
        raise ValueError('Polygons must have at least 3 sides.')

    parent_radius = parent_rxy[0]

    # The radius of the child polygons is calculated from the scale factor
    new_radius = parent_radius/(scale_factor(n, edge_center=edge_center))

    # The child polgyons are centered on the vertexes of a polygon with radius cr
    cr = parent_radius-new_radius
    ocr = cr                            # cr may be modified, store its original value here

    # Initialize output list and break out parent coordinates
    rxys = []
    pcx = parent_rxy[1]
    pcy = parent_rxy[2]

    # If edge_center is True, the polygons will be centered on the edges not the vertices
    ph = pi/n if edge_center else 0
    cr *= cos(ph)

    # Calculate the x,y values of the centers.
    for ii in range(0, n):
        rxys.append((new_radius, pcx+cr*sin(ii*2*pi/n+ph), pcy+cr*cos(ii*2*pi/n+ph)))

    # The center polygon's size depends on whether or not the shape is even or odd and on the
    # flake's edge_center parameter (e.g. configuration).
    if center_gon:
        if npy.mod(n, 2):
            if not edge_center:
                rxys.append((-parent_radius*(1-(1+cos(pi/n))/scale_factor(n))/cos(pi/n),
                            pcx, pcy))
            else:
                rxys.append((-(parent_radius*cos(pi/n)-new_radius*(1+cos(pi/n))), pcx, pcy))
        else:
            rxys.append((-(ocr-new_radius), pcx, pcy))
    return rxys


def plot_nflake(n, n_iterations, top_rad=1, xy=(0, 0), edge_center=False, center_polygon=False,
                color='none', ec='k', elw=0.5, alpha=1.0,
                center_color=None, center_ec=None, center_elw=None, center_alpha=None,
                fig=None, fig_dpi=150, fig_size=(8, 8), 
                view_buff=0.001, view_buff_x=None, view_buff_y=None,
                only_centermost_colored=False):
    """
    Plots an n-flake where n is the number of sides on the polygons which comprise the flake.

    :param n: The number of sides of the polygon
    :param n_iterations: The number of iterations in the flake (caution: the number of shapes
                         rendered is an exponential function of n_iterations)
    
    Optional:
    :param top_rad: The radius of the circle in which the top-level polygon is inscribed (default 1)
    :param xy: A tuple containing the (x, y) coordinates of the center of the circle into which the
               top-level polygon is inscribed. (default: 0,0)
    :param edge_center: If True, this will generate an edge-centered n-flake. In edge-centered
                        n-flakes, each child polygon has a single edge collinear with a single edge
                        of the parent polygon. Without a center polygon, this only recursively 
                        produces continuous shapes for polygons with number of sides n = 4*j + 6 
                        where j is 0 or any positive integer. With a center polygon, this produces 
                        a continuous shape for all even-sided polygons. Default is False.
    :param center_polygon: Whether to generate a central polygon touching all the child polygons 
                           or not. For most values of n, the central polygon will be scaled
                           differently than the edge polygons. Default is False. 
    :param color: The face color of the polygon (default: 'none')
    :param ec: The edge color of the polygon (default: 'k')
    :param elw: The edge line width (default: 0.5)
    :param alpha: The transparency of the polygons (default: 1)
    :param center_color: For n-flakes with a central polygon, specify the center polygon's face
                         color. If None or not specified, this takes its value from `color`
    :param center_ec: For n-flakes with a central polygon, specify the center polygon's edge
                      color. If None or not specified, this takes its value from `ec`
    :param center_elw: For n-flakes with a central polygon, specify the center polygon's edge line
                       width. If None or not specified, this takes its value from `elw`
    :param center_alpha: For n-flakes with a central polygon, specify the center polygon's alpha
                         transparency. If none or not specified, this takes its value from `alpha`
    :param fig: A figure instance with an existing axis. If None is specified, a new figure will be
                generated. Default is None.
    :param fig_dpi: If fig is None, the new figure generated will have this resolution, in dpi.
                    Default is 150.
    :param fig_size: A tuple specifying the size of the new figure as (width, height). 
                     Default is (8, 8)
    :param view_buff: The amount of "buffer" to add to each side of the axis to prevent clipping.
                      Default is 0.001
    :param view_buff_x: The amount of "buffer" to use along the x-axis. If None or not specified,
                        this value is taken from the `view_buff` parameter.
    :param view_buff_y: The amount of "buffer" to use along the y-axis. If None or not specified,
                        this value is taken from the `view_buff` parameter.
    :param only_centermost_colored: Normally the "central" polygons have an inverted color scheme
                                    to the parent polygons if `center_color` and other parameters
                                    are specified. If this parameter is set True, for even-numbered
                                    polygons, the main color scheme is used for all but the center
                                    polygons at the smallest level. This only works for even 
                                    polygons due to implementation details, and will be fixed later.
                                    For now it is ignored on odd polygons. Default is False.

    :raises: ValueError

    :return: Returns the figure on which this is rendered.
    """
    # Create a figure if one is not provided.
    if fig is None:
        fig = plt.figure(figsize=fig_size, dpi=fig_dpi, frameon=False)
        ax = fig.add_subplot(111, axis_bgcolor='none', frameon=False, aspect='equal')
    else:
        ax = fig.gca()

    # If not specified, the center polygons use the parameters of the edge polygons
    if center_color is None:
        center_color = color

    if center_ec is None:
        center_ec = ec

    if center_elw is None:
        center_elw = elw

    if center_alpha is None:
        center_alpha = alpha

    if view_buff_x is None:
        view_buff_x = view_buff

    if view_buff_y is None:
        view_buff_y = view_buff
    
    o_rxys = [(top_rad, xy[0], xy[1])]

    # Plot parameters for each polygon
    gon_kwargs = {'color': color, 'lw': elw, 'ec': ec, 'alpha': alpha}
    cgon_kwargs = {'color': center_color, 'lw': center_elw, 'ec': center_ec, 'alpha': center_alpha}

    # For zero-iterations, we're just plotting a regular polygon
    if n_iterations == 0:
        gons = [RegPol((o_rxys[0][1], o_rxys[0][2]), n, o_rxys[0][0], **gon_kwargs)]
    else:
        gons = []

    # Recursively populate the set of polygons.
    for ii in range(0, n_iterations):
        n_rxys = []
        for rxy in o_rxys:
            c_rxys = subflake_n(n, rxy, edge_center=edge_center, center_gon=center_polygon)
            if only_centermost_colored and ii < n_iterations-1 and npy.mod(n, 2) == 0:
                for jj in range(0, len(c_rxys)):
                    c_rxys[jj] = (npy.abs(c_rxys[jj][0]), c_rxys[jj][1], c_rxys[jj][2])

            for nrxy in c_rxys:
                n_rxys.append(nrxy)

                if ii == n_iterations-1:
                    kwargs = gon_kwargs if npy.sign(nrxy[0]) == npy.sign(top_rad) else cgon_kwargs
                    gons.append(RegPol((nrxy[1], nrxy[2]), n, nrxy[0], **kwargs))

        o_rxys = n_rxys

    # This part is separate from the main loop in case I want to do bulk transforms of some sort
    # before adding the patches to the axes. That may not be necessary.
    for cgon in gons:                 
        ax.add_patch(cgon)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()

    ax.relim()
    ax.autoscale_view(True, True, True)

    # Getting cut off at the edges for whatever reason, add a view buffer
    ylims = ax.get_ylim()
    xlims = ax.get_xlim()

    yrang = abs(ylims[1]-ylims[0])
    xrang = abs(xlims[1]-xlims[0])

    ybuff = view_buff_y*yrang
    xbuff = view_buff_x*xrang

    ax.set_ylim([ylims[0]-ybuff, ylims[1]+ybuff])
    ax.set_xlim([xlims[0]-xbuff, xlims[1]+xbuff])

    return fig
