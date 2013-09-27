# -*- coding: utf-8 -*-
"""
 Function to display X-ray images and analysis.
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2012, European Synchrotron Radiation Facility (ESRF)'
___version___  = '0'

""" External modules (preliminary installation could be require) """
import numpy
import pylab
pylab.ion()

""" Functions definitions """
def display_image(npimage):
    fig = pylab.figure()
    dpl = pylab.gcf()
    ax1 = fig.add_subplot(111)
    ax1.imshow(npimage,interpolation='nearest',aspect='auto')
