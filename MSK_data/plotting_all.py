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

all_stations.append(all_stations[0])
all_stations.append(all_stations[1])

goess = lc.GOESLightCurve.create(t_start, t_end)
gl = goess.data['xrsb'] #1-8A Channel


plt.subplot(5,3,1)
plt.plot(gl.index, gl, label = 'GOES 1-8')
for i in range(2, len(all_stations)):
	plt.subplot(5,3,i)
	plt.plot(all_stations[i][3], label = all_stations[i][0])
	plt.legend()

plt.tight_layout()
