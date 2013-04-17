# -*- coding: utf-8 -*-
"""
 First attempt to analyze data set
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2013, ESRF'
___version___  = '0.0.1'

""" ______________________________SETTINGS_____________________________"""

""" External modules (preliminary installation could be require) """
import sys
sys.path.append('.'+'/Tools') # Add the Tools directory to the module path list
import os
import fabio                  # ESRF library for I/O of 2D X-ray detector images

""" Internal modules (local modules files) """
import SpecTools

""" Set the working directory as experiment directory """
wdname = os.getcwd().rsplit('/',2)[0] + '/'

os.chdir(wdname)# Change current working directory
print 'Working directory is set to',os.getcwd()

""" ______________________________ANALYSIS_____________________________"""

