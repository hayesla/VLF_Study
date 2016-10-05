import numpy as np
import urllib
import urllib2
import datetime
import os.path
from pandas import Series
from pandas import read_csv
import matplotlib.pyplot as plt
import matplotlib.dates as dates
plt.ion()
from scipy import ndimage
smooth = ndimage.filters.uniform_filter
from sunpy import lightcurve as lc
from astropy.io import fits


t_start = '2016-07-24 11:25'
t_end = '2016-07-24 15:00'


#functions#
def normalise(x): #Function to normalise data
	return (x-np.min(x))/(np.max(x) - np.min(x))

def make_sid_series(file_name):
	a = np.loadtxt(file_name, comments = '#', delimiter = ',', dtype = 'str')
	times = []
	data = []
	for i in range(len(a)):
		t = datetime.datetime.strptime(a[i][0], "%Y-%m-%d %H:%M:%S")
		times.append(t)
        
		data.append(a[i][1])
    
	for i in range(len(data)):
		data[i] = float(data[i])
    
    
	sid_full = Series(data, index = times)
	sid  = sid_full.truncate(t_start, t_end)
	return sid

sid_dataa = make_sid_series('BIR_sid_20160724_000000.txt')

g = lc.GOESLightCurve.create(t_start, t_end)
gl = g.data['xrsb']
gs = g.data['xrsa']

#aia_lightcurve#

date, time, data_aia = np.loadtxt('aia_131_lightcurve.txt', unpack = True, dtype = 'str')
aia_index = []
aia_data_float = []
for i in range(len(date)):
	aia_index.append(datetime.datetime.strptime(date[i] + ' ' + time[i], '%Y-%m-%d %H:%M:%S.%f'))
	aia_data_float.append(float(data_aia[i]))

aia_lc = Series(aia_data_float, index = aia_index)
aia_lc = aia_lc.truncate(t_start, t_end)

'''
#ESP DATA#
data_table, header_table = fits.getdata('esp_L1_2016206_005.fit', 1, header = True)

year = data_table.field('year')
doy = data_table.field('doy')
hour = data_table.field('hour')
minute = data_table.field('minute')
sec = data_table.field('sec')


time_frame = []
for i in range(len(year)):
	a = datetime.datetime(2016, 1,1) +datetime.timedelta(days = int(doy[i])-1, hours = int(hour[i]), minutes = int(minute[i]), seconds=float(sec[i]))
	time_frame.append(a)

sxr = data_table.field('QD')
channel18 = data_table.field('CH_18')
channel26 = data_table.field('CH_26')
channel30 = data_table.field('CH_30')
channel36 = data_table.field('CH_36')

sxr = Series(sxr, index = time_frame)
sxr = sxr.truncate(t_start, t_end)
cha18 = Series(channel18, index = time_frame)
cha18 = cha18.truncate(t_start, t_end)
cha26 = Series(channel26, index = time_frame)
cha26 = cha26.truncate(t_start, t_end)
cha30 = Series(channel30, index = time_frame)
cha30 = cha30.truncate(t_start, t_end)
cha36 = Series(channel36, index = time_frame)
cha36 = cha36.truncate(t_start, t_end)
'''
import seaborn as sns
sns.set_style('ticks',{'xtick.direction':'in','ytick.direction':'in'})
sns.set_context('paper')

plot_goes_sid = False
if plot_goes_sid:
        fig, ax = plt.subplots(2,sharex = True, figsize = (10,15))

        ax[0].plot(sid_dataa.index.to_pydatetime(), sid_dataa, color =  sns.xkcd_rgb["pale red"], label = 'BIRR VLF')
        ax[0].plot(sid_dataa.index, smooth(sid_dataa, 120), color = 'k', lw = 2, label = 'Smoothed BIRR VLF')
        ax[0].tick_params(which = 'both', labelsize = 10)
        ax[0].legend(loc = 'upper left', fontsize = 15)
        ax[0].set_ylabel('Volts', fontsize = 15)




        ax[0].set_title('July Flares BIRR SID and GOES', fontsize = 15)
        ax[0].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
        ax[0].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
        ax[0].xaxis.grid(True, which="major")

        ax[1].plot(gl.index.to_pydatetime(), (gl), label = 'GOES 1-8 $\mathrm{\AA}$')
        ax[1].plot(gs.index, (gs), label = 'GOES 0.4-5 $\mathrm{\AA}$')
        ax[1].legend(loc = 'upper left', fontsize = 15)
        ax[1].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
        ax[1].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
        ax[1].xaxis.grid(True, which="major")
        ax[1].tick_params(which = 'both', labelsize = 10)
        ax[1].set_ylabel('Flux', fontsize = 15)
        ax[1].set_xlabel('Start time: '+t_start, fontsize = 15)

        plt.tight_layout()

plot_all = True
if plot_all:
        fig, ax = plt.subplots(3,sharex = True, figsize = (10,20))

        ax[0].plot(sid_dataa.index.to_pydatetime(), sid_dataa, color =  sns.xkcd_rgb["pale red"], label = 'BIRR VLF')
        ax[0].plot(sid_dataa.index, smooth(sid_dataa, 120), color = 'k', lw = 2, label = 'Smoothed BIRR VLF')
        ax[0].tick_params(which = 'both', labelsize = 10)
        ax[0].legend(loc = 'upper left', fontsize = 15)
        ax[0].set_ylabel('Volts', fontsize = 15)




        ax[0].set_title('July Flares BIRR SID, GOES, AIA', fontsize = 15)
        ax[0].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
        ax[0].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
        ax[0].xaxis.grid(True, which="major")

        ax[1].plot(gl.index.to_pydatetime(), (gl), label = 'GOES 1-8 $\mathrm{\AA}$')
        ax[1].plot(gs.index, (gs), label = 'GOES 0.4-5 $\mathrm{\AA}$')
        ax[1].legend(loc = 'upper left', fontsize = 15)
        ax[1].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
        ax[1].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
        ax[1].xaxis.grid(True, which="major")
        ax[1].tick_params(which = 'both', labelsize = 10)
        ax[1].set_ylabel('Flux', fontsize = 15)
       


        ax[2].plot(aia_lc.index.to_pydatetime(), (aia_lc), label = 'AIA 131 $\mathrm{\AA}$', color = 'black')
        ax[2].legend(loc = 'upper left', fontsize = 15)
        ax[2].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
        ax[2].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
        ax[2].xaxis.grid(True, which="major")
        ax[2].tick_params(which = 'both', labelsize = 10)
        ax[2].set_ylabel('Count Rate (DN/s)', fontsize = 15)
        ax[2].set_xlabel('Start time: '+t_start, fontsize = 15)


        plt.tight_layout()
