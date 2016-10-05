import numpy as np
import os
import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from sunpy import lightcurve as lc
import pylab
import seaborn as sns
sns.set_style('ticks',{'xtick.direction':'in','ytick.direction':'in'})
sns.set_context('paper')
from scipy import ndimage
smooth = ndimage.filters.uniform_filter
import datetime
import matplotlib.dates as dates
from pandas import Series
#---------------------------------------------------#
#Makes list of all the files under consideration from
# 11 - 16 UT
#---------------------------------------------------#
def make_t_array(hour):
    
    t = np.zeros(60)
    times = []
    for i in range(1, len(t)):
        t[i] = t[i-1] + 1
    for i in range(len(t)):
        if i <10:
            times.append(hour + '0' + str(int(t[i])) + '00')
        else:
            times.append(hour + str(int(t[i]))+ '00')
    return times


hours =  ['11', '12', '13', '14', '15', '16']
timess = []
for i in hours:
    timess.append(make_t_array(i))

flatten_times = [val for lst in timess for val in lst]
filess = []
for i in range(len(flatten_times)):
    filess.append('SWX_DRAP20_C_SWPC_20160724'+flatten_times[i]+'_GLOBAL.txt')

dir_path = '/home/laura/QPP/sid/july_event/VLF_Study/d_region/SWX_DRAP20_C_SWPC_20160724'



t_start = '2016-07-24 11:00'
t_end = '2016-07-24 16:00'


#----------------------------------------------------#
#Functions to make sid series and to make GOES lc----#
#----------------------------------------------------#

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


#-----------------------------------------------------#
#Function to return a map with lons, lats and map data#
#-----------------------------------------------------#
def reading_files(file_name):
	f = open(os.path.join(dir_path, file_name))
	a = f.readlines()

	b = []
	for i in range(len(a)):
		if a[i][0] != '#':
			b.append(a[i])

	lat = re.split('\s+',b[0])[1:-1]
	for i in range(len(lat)):
		lat[i] = float(lat[i])
	rest = b[2:]



	alll = []
	longg = []
	for i in range(len(rest)):
		
		s = rest[i].split()
		long1 = s[0]
		values1 = s[2:]
		
		for i in range(len(values1)):
			values1[i] = float(values1[i])
		alll.append(values1)
		
		long1 = float(long1)
		longg.append(long1)
	
	longg.reverse()
	alll.reverse()
	mapp = np.array(alll)
	full_map = mapp.T
	lats, lons = np.meshgrid(np.array(longg), np.array(lat))		

	return lats, lons, full_map





plotting_path = '/home/laura/QPP/sid/july_event/VLF_Study/d_region/world_drap_plots/'
def plot_map(lats, lons, full_map, plot_all = False, i = 0):
	fig=plt.figure()
	m = Basemap(projection = 'cyl', llcrnrlat=-89,urcrnrlat=89, llcrnrlon=-178,urcrnrlon=178, resolution = 'c')
	
	levels = np.arange(0, 35,0.1)
	#CS1 = m.contour(lons,lats,full_map,levels,linewidths=0.5,colors='k',latlon=True)
	CS2 = m.contourf(lons,lats,full_map,levels,cmap=plt.cm.gist_heat_r, extend='both',latlon=True)
	cbar = m.colorbar(CS2,location = 'bottom') 
	cbar.set_label('Degraded Frequency')
	m.drawcoastlines()
	m.drawmapboundary()
	#m.fillcontinents()
	plt.xlim(-133, 77)
	plt.ylim(-56, 89)
	plt.tight_layout()
	if plot_all:
		if i<10:
			plt.savefig(os.path.join(plotting_path, 'img00'+str(i)+'.png')) 
  			plt.clf()
    		elif (i<100 and i>9):
	
			plt.savefig(os.path.join(plotting_path, 'img0'+str(i)+'.png'))
			plt.clf()
    		else:
			plt.savefig(os.path.join(plotting_path, 'img'+str(i)+'.png'))
			plt.clf()
	else:
		plt.show()
	


