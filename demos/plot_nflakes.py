from __future__ import division
from matplotlib import pyplot as plt
import numpy
import argparse
import sys
import os
sys.path.append('../')
from nflake import plot_nflake


# Parse command line arguments
parser = argparse.ArgumentParser(description="""Generates n-flakes using the default color set.
                                 This will generate an overlay of the first -ni iterations of all 
                                 regular polygons with number of sides n ranges from --start-n (-sn)
                                 to --end-n (-en) (inclusive), with step size --step-n (-tn).""")
parser.add_argument('-s', '--save', help='Save the figures', action='store_true')
parser.add_argument('-ns', '--no-svg', help='If present, the figures won\'t be saved as SVG', 
                    action='store_false')
parser.add_argument('-p', '--png', help='If present, the figures will also be saved as PNG', 
                    action='store_true')
parser.add_argument('-nd', '--no-display', help='If present, the plotting will be suppressed', 
                    action='store_false')
parser.add_argument('-d', '--dpi', help='The DPI of the output figures. Default is 180', 
                    default=180)
parser.add_argument('-fh', '--fig-height', help='The height of the figure (in inches, default is 8)', 
                    default=8)
parser.add_argument('-fw', '--fig-width', help='The width of the figure (in inches, default is 8)',
                    default=8)
parser.add_argument('-sn', '--start-n', help='Number of sides in the lowest-n shape. Default is 6.', 
                    default=6)
parser.add_argument('-en', '--end-n', help='Number of sides in the highest-n shape, '+\
                    'default is start-n.', 
                    default=None)
parser.add_argument('-tn', '--step-n', help='Step size in shape-side loop, default is 1.', 
                    default=1)
parser.add_argument('-ni', '--num-iterations', help='Number of iterations in the nflake. '+\
                    'Warning: This is an exponential, recursive process. Setting this value '+\
                    'too high could result in significant memory consumption! Default is 3', 
                    default=4)
parser.add_argument('-e', '--edge', help='Plot the shared-edge variant', action='store_true')
parser.add_argument('-c', '--center', help='Include a central polygon.', action='store_true')
parser.add_argument('-ms', '--max-shapes', help='Maximum number of shapes allowed per plot. '+\
                    '(This protects against runaway exponentials. Default is 50000.)',
                    default=50000)
parser.add_argument('-o', '--output', help='Output folder for any files saved. Default is '+\
                    './output', default=None)
parser.add_argument('-g', '--use-greek', help='Use greek names for output files.', 
                    action='store_true')


args = parser.parse_args()

start_n = int(args.start_n)
step_n = int(args.step_n)
end_n = start_n if args.end_n is None else int(args.end_n)

dpi = int(args.dpi)
num_iterations = int(args.num_iterations)
figsize = (int(args.fig_width), int(args.fig_height))
max_shapes = int(args.max_shapes)

if args.output is None:
  if not os.path.exists('./output'):
    os.mkdir('./output')
  
  output = './output'
elif not os.path.exists(args.output):
  raise IOError('Output directory '+args.output+' not found!')
else:
  output = args.output

# Check that there won't be excessive resource consumption
nbase = end_n + (1 if args.center else 0)    # Use highest number of shapes
nshapes = numpy.sum([nbase**ii for ii in range(0, num_iterations)])
if nshapes > max_shapes:
  raise Exception('Number of shapes in largest Sierpinski n-gon, '+repr(nshapes)+' exceeds '+\
                  'maximum allowed value of '+repr(max_shapes))

# Plot the overlapping diagrams
kwargs = {'ec': 'k', 'elw': 0.25, 'center_polygon': args.center, 'edge_center': args.edge,
          'view_buff_x': 0.001, 'view_buff_y': 0.001, 'fig_dpi': dpi, 'fig_size': figsize}

# Create a color set to work with
grc = '#d6d6d6'
tc = '#eae2ac'
bc = '#0099cc'
rc = '#af0a0a'
pc = '#8C198C'
gc = '#198c19'

g1 = '#DCDCDC'
g2 = '#A9A9A9'
g3 = '#708090'

pale_aqua = '#BCD4E6'
l_moss = '#b1d2b1'

color_list = [pale_aqua, tc, rc, g1, bc,  l_moss, gc, pale_aqua, pc, g2, 'k', 'w']

# Greek numbering up to 15
name_list = {3: 'Tri', 4: 'Tetra', 5: 'Penta', 6: 'Hexa', 7: 'Hepta', 8: 'Octo', 9: 'Ennea',
             10: 'Deca', 11: 'Hendeca', 12: 'Dodeca', 13: 'Trideca', 14: 'Tetradeca', 
             15: 'Pentadeca', 16: 'Hexadeca', 17: 'Heptadeca', 18: 'Octadeca', 19: 'Enneadeca',
             20: 'Icosa'}


formats = []
if args.no_svg:
  formats.append('svg')
if args.png:
  formats.append('png')

all_figs = []
for n in range(start_n, end_n+1, step_n):
    kwargs['fig'] = None                # Reset the figure
    for ii in range(0, num_iterations+1):
        kwargs['fig'] = plot_nflake(n, ii, color=color_list[ii%len(color_list)], **kwargs)

    all_figs.append(kwargs['fig'])
    if args.save:
        if args.use_greek and n in name_list.keys():
          name_base = 'Sierpinski '+name_list[n]+'gon '
        else:
          name_base = 'Sierpinski {:02d}-gon '.format(n)

        name = name_base + ('C' if kwargs['center_polygon'] else 'N') + \
                ' ' + ('Edge' if kwargs['edge_center'] else 'Vertex') + ' Iterations ' + \
                '00-{:02d}.'.format(num_iterations)

        for cform in formats:
            kwargs['fig'].savefig(os.path.join(output, name+cform), transparent=True,
                                  bbox_inches='tight', dpi=dpi, format=cform)

if args.no_display:
  plt.show()
else:
  for fig in all_figs:
    plt.close(fig)
