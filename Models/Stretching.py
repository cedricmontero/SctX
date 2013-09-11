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
    """
    Class to handle stretching experiments at ESRF ID13.
    """
    def set_tensmon_specfile(self,sfpath):
        """
        Set the tensile monitor specfile and retrieve the data
        @param sfpath : specfile path
        @type sfpath : string
        """
        self.tensmon = SpecTools.specfile.Specfile(sfpath)
        self.Stretch_Time,self.Stretch_Volt = SpecTools.get_ScanMeasurementsAlongTime(self.tensmon,'*','strechVolt')
        self.Stretch_Time,self.Stretch_N = SpecTools.get_ScanMeasurementsAlongTime(self.tensmon,'*','strechN')
        self.Stretch_Time,self.Stretch_MM = SpecTools.get_ScanMeasurementsAlongTime(self.tensmon,'*','strechMM')
        self.Stretch_Time_inHr = []
        for i in self.Stretch_Time:
            self.Stretch_Time_inHr.append((i-self.Stretch_Time[0]).days*24.+(i-self.Stretch_Time[0]).seconds/3600.)

    def set_hummon_specfile(self,sfpath):
        """
        Set the humidity monitor specfile and retrieve the data
        @param sfpath : specfile path
        @type sfpath : string
        @return : measurements of temperature, humidity, and set-point along time onto numpy arrays.
        """
        self.hummon = SpecTools.specfile.Specfile(sfpath)
        self.Hum_Time,self.Hum_Temp = SpecTools.get_ScanMeasurementsAlongTime(self.hummon,'*','hum_t') 
        self.Hum_Time,self.Hum_RH   = SpecTools.get_ScanMeasurementsAlongTime(self.hummon,'*','hum_h') 
        self.Hum_Time,self.Hum_SP   = SpecTools.get_ScanMeasurementsAlongTime(self.hummon,'*','hum_rsp') 

    def set_scanning_specfile(self,sfpath):
        """
        Set the X-ray scanning specfile and retrieve the data
        @param sfpath : specfile path
        @type sfpath : string
        @return : 
        """
        self.scanning = SpecTools.specfile.Specfile(sfpath)
        self.numberofscans_scanning = SpecTools.get_NumberOfScans(self.scanning)
        instant_measurements = []
        for scannumber in range(0,self.numberofscans):
            instant_measurements.append(SpecTools.get_ScanStartingTime(self.scanning,scannumber+1))
        self.instant_measurements = numpy.array(instant_measurements)
   
    def synchro_on_scanning(self):
        """
        Calculate the average of tensmon and humidity informations on each x-ray scans performed
        """
        self.synchro = SpecTools.get_ScanEndingTime(self.scanning,1)
        print self.synchro        

    def display_Stretch_Volt(self,specimen_label = None):
        fig = pylab.figure(figsize=(9,4))
        dpl = pylab.gcf()
        dpl.canvas.set_window_title('Stretch_Volt')
        ax = fig.add_subplot(111)
        ax.plot(self.Stretch_Time_inHr,self.Stretch_Volt,'bx',markersize=2,label = specimen_label)
        ax.set_xlabel('Elapsed Time [hr]')
        ax.set_ylabel('Force [Volt]')
        pylab.grid(True)
        if specimen_label != None:
            pylab.legend()
    
    def display_Stretch_N(self,specimen_label = None):
        fig = pylab.figure(figsize=(9,4))
        dpl = pylab.gcf()
        dpl.canvas.set_window_title('Stretch_N')
        ax = fig.add_subplot(111)
        ax.plot(self.Stretch_Time_inHr,self.Stretch_N,'bx',markersize=2,label = specimen_label)
        ax.set_xlabel('Elapsed Time [hr]')
        ax.set_ylabel('Force [N]')
        pylab.grid(True)
        if specimen_label != None:
            pylab.legend()
    
    def display_Stretch_MM(self,specimen_label = None):
        fig = pylab.figure(figsize=(9,4))
        dpl = pylab.gcf()
        dpl.canvas.set_window_title('Stretch_MM')
        ax = fig.add_subplot(111)
        ax.plot(self.Stretch_Time_inHr,self.Stretch_MM,'bx',markersize=2,label = specimen_label)
        ax.set_xlabel('Elapsed Time [hr]')
        ax.set_ylabel('Disp [mm]')
        pylab.grid(True)
        if specimen_label != None:
            pylab.legend()

    def set_zero_force_offset(self,offset_Volt = None,offset_N = None):
        """
        Correct an offset value in the force measuremets (positive offset decrease the measurement value)
        """
        # TODO : Calculate the ratio N2V and V2N to correct the measurements accordingly
        if offset_Volt != None and offset_N == None:
            self.Stretch_Volt = self.Stretch_Volt - offset_Volt
        elif offset_Volt == None and offset_N != None:
            self.Stretch_N    = self.Stretch_N - offset_N
        else:
            print 'You cannot change Volt and Newton simultaneously !'
    
    def set_zero_disp_offset(self,offset_MM = 0):
        """
        Correct an offset value in the displacement measuremets (positive offset decrease the measurement value)
        """
        self.Stretch_MM = self.Stretch_MM - offset_MM 

if __name__ == '__main__':
    # Try to instantiate the class :
    S = Stretching()    
