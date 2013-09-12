#coding: utf8
"""
Module of function to search in arrays
"""
___author___   = 'Cédric Montero'
___contact___  = 'cedric.montero@esrf.fr'
___copyright__ = '2012, ESRF'
___version___  = '0'

#External modules:
import numpy
import datetime

def find_nearest(value,array):
    """
    Return the nearest element in an array of a specified value
    @param value : value to look into data array
    @type  value : integer or float or datetime values
    @param array : data array of values ordered increasingly. All values contains in array have to be on same type.
    @type  array : numpy 1D array
    """
    if type(array[0]) != datetime.datetime:
        idx = numpy.where(numpy.abs(array - value) == numpy.nanmin(numpy.abs(array - value)))[0][0]
    elif type(array[0]) == datetime.datetime:
        # Create a epoch vector of the datetime array :
        eplist  = [int(instants.strftime('%s')) for instants in datevals]
        eparray = numpy.array(eplist)
        epvalue = int(value.strftime('%s'))
        idx = numpy.where(numpy.abs(eparray - epvalue) == numpy.nanmin(numpy.abs(eparray - epvalue)))[0][0]
    return idx,array[idx]

if __name__ == "__main__":
    data  = numpy.arange(-2.0,5.0,.5)
    point =  -1.6
    index,value = find_nearest(point,data)
    print "The closest value is at the index %i and the value at this index is %s" %(index,str(value))
    
    date1 = datetime.datetime.fromtimestamp(1376028805)
    date2 = datetime.datetime.fromtimestamp(1376028815)
    date3 = datetime.datetime.fromtimestamp(1376028825)
    datevals = numpy.array([date1,date2,date3])

    datep =  datetime.datetime.fromtimestamp(1376028813)
    indexdate,valuedate = find_nearest(datep,datevals)
    print "The closest date value is at the index %i and the date value at this index is %s" %(indexdate,str(valuedate))
