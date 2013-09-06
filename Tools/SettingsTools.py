# -*- coding: utf-8 -*-
"""
 Module to set the environment
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2013, European Synchrotron Radiation Facility (ESRF)'

"""
_______________________ Set the working directory within ID13 data phylosophy _________________________
"""
import os

class SetDirectoryEnvironment:
    def __init__(self):
        try:
            # Retrieve the directory up to PROCESS directory if it exists and set the working directory
            self.wdname = self.getpath_uptodir('PROCESS')
            os.chdir(self.wdname)
        except ValueError:
            print 'No PROCESS directory founded'

    def getpath_uptodir(self,keydname):
        return os.getcwd().rsplit(os.path.sep,len(os.getcwd().split(os.path.sep)) - os.getcwd().split(os.path.sep).index(keydname))[0] + os.path.sep
