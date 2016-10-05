import numpy as np
import datetime
from pandas import Series
import matplotlib.pyplot as plt
plt.ion()

day = ['21', '22', '23', '24', '25', '26', '27', '28', '29']
filess = []
for i in range(len(day)):
    filess.append('BIR_sid_201607'+day[i]+'_000000.txt')



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
    
        times = times[21600:82775]
        data = data[21600:82775]
	sid_full = Series(data, index = times)
	#sid  = sid_full.truncate(t_start, t_end)
	return sid_full

sid_data = []
for i in range(len(filess)):
    ss = make_sid_series(filess[i])
    sid_data.append(ss)

fig, ax = plt.subplots(1)
ax.plot(sid_data[0].index, sid_data[3], label = str(sid_data[3].index[0])[0:10])
ax.plot(sid_data[0].index, sid_data[6], label = str(sid_data[6].index[0])[0:10])
ax.tick_params(which = 'both', labelsize = 10)
ax.legend(loc = 'upper left', fontsize = 10)
ax.set_ylabel('Volts', fontsize = 15)
ax.set_xlabel('Time (UT)', fontsize = 15)
