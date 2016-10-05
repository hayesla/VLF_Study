import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap


dir_path = '/home/laura/QPP/sid/july_event/TEC/dat'
datee = []
for i in range(11, 17):
	if i<10:
		datee.append(str(0)+str(i))
	else:
		datee.append(str(i))
file_start = 'DLRNZ-GNSS-GCG-R-2-TCAV-NC-GB-M05-D-2016-206-'
timz = ['00','15','30','45']
file_name = []
for i in range(len(datee)):
    for j in range(0,4):
        file_name.append(file_start + datee[i]+'-'+timz[j]+'-' + '00.dat')


plotting_path = '/home/laura/QPP/sid/july_event/TEC/tec_plots/only_flare/'
plot_all = True
def plot_file(file_name):

	f = open(os.path.join(dir_path, file_name))
	all_lines = f.readlines()
	meta = all_lines[0]
	data1 = all_lines[1:]
	data = []
	for k in range(len(data1)):
		data.append(data1[k].split())
	for l in range(len(data)):
		for m in range(len(data[0])):
			data[l][m] = float(data[l][m])
	
	
	
	lats = np.arange(-90, 91, 2.5)
	lons = np.arange(-180, 181, 5)
	
	latitude , longitude = np.meshgrid(lats, lons)
	mapp = np.array(data).T
	mapp =np.fliplr(mapp)
	
	fig=plt.figure(figsize = (10, 7))

	levels = np.arange(0, 100, 1)
	levels1 = np.arange(0, 35, 5)
	m = Basemap(projection = 'cyl', llcrnrlat=-90,urcrnrlat=90, llcrnrlon=-180,urcrnrlon=180, resolution = 'c')
	CS2 = m.contourf(longitude, latitude, mapp,levels, cmap='magma_r')
	CS = m.contour(longitude, latitude, mapp,levels1, colors = 'white', linewidths = 0.5, linestyle = 'dashed')
	plt.clabel(CS, inline=1, fontsize=10)
	cbar = m.colorbar(CS2) 
	cbar.set_label('TEC/TECU')
	plt.title('Total Electron Content (TEC) 24-July-16 '+file_name[45:-4]) 
	m.drawcoastlines()
	m.drawmapboundary()
	m.drawmeridians(np.arange(0,301,60), labels=[0,0,0,1], fmt='%d', linewidth=0.2)
	m.drawparallels(np.arange(-90,91,30), labels=[1,0,0,0], fmt='%d', linewidth=0.2)
	#plt.tight_layout()
	if plot_all:
		print i
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


for i in range(len(file_name)):
	plot_file(file_name[i])	



