import numpy as np
from sunpy import lightcurve as lc
import matplotlib.pyplot as plt
from pandas import *
from sunpy.time import parse_time
basetime = parse_time('2016-07-24 00:00')
import datetime
from reading_msk_files import read_files
import seaborn as sns
sns.set_style('ticks',{'xtick.direction':'in','ytick.direction':'in'})
sns.set_context('paper')
import matplotlib.dates as dates



t_start = '2016-07-24 11:00:00'
t_end = '2016-07-24 16:00:00'


date = '20160724'
Stations = ['DHO', 'FTA', 'GBZ', 'GQD', 'HWU', 'ICV', 'ITS', 'NAA', 'NAU', 'NPM', 'NRK', 'NWC', 'TBB', 'VTX']
Freq = ['23.4', '20.9', '19.58', '22.1', '18.3', '20.27', '45.9', '24', '40.8', '21.4', '37.5', '19.8', '26.7', '18.2']

files = []
for i in range(0, len(Stations)):
	s = Stations[i]+date+'.txt'
	files.append(s)

all_stations = []
for i in range(0, len(files)):
	t = read_files(files[i], t_start, t_end)
	all_stations.append(t)


goess = lc.GOESLightCurve.create(t_start, t_end)
gl = goess.data['xrsb'] #1-8A Channel
gll = ['GOES 1-8 $\mathrm{\AA}$', 0, gl, gl]
all_stations.insert(0, gll)

fig, axarr = plt.subplots(5,3, figsize = (18,18))
phase = True
amp = False
if phase:
	c = 3
	title = 'Phase (degrees)'
if amp:
	c = 2
	title = 'Amplitude (dB)'


fig.suptitle("All MSK data ("+title+") recieved at Birr with GOES 1-8 $\mathrm{\AA}$", fontsize=18)

k = 0
while k< len(all_stations):
	for i in range(0,5):
		for j in range(0,3):
			if k == 0:
				color = 'g'
			else:
				color = 'b'
			axarr[i,j].plot(all_stations[k][c].index.to_pydatetime(), all_stations[k][c],label = all_stations[k][0], color = color)
			axarr[i,j].xaxis.set_major_locator(dates.HourLocator(interval = 1))
			axarr[i,j].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
			axarr[i,j].xaxis.grid(True, which="major")
			print k
			axarr[i,j].legend(fontsize = 12)
			k+=1
axarr[4,1].set_xlabel('Start time ' + t_start[0:16] + ' UT', fontsize = 18)
plt.subplots_adjust(left = 0.05, right = 0.99, top = 0.92, bottom = 0.05, hspace = 0.3, wspace = 0.1)


