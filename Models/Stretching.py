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

class Stretching:
    def set_specfile(self,sfpath):
        """
        Set the specfile and retrieve the data
        @param sfpath : specfile path
        @type sfpath : string
        """
        self.specfile = SpecTools.specfile.Specfile(sfpath)
        self.Stretch_Time,self.Stretch_Volt = SpecTools.get_ScanMeasurementsAlongTime(self.specfile,'*','strechVolt')
        self.Stretch_Time,self.Stretch_N = SpecTools.get_ScanMeasurementsAlongTime(self.specfile,'*','strechN')
        self.Stretch_Time,self.Stretch_MM = SpecTools.get_ScanMeasurementsAlongTime(self.specfile,'*','strechMM')
        self.Stretch_Time_inHr = []
        for i in self.Stretch_Time:
            self.Stretch_Time_inHr.append((i-self.Stretch_Time[0]).days*24.+(i-self.Stretch_Time[0]).seconds/3600.)

#if __name__ == '__main__':
    # Try to instantiate the class :
    #S = Stretching()    
