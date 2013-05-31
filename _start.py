# -*- coding: utf-8 -*-
"""
 First attempt to analyze data set
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2013, European Synchrotron Radiation Facility (ESRF)'
___version___  = '0.0.1'

""" ______________________________SETTINGS_____________________________"""

""" External modules (preliminary installation could be require) """
import sys
sys.path.append('.'+'/Tools') # Add the Tools directory to the module path list
import os
# ESRF library for I/O of 2D X-ray detector images
try:
    import fabio
except ImportError:
    print("No module to read ESRF edf images. Please install FabIO module.")

""" Internal modules (local modules files) """
import SpecTools

""" Set the working directory as experiment directory """
# TODO : Check if just below there is PROCESS directory or not
wdname = os.getcwd().rsplit('/',1)[0] + '/'

os.chdir(wdname)# Change current working directory
print 'Working directory is set to',os.getcwd()

""" ______________________________ANALYSIS_____________________________"""

