#-*- coding: utf-8 -*-
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
import NumpyTools

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
        for scannumber in range(0,self.numberofscans_scanning):
            instant_measurements.append(SpecTools.get_ScanStartingTime(self.scanning,scannumber+1))
        self.instant_measurements = numpy.array(instant_measurements)
  
    def synchro_on_scanning(self,sfscanning,timehistory,meashistory,sfscanrange=None):
        """
        Calculate the average of tensmon or humidity informations on each x-ray scans performed. A trick to improve rapidity of calculation have been set.
        @param sfscanning  : specfile of the scanning history
        @param timehistory,meashistory : time and values of measurements performed on tensmon of hummon.
        @param sfscanrange : list of scannumber to synchronize
        """
        scannumbers = SpecTools.get_NumberOfScans(sfscanning)
        averageshistory = []
        idx = 0
        if sfscanrange == None:
            scanrange = range(1,scannumbers+1)
        else:
            scanrange = sfscanrange

        for scan in scanrange:
            scan_starttime = SpecTools.get_ScanStartingTime(self.scanning,scan)
            idx_ini,val_ini = NumpyTools.find_nearest(scan_starttime,timehistory)
            idx = idx_ini
            scan_endtime   = SpecTools.get_ScanEndingTime(self.scanning,scan)
            idx_end,val_end = NumpyTools.find_nearest(scan_endtime,timehistory)
            idx = idx_end
            avghistory = numpy.mean(meashistory[idx_ini:idx_end])
            averageshistory.append(avghistory)
            print scan, scan_starttime, scan_endtime, idx_ini, idx_end, avghistory 
        self.scanning_scannumbers = range(1,scannumbers+1)
        self.scanning_measurements = numpy.array(averageshistory)

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
    
    def display_Stretch_N_datetime(self,specimen_label = None):
        fig = pylab.figure(figsize=(9,4))
        dpl = pylab.gcf()
        dpl.canvas.set_window_title('Stretch_N')
        ax = fig.add_subplot(111)
        dpl.autofmt_xdate()
        ax.plot(self.Stretch_Time,self.Stretch_N,'bx',markersize=2,label=specimen_label)
        ax.set_xlabel('Date time []')
        ax.set_ylabel('Force [N]')
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
