# -*- coding: utf-8 -*-
"""
 This module offer simple functions to retrieve informations from a SPEC file
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = 'European Synchrotron Radiation Facility (ESRF), Grenoble, France'
___version___  = '0.1'

""" External modules (preliminary installation could be require) """
# Public modules :
import datetime
import numpy
from collections import defaultdict # Used in detection of cnofiguration of calibration

# ESRF modules :
try:
    # ESRF module to explore Spec files (contact : jerome.kieffer@esrf.fr)
    import specfile
except ImportError:
    from PyMca import specfile

""" Internal modules (local modules files) """

"""------------------------------------------------------------------------------------"""
"""                    General functions on spec file informations 
---------------------------------------------------------------------------------------"""
def get_ScanNumbers(sf):
    """
    Get the number of scan of the files
    @type sf : specfile object from specfile module
    """
    return int(sf.scanno())

def show_SpecInfos(sf):
    """
    Print some Specfile informations
    @param sf : specfile object or path
    @type  sf : specfile of string
    """
    if type(sf) == 'str':
        sf = specfile.Specfile(sf)
    
    print '%i scans have been performed in this session'% get_ScanNumbers(sf)

def get_ScanCommand(sf,scannumber):
    """
    Get the scan command
    @param sf : specfile object or path to spec file
    @type  sf : specfile or string
    """
    # Convert the entries if required :
    if type(sf) == str:
        sf = specfile.Specfile(sf)
    if type(scannumber) == int:
        scannumber = str(scannumber)
    # Store the scan data :
    scan = sf.select(scannumber)
    # Retrieve the command :
    return scan.header('S')[0]

def get_ScanStartingTime(sf,scannumber):
    """
    Get the starting time of the scan
    @type sf : specfile object from specfile module
    @type scannumber : integer
    """
    # Store the scan data :
    scan = sf.select(str(scannumber))
    data = scan.data()
    # Calculate the first time of the first measurement :
    eptime = sf.epoch() + numpy.array(data[1,:][0])
    schedule   = datetime.datetime.fromtimestamp(eptime)
    return schedule

"""                        Retrieve measurement from a spec file 
---------------------------------------------------------------------------------------"""
def get_ScanValueInSpecHeaderComment(sf,scannumber,field):
	"""
	Retrieve the value of a scan comment field
	@param  sf : specfile object from specfile module
	@type   sf : specfile object
	@param field : field to look for the value in the comments
	@type  field : string
	TODO : print a warning message for unexisting comment
	"""
	scan      = sf.select(str(scannumber))
	scan_head = scan.header('C')
	value     = scan_head[[x for x in range(len(scan_head)) if scan_head[x].split('=')[0] == field][0]].split('=')[1]
	return value

def get_ScanMeasurementsAlongTime(sf,scannumber,motorlabel):
    """
    Retrieve the measurements of a motor label against time
    @type sf : specfile object from specfile module
    @type scannumber : integer
    @type motorlabel : string
    """
    #TODO : rewrite this function based on the get_ScanMeasurement function
    #TODO : extend this function to more than one motor to extract (induce list of string in input and variable number of output of list of output
    def get_SingleScanMeasurementAlongTime(scannumber):
        # Store the scan data:
        scan       = sf.select(str(scannumber))
        data       = scan.data()
        # Find 'Epoch' label and motorlabel column position:
        labelslist = scan.alllabels()
        pos_epoch  = [idx for idx in range(len(labelslist)) if labelslist[idx] == 'Epoch'][0]
        pos_motor  = [idx for idx in range(len(labelslist)) if labelslist[idx] == motorlabel][0]
        # Calculate time elements of the measurements:
        eptime     = sf.epoch() + numpy.array(data[pos_epoch,:])# Create a numpy 1D array with unix epoch time of each measurement
        schedule   = numpy.array([datetime.datetime.fromtimestamp(values) for values in eptime])# Create a numpy 1D array of datetime instant of each measurement
        if pos_motor == []:
            print 'ERROR : The motorlabel required does not exist in the list of the labels of this scan.'
        else:
            measurement = data[pos_motor]
        return schedule,measurement
    if scannumber == '*':
        schedule    = numpy.array([])
        measurement = numpy.array([])
        for scan in range(1,get_NumberOfScans(sf)+1):
            scan_schedule,scan_measurement = get_SingleScanMeasurementAlongTime(scan)
            schedule = numpy.hstack((schedule,scan_schedule))
            measurement = numpy.hstack((measurement,scan_measurement))
    else:
        schedule,measurement = get_SingleScanMeasurementAlongTime(scannumber)
    return schedule,measurement

def get_ScanExposureTime(sf,scannumber):
	"""
	Return the exposure time of the scan
	"""
	scan       = sf.select(str(scannumber))
	time_field = scan.header('T')
	expo_time  = float(time_field[0].split(' ')[1])
	return expo_time 

def findCalibrationConfigs(sf):
	"""
	Find the nominal detector distance, detector binning and exposure time combinations for calibration scripts
	"""
	scan_numbers = get_ScanNumbers(sf)
	calib_config = {}# Create a dictionnary with all the configurations of the scans
	# Get the configuration for calibration on each scan
	for sc in range(1,scan_numbers+1):
		nominal_dist = float(get_ScanValueInSpecHeaderComment(sf,sc,'#C qq.adet.nominaldist'))
		expo_time    = get_ScanExposureTime(sf,sc)
		det_bin_row  = get_ScanValueInSpecHeaderComment(sf,sc,'#C qq.adet.rowbin')
		det_bin_col  = get_ScanValueInSpecHeaderComment(sf,sc,'#C qq.adet.colbin')
		if det_bin_row != det_bin_col:
			print 'Warning : row binning differs with column binning.'
		det_binning = (int(det_bin_row) + int(det_bin_row))	/ 2
		calib_config[sc] = (nominal_dist,det_binning,expo_time)
		print calib_config[sc]
	# Create a reversed dictionnary for each configuration as keys and scans as values
	config_calib = defaultdict(list)
	for k,v in calib_config.iteritems():
		config_calib[v].append(k)

	return config_calib.items()

