import numpy as np
import matplotlib.pyplot as plt
from sunpy import map
import sys
import os
#plt.ion()
from sunpy import lightcurve as lc
get_time = 1
aia_131 = map.Map('/home/laura/QPP/SID_CLEAN/sid-data/july_flare/131_aia/*AIA_131_.fts')
from pandas import read_csv
import datetime
from pandas import Series

def sortedd(aia):
	t = []
	for i in range(len(aia)):
		q = aia[i].date
		w = i
		t.append([w, q])

	new = sorted(t, key = lambda s: s[1])
	new = np.array(new)
	indices = new[:,0]
	indices = list(indices)
	aia_new  = []
	for i in range(len(aia)):
		b = aia[indices[i]]
		aia_new.append(b)
	return aia_new

runn = False
if runn:
	new_aia131 = sortedd(aia_131)




#plotting#
plott = False
if plott:
	for i in range(1000,len(new_aia131)):
		new_aia131[i].plot()
		plt.savefig('/home/laura/QPP/SID_CLEAN/sid-data/july_flare/aia_plots_131/a131'+ str(i)+'.png')
		plt.clf()


#lightcurve#
lightcurve_aia = False
if lightcurve_aia:
	dataa = []
	timess = []
	for i in range(len(new_aia131)):
		dataa.append(np.sum(new_aia131[i].data))
		timess.append(new_aia131[i].date)

	aia_131_lc = Series(dataa, index = timess)

from sunpy import lightcurve as lc
g = lc.GOESLightCurve.create(new_aia131[0].date, new_aia131[-1].date)
gl = g.data['xrsb']
for i in range(100, 1000):
	fig = plt.figure(figsize = (14,28))
	plt.subplot(2,1,1)
	plt.plot(gl)
	plt.axvline(new_aia131[i].date)

	plt.subplot(2,1,2)
	new_aia131[i].plot()
	plt.savefig('/home/laura/QPP/SID_CLEAN/sid-data/july_flare/aia_plots_131_w_gl/a131_gl00'+ str(i)+'.png')

	plt.clf()



plt.tight_layout()
	
