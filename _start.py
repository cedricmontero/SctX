# -*- coding: utf-8 -*-
"""
 Template to start analysis of data sets within ESRF ID13 scheme
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2013, European Synchrotron Radiation Facility (ESRF)'
___version___  = '0.1.beta'

""" ______________________________SETTINGS_____________________________"""

print('Welcome in SctX (v.%s) !'%___version___)

""" External modules (preliminary installation could be require) """
# Set the working environment : 
import sys
import os
sys.path.append(os.path.realpath('.') + os.path.sep + 'Tools') # Add the Tools directory to the module path list
sys.path.append(os.path.realpath('.') + os.path.sep + 'Models') # Add the Models directory to the module path list
# Set calculation and data visualisation library :
import pylab
pylab.ion()
import numpy

""" Internal modules (local modules files) """
from Tools import SettingsTools

""" Set the working directory as experiment directory """
print('Set the working directory :')

SDE = SettingsTools.SetDirectoryEnvironment()
wdname = SDE.wdname
print '    . Working directory is set to',os.getcwd()

""" ______________________________ANALYSIS_____________________________"""

