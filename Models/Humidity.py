# -*- coding: utf-8 -*-
"""
 Classes to handle humidity cell measurements of ID13 within SPEC beamline layout
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

class Humidity:
    def set_specfile(self,sfpath):
        """
        Set the specfile and retrieve the data
        @param sfpath : specfile path
        @type sfpath : string
        """
        self.specfile = SpecTools.specfile.Specfile(sfpath)
        self.Stretch_Time,self.Hum_T  = SpecTools.get_ScanMeasurementsAlongTime(self.specfile,'*','hum_t')
        self.Stretch_Time,self.Hum_H  = SpecTools.get_ScanMeasurementsAlongTime(self.specfile,'*','hum_h')
        self.Stretch_Time,self.Hum_Sp = SpecTools.get_ScanMeasurementsAlongTime(self.specfile,'*','hum_rsp')
        self.Stretch_Time_inHr = []
        for i in self.Stretch_Time:
            self.Stretch_Time_inHr.append((i-self.Stretch_Time[0]).days*24.+(i-self.Stretch_Time[0]).seconds/3600.)
