import numpy as np
import matplotlib.pyplot as plt
from pandas import Series
import datetime
import matplotlib.dates as dates
import seaborn as sns
sns.set_style('ticks',{'xtick.direction':'in','ytick.direction':'in'})
sns.set_context('paper')
f = open('birr_mag_20160724_000002.txt')
ff = f.readlines()
meta = ff[0].split()
ff = ff[1:]

data = []
for i in range(len(ff)):
	if ff[i][0] == '2':
		data.append(ff[i].split())

t_start = '2016-07-24 11:00'
t_end = '2016-07-24 16:00'
	

times = []
index = []
bx = [] 
by = [] 
bz = [] 
E1 = [] 
E2 = [] 
E3 = [] 
E4 = []
T_FG = [] 
T_E = [] 
volts = []
for i in range(0, len(data)):
	times.append(datetime.datetime.strptime(data[i][0]+' ' + data[i][1], '%d/%m/%Y %H:%M:%S'))
	index.append(data[i][2])
	bx.append(data[i][3])
	by.append(data[i][4])
	bz.append(data[i][5])
	E1.append(data[i][6])
	E2.append(data[i][7])
	E3.append(data[i][8])
	E4.append(data[i][9])
	T_FG.append(data[i][10])
	T_E.append(data[i][11])
	volts.append(data[i][12])

def floatify(xx):
	tt = []
	for i in range(0, len(xx)):
		t = np.float(xx[i])
		tt.append(t)
	return tt
bx = floatify(bx)
by = floatify(by)
bz = floatify(bz)

h = np.sqrt(np.array(bx)**2 + np.array(by)**2)
H = Series(h, index = times)
H_tr = H.truncate(t_start, t_end)


BX = Series(bx, index = times).truncate(t_start, t_end)
BY = Series(by, index = times).truncate(t_start, t_end)
BZ = Series(bz, index = times).truncate(t_start, t_end)


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
	sid = sid_full
	return sid

sid_dataa = make_sid_series('BIR_sid_20160724_000000.txt')


fig, ax = plt.subplots(3, sharex = True, figsize = (18, 15))
ax[0].plot(H.index.to_pydatetime(), H, sns.xkcd_rgb["pale red"])
ax[0].set_ylabel('H (nT)', fontsize = 20)
ax[0].set_title('BIRR magnetometer', fontsize = 30)
ax[0].tick_params(which = 'both', labelsize = 18)
ax[0].xaxis.set_major_locator(dates.HourLocator(interval =2))
ax[0].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[0].xaxis.grid(True, which="major")
ax[0].axvline(t_start)
ax[0].axvline(t_end)

ax[1].plot(H.index.to_pydatetime(), np.gradient(H), sns.xkcd_rgb["medium green"])
ax[1].set_ylabel('dH/dt(nT/min)', fontsize = 20)
ax[1].tick_params(which = 'both', labelsize = 18)
ax[1].xaxis.set_major_locator(dates.HourLocator(interval =2))
ax[1].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[1].xaxis.grid(True, which="major")
ax[1].axvline(t_start)
ax[1].axvline(t_end)





ax[2].plot(sid_dataa.index.to_pydatetime(), sid_dataa, sns.xkcd_rgb["denim blue"])
#ax[2].plot(sid_full.index.to_pydatetime(), smooth(sid_full,120), sns.xkcd_rgb["black"])
ax[2].set_ylabel('SID (Volts)', fontsize = 20)
ax[2].tick_params(which = 'both', labelsize = 18)
ax[2].xaxis.set_major_locator(dates.HourLocator(interval =2))
ax[2].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[2].xaxis.grid(True, which="major")
ax[2].set_xlabel('Start time ' + str(BZ.index[0])[0:16]+ ' UT', fontsize = 30)
ax[2].axvline(t_start)
ax[2].axvline(t_end)


plt.tight_layout()






'''

fig, ax = plt.subplots(2, sharex = True, figsize = (18, 15))
ax[0].plot(H.index.to_pydatetime(), H, sns.xkcd_rgb["pale red"])
ax[0].set_ylabel('H (nT)', fontsize = 20)
ax[0].set_title('BIRR magnetometer', fontsize = 30)
ax[0].tick_params(which = 'both', labelsize = 18)
ax[0].xaxis.set_major_locator(dates.HourLocator(interval =2))
ax[0].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[0].xaxis.grid(True, which="major")
ax[0].axvline(t_start)
ax[0].axvline(t_end)

ax[1].plot(H.index.to_pydatetime(), np.gradient(H), sns.xkcd_rgb["medium green"])
ax[1].set_ylabel('dH/dt(nT/min)', fontsize = 20)
ax[1].tick_params(which = 'both', labelsize = 18)
ax[1].xaxis.set_major_locator(dates.HourLocator(interval =2))
ax[1].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[1].xaxis.grid(True, which="major")
ax[1].axvline(t_start)
ax[1].axvline(t_end)

plt.tight_layout()

'''
'''
fig, ax = plt.subplots(3, sharex = True, figsize = (18, 15))
ax[0].plot(BX.index.to_pydatetime(), BX, sns.xkcd_rgb["pale red"])
ax[0].set_ylabel('Bx (nT)', fontsize = 20)
ax[0].set_title('BIRR magnetometer', fontsize = 30)
ax[0].tick_params(which = 'both', labelsize = 18)
ax[0].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
ax[0].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[0].xaxis.grid(True, which="major")
ax[0].axvline(t_start)
ax[0].axvline(t_end)

ax[1].plot(BY.index.to_pydatetime(), BY, sns.xkcd_rgb["medium green"])
ax[1].set_ylabel('By (nT)', fontsize = 20)
ax[1].tick_params(which = 'both', labelsize = 18)
ax[1].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
ax[1].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[1].xaxis.grid(True, which="major")
ax[1].axvline(t_start)
ax[1].axvline(t_end)


ax[2].plot(BZ.index.to_pydatetime(), BZ, sns.xkcd_rgb["denim blue"])
ax[2].set_ylabel('BZ (nT)', fontsize = 20)
ax[2].tick_params(which = 'both', labelsize = 18)
ax[2].xaxis.set_major_locator(dates.MinuteLocator(interval =30))
ax[2].xaxis.set_major_formatter(dates.DateFormatter('%H.%M'))
ax[2].xaxis.grid(True, which="major")
ax[2].set_xlabel('Start time ' + str(BZ.index[0])[0:16]+ ' UT', fontsize = 30)
ax[2].axvline(t_start)
ax[2].axvline(t_end)
plt.tight_layout()
plt.ion()

'''







