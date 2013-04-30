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
import specfile # ESRF module to explore Spec files (contact : jerome.kieffer@esrf.fr)

""" Internal modules (local modules files) """

""" Functions definitions """
def get_ScanNumbers(sf):
	"""
	Get the number of scan of the files
	@type sf : specfile object from specfile module
	"""
	return sf.scanno()

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
	#type motorlabel : string
	TODO : implementation not finished !!!
	"""
	# Store the scan data :
	scan       = sf.select(str(scannumber))
	data       = scan.data()
	# Calculate time elements of the measurements :
	eptime     = sf.epoch() + numpy.array(data[1,:])# Create a numpy 1D array with unix epoch time of each measurement
	schedule   = numpy.array([datetime.datetime.fromtimestamp(values) for values in eptime])# Create a numpy 1D array of datetime instant of each measurement
	eltime     = numpy.array(data[0,:])# Create a numpy 1D array of elapsed time [s] 
	# Get the data measured mentionned by the motorlabel :
	labelslist = scan.alllabels()
	pos        = [idx for idx in range(len(labelslist)) if labelslist[idx] == motorlabel]
	if pos == []:
		print 'ERROR : The motorlabel required does not exist in the list of the labels of this scan.'
	else:
		print str(pos)
	#return schedule,data

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

