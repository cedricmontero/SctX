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
        
    def display_Stretch_Volt(self):
        fig = pylab.figure(figsize=(9,4))
        dpl = pylab.gcf()
        dpl.canvas.set_window_title('Stretch_Volt')
        ax = fig.add_subplot(111)
        ax.plot(self.Stretch_Time_inHr,self.Stretch_Volt,'bx',markersize=2)
        ax.set_xlabel('Elapsed Time [hr]')
        ax.set_ylabel('Force [Volt]')
        pylab.grid(True)
    
    def display_Stretch_N(self):
        fig = pylab.figure(figsize=(9,4))
        dpl = pylab.gcf()
        dpl.canvas.set_window_title('Stretch_N')
        ax = fig.add_subplot(111)
        ax.plot(self.Stretch_Time_inHr,self.Stretch_N,'bx',markersize=2)
        ax.set_xlabel('Elapsed Time [hr]')
        ax.set_ylabel('Force [N]')
        pylab.grid(True)
    
    def display_Stretch_MM(self):
        fig = pylab.figure(figsize=(9,4))
        dpl = pylab.gcf()
        dpl.canvas.set_window_title('Stretch_MM')
        ax = fig.add_subplot(111)
        ax.plot(self.Stretch_Time_inHr,self.Stretch_MM,'bx',markersize=2)
        ax.set_xlabel('Elapsed Time [hr]')
        ax.set_ylabel('Disp [mm]')
        pylab.grid(True)

    def set_zero_force_offset(self,offset_Volt = None,offset_N = None):
        """
        Correct an offset value in the force measuremets (positive offset decrease the measurement value)
        """
        if offset_Volt != None and offset_N == None:
            self.Stretch_Volt = self.Stretch_Volt - offset_Volt
        elif offset_Volt == None and offset_N != None:
            self.Stretch_N    = self.Stretch_N - offset_N
        else
            print 'You cannot change Volt and Newton simultaneously !'
    
    def set_zero_disp_offset(self,offset_MM = 0):
        self.Stretch_MM = self.Stretch_MM - offset_MM 

if __name__ == '__main__':
    # Try to instantiate the class :
    S = Stretching()    
