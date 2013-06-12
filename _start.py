# -*- coding: utf-8 -*-
"""
 First attempt to analyze data set
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2013, European Synchrotron Radiation Facility (ESRF)'
___version___  = '0.1.beta'

""" ______________________________SETTINGS_____________________________"""

print('Welcome in SctX (v.%s) !'%___version___)


""" External modules (preliminary installation could be require) """
import sys
sys.path.append('.'+'/Tools') # Add the Tools directory to the module path list
import os
import sys
# ESRF library for I/O of 2D X-ray detector images
#try:
#    import fabio
#except ImportError:
#    print('No module to read ESRF edf images. Please install FabIO module.')

""" Internal modules (local modules files) """
import SettingsTools
import SpecTools

""" Set the working directory as experiment directory """
print('Set the working directory :')

SDE = SettingsTools.SetDirectoryEnvironment()
wdname = SDE.wdname
print '    . Working directory is set to',os.getcwd()

""" ______________________________ANALYSIS_____________________________"""