def plotting_movie(filess, plot_all = False, i = i):

	lats, lons, full_map = reading_files(filess)
	date = '2016-07-24'
	av_lines =  date+' ' +filess[26:28]+':'+filess[28:30]+':'+filess[30:32] #lines for each file time
	ti = ['11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30']
	tims = []
	for j in range(len(ti)):
		tims.append(date + ' '+ti[j])

	birr_lon, birr_lat = [-7.9, 53]
	maine_lon, maine_lat = [-67.1, 44.3]

	#-----------------------------------#
	# PLOTTING
	#-----------------------------------#
	fig = pylab.figure(figsize = (10,5))

	###MAP###
	ax = pylab.axes([0.05, 0.090, 0.60, 0.9])
	m = Basemap(projection = 'cyl', llcrnrlat=-89,urcrnrlat=89, llcrnrlon=-178,urcrnrlon=178, resolution = 'c')
	levels = np.arange(0, 35, 0.1)
	CS2 = m.contourf(lons,lats,full_map,levels,cmap=plt.cm.ocean_r, extend='both',latlon=True)
	cbar = m.colorbar(CS2,location = 'bottom') 
	cbar.set_label('Degraded Frequency (MHz)')
	m.drawcoastlines()
	m.drawmapboundary()
	x_b, y_b = m(birr_lon, birr_lat)
	x_m, y_m = m(maine_lon, maine_lat)
	m.plot(x_b, y_b, marker = 'D', color = 'red', label = 'BIRR Reciever')
	m.plot(x_m, y_m, marker = 'D', color = 'yellow', label = 'NAA Transmitter')
	ax.legend(loc = 'lower left')

	plt.xlim(-133, 77)
	plt.ylim(-56, 89)


	###BIRR DATA###
	bx = pylab.axes([0.70, 0.1, 0.28, 0.42])
	bx.set_xlabel('Start time 24-Jul-2015 11:00')
	bx.plot(sid_dataa.index.to_pydatetime(), (sid_dataa), color =  sns.xkcd_rgb["pale red"], label = 'BIRR VLF')
	bx.plot(sid_dataa.index, (smooth(sid_dataa, 120)), color = 'k', lw = 2, label = 'Smoothed BIRR VLF')
	for k in range(len(tims)):
		bx.axvline(tims[k], linestyle = '--', color = 'grey', lw = 0.5)
	bx.legend(loc = 'upper left')
	bx.set_ylabel('Volts')
	bx.axvline(av_lines, color = 'k')


	###GOES DATA###
	cx = pylab.axes([0.7, 0.56, 0.28, 0.42], sharex = bx)
	plt.setp(cx.get_xticklabels(), visible=False)
	cx.plot(gl.index.to_pydatetime(), (gl)*10e5, label = 'GOES 1-8 $\mathrm{\AA}$')
	cx.xaxis.set_major_locator(dates.HourLocator(interval =1))
	cx.xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
	cx.legend(loc = 'upper left')
	cx.set_ylim(0, 7.1)
	cx.set_ylabel('$\mathrm{Wm^{-2}}$ (x$10^{-6})$')
	for k in range(len(tims)):
		cx.axvline(tims[k], linestyle = '--', color = 'grey', lw = 0.5)
	cx.axvline(av_lines, color = 'k')
	

	###SAVING DATA IF KEYWORD SET###
	if plot_all:
		if i<10:
			plt.savefig(os.path.join(plotting_path, 'img00'+str(i)+'.png')) 
			print 'saving'+str(i)
  			plt.clf()
    		elif (i<100 and i>9):
		
			plt.savefig(os.path.join(plotting_path, 'img0'+str(i)+'.png'))
			print 'saving'+str(i)
			plt.clf()
  		else:
			plt.savefig(os.path.join(plotting_path, 'img'+str(i)+'.png'))
			print 'saving'+str(i)
			plt.clf()
	else:
		plt.show()
	

for i in range(0, 360):
	plotting_movie(filess[i], plot_all = True, i = i)

'''
map_struct = []
for i in range(len(filess)):
	a,b,c = reading_files(filess[i])
	map_struct.append([a,b,c])

for i in range(len(map_struct)):
	plot_map(map_struct[i][0], map_struct[i][1], map_struct[i][2], plot_all = True, i = i)
	'''
