import numpy as np
from sunpy import lightcurve as lc
import matplotlib.pyplot as plt
from pandas import *
from sunpy.time import parse_time
basetime = parse_time('2016-07-24 00:00')
import datetime
from reading_msk_files import read_files
import os
import seaborn as sns
sns.set_style('ticks',{'xtick.direction':'in','ytick.direction':'in'})
sns.set_context('paper')

file_name = 'NAA20160724.txt'

t_start = '2016-07-24 11:00:00'
t_end = '2016-07-24 16:00:00'

def normalise(x): #Function to normalise data
	return (x-np.min(x))/(np.max(x) - np.min(x))


station, t, amp, pha = read_files(file_name)

amp = amp.truncate(t_start, t_end)
pha = pha.truncate(t_start, t_end)




##GOES Data##
goess = lc.GOESLightCurve.create(t_start, t_end)
gl = goess.data['xrsb'] #1-8A Channel




#----------#
#Plot Data
#----------#

fig, ax = plt.subplots(2, sharex = True)

ax[0].plot(amp.index, amp, label = 'Amp(dB)'+station, color = 'r')
ax[0].legend(loc = 'upper left')
ax[1].plot(gl.index, gl, label = 'GOES 1-8 $\mathrm{\AA}$')
ax[1].legend(loc = 'upper left')
ax[1].set_yscale('log')
ax[1].set_xlabel('Start time:' + t_start[0:16] + ' UT')
plt.tight_layout()
plt.subplots_adjust( hspace=0.06)
plt.show()
