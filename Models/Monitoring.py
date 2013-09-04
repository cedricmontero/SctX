# -*- coding: utf-8 -*-
"""
 Classes to handle stretching cell of ID13 within SPEC beamline layout
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2013, European Synchrotron Radiation Facility (ESRF)'
___version___  = '0.1.beta'

# Set the working environment :
import sys
import os
sys.path.append(os.path.realpath('..') + os.path.sep + 'Tools') #  Add the Tools  directory to the module path list
import SpecTools

# Set calculation and data visualisation library :
import pylab
pylab.ion()
import numpy

class ScanningHistory:
    def __init__(self,sfpath):
        """
        Set the specfile and retrieve the date and time history of the data measurement
        @param sfpath : specfile path
        @type sfpath : string
        """
        self.specfile = SpecTools.specfile.Specfile(sfpath)
        self.numberofscans = SpecTools.get_NumberOfScans(self.specfile)
        instant_measurements = []
        print 'Number of scans :',self.numberofscans
        for scannumber in range(0,self.numberofscans):
            instant_measurements.append(SpecTools.get_ScanStartingTime(self.specfile,scannumber+1))
        self.instant_measurements = numpy.array(instant_measurements) 
