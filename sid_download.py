import numpy as np
import urllib
import urllib2
import datetime
import os.path
from pandas import Series
from pandas import read_csv
from sunpy import lightcurve as lc
from scipy import ndimage
smooth = ndimage.filters.uniform_filter

######################################################
# Code to pull VLF data from SID reciever at Birr RSTO
# http://www.rosseobservatory.ie/data
######################################################



#----------------------------#
#start and end times of flare#
#----------------------------#
t_start = '2015-03-12 13:30'
t_end = '2015-03-12 14:30'



urll = 'http://data.rosseobservatory.ie/data/'+t_start[0:4]+'/'+t_start[5:7]+'/'+t_start[8:10]+'/sid/txt/'

filee = 'BIR_sid_'+t_start[0:4]+t_start[5:7]+t_start[8:10]+'_000000.txt'
file1 = 'birr_SID_'+t_start[0:4]+t_start[5:7]+t_start[8:10]+'_000000.txt'

if os.path.exists('/Users/laura/Documents/QPPs/sid/'+filee) == False:
    print 'downloading'
    status = urllib.urlopen(urll+filee).getcode()
    status1 = urllib.urlopen(urll+file1).getcode()
    if status != 404:
        urllib.urlretrieve(urll+filee, filee)
    elif status1 != 404:
        urllib.urlretrieve(urll+file1, file1)

    else:
        print 'holla'

if os.path.exists('/Users/laura/Documents/QPPs/sid/'+filee) == True:
    a = np.loadtxt(filee, comments = '#', delimiter = ',', dtype = 'str')
    times = []
    data = []
    for i in range(len(a)):
        t = datetime.datetime.strptime(a[i][0], "%Y-%m-%d %H:%M:%S")
        times.append(t)
    
        data.append(a[i][1])
    for i in range(len(data)):
        data[i] = np.float(data[i])
    sid_full = Series(np.array(data), index = times)
    sid = sid_full.truncate(t_start, t_end)


if os.path.exists('/Users/laura/Documents/QPPs/sid/'+file1) == True:
    a = np.loadtxt(file1, comments = '#', delimiter = ',', dtype = 'str')
    times = []
    data = []
    for i in range(len(a)):
        t = datetime.datetime.strptime(a[i][0], "%Y-%m-%d %H:%M:%S")
        times.append(t)
        
        data.append(a[i][1])
    for i in range(len(data)):
        data[i] = np.float(data[i])
    sid_full = Series(np.array(data), index = times)
    sid = sid_full.truncate(t_start, t_end)


##goes data##
g = lc.GOESLightCurve.create(t_start, t_end)
gl = g.data['xrsb']
gs = g.data['xrsa']







