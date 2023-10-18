from pygnuplot import gnuplot
import numpy as np
class Renderer:
    def __init__(self):
        self.g = gnuplot.Gnuplot(log = True) 
        self.g.set('title "BGP GUI"')
        self.g.unset('key')
        self.g.unset('xlabel')
        self.g.unset('ylabel')
        self.g.unset('xtics')
        self.g.unset('ytics')
        self.g.set('xrange [0:10]')
        self.g.set('yrange [0:10]')
        self.render()
    def render(self):
        self.g.set('object 1 rect from 1,1 to 2,2 lw 5')
        self.g.plot('sqrt(-1)')

