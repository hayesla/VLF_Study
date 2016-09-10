import numpy as np
import re
import matplotlib.pyplot as plt 
from mpl_toolkits.basemap import Basemap

f = open('SWX_DRAP20_C_SWPC_20160724000000_GLOBAL.txt')
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
	s = rest[i].split('  ')
	if s[0] == '':
		long1 = s[1]
		values1 = s[2:]
	elif s[0][0] == '-':
		long1 = s[0][0:3]
		values1 = s[1:]
	else:
		long1 = s[0]
		values1 = s[1:]

	values1[-1] = values1[-1][:3]
	for i in range(len(values1)):
		values1[i] = float(values1[i])
	alll.append(values1)
	if long1[-1] == '|':
		long1 = long1[:-1]
	long1 = float(long1)
	longg.append(long1)

longg.reverse()
alll.reverse()
mapp = np.array(alll)
full_map = mapp.T
lats, lons = np.meshgrid(np.array(longg), np.array(lat))

fig=plt.figure()
m = Basemap(projection = 'cyl', llcrnrlat=-89,urcrnrlat=89, llcrnrlon=-178,urcrnrlon=178, resolution = 'c')
#CS1 = m.contour(lons,lats,hgt,15,linewidths=0.5,colors='k',latlon=True)
# fill between contour lines.
levels = np.arange(0, 35,0.1)
CS2 =\
m.contourf(lons,lats,full_map,levels,cmap=plt.cm.viridis,extend='both',latlon=True)
m.colorbar(CS2) # draw colorbar
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawmapboundary()
m.fillcontinents()
plt.show()


