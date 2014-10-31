from __future__ import division
from nflake import plot_nflake
from matplotlib import pyplot as plt
import numpy

# Plot the overlapping diagrams
cdpi = 180
kwargs = {'ec': 'k', 'elw': 0.25, 'center_polygon': False,
          'view_buff_x': 0.001, 'view_buff_y': 0.001, 'fig_dpi': cdpi}

grc = '#d6d6d6'
tc = '#eae2ac'
bc = '#0099cc'
rc = '#af0a0a'
pc = '#8C198C'
gc = '#198c19'
sgc = '#708090'

g1 = '#DCDCDC'
g2 = '#A9A9A9'
g3 = '#708090'

pale_aqua = '#BCD4E6'
l_moss = '#b1d2b1'

color_list = [pale_aqua, tc, rc, g1, bc, l_moss]
name_list = {3: 'Tri', 4: 'Tetra', 5: 'Penta', 6: 'Hexa', 7: 'Hepta', 8: 'Octo', 9: 'Ennea',
             10: 'Deca', 11: 'Hendeca',
             12: 'Dodeca', 13: 'Trideca', 14: 'Tetradeca', 15: 'Pentadeca'}


iters = 4
SaveFig = True
formats = ['svg', 'png']
for n in range(4, 9, 2):
    kwargs['phase_offset'] = True or (numpy.mod(n-6, 4) == 0 or n == 4)
    kwargs['center_polygon'] = True or (n == 4)
    kwargs['fig'] = None
    for ii in range(0, iters+1):
        kwargs['fig'] = plot_nflake(n, ii, color=color_list[ii], **kwargs)

    if SaveFig:
        name = name_list[n] + 'flake-' + ('C' if kwargs['center_polygon'] else 'N') + \
                ' ' + ('Edge' if kwargs['phase_offset'] else 'Vertex') + ' Iterations ' + \
                '00-{:02d}.'.format(iters)

        for cform in formats:
            kwargs['fig'].savefig(name+cform, transparent=True,
                                  bbox_inches='tight', dpi=cdpi, format=cform)

plt.show()
