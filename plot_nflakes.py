from __future__ import division
from matplotlib import pyplot as plt
from nflake import plot_nflake

color_list = ['#eeeeee', '#fcf49f', '#b6ddc7', '#0093dd', '#e32822']
line_color = '#a8a6a5'


kwargs = {'ec':line_color}
'''
fig = plot_nflake(8, 0, color=color_list[0], elw=0.75, **kwargs)
kwargs['fig'] = fig
plot_nflake(8, 1, color=color_list[1], elw=0.5, **kwargs)
plot_nflake(8, 2, color=color_list[2], elw=0.25, **kwargs)
plot_nflake(8, 3, color=color_list[3], elw=0.1, **kwargs)
plot_nflake(8, 4, color=color_list[4], elw=0.0, **kwargs)

fig.savefig('Octoflake-NC Iterations 01-04.svg', transparent=True, format='svg', dpi=120)

kwargs['phase_offset'] = True
kwargs['fig'] = None
fig = plot_nflake(10, 0, color=color_list[0], elw=0.75, **kwargs)
kwargs['fig'] = fig
plot_nflake(10, 1, color=color_list[1], elw=0.5, **kwargs)
plot_nflake(10, 2, color=color_list[2], elw=0.25, **kwargs)
plot_nflake(10, 3, color=color_list[4], elw=0.1, **kwargs)
plot_nflake(10, 4, color=color_list[3], elw=0.0, **kwargs)

fig.savefig('Decaflake-NC Iterations 01-04.svg', transparent=True, format='svg', dpi=120)
'''

kwargs['phase_offset'] = False

kwargs['fig'] = None
fig = plot_nflake(12, 0, color=color_list[0], elw=0.75, **kwargs)
kwargs['fig'] = fig
plot_nflake(12, 1, color=color_list[1], elw=0.5, **kwargs)
plot_nflake(12, 2, color=color_list[2], elw=0.25, **kwargs)
plot_nflake(12, 3, color=color_list[4], elw=0.1, **kwargs)
#plot_nflake(12, 4, color=color_list[3], elw=0.0, **kwargs)
plt.show();

fig.savefig('Dodecaflake-NC Iterations 01-03.svg', transparent=True, format='svg', dpi=120)