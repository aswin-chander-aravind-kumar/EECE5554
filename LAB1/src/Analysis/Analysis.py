import bagpy
import sklearn.metrics
from bagpy import bagreader
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


#Uncomment below for plotting open data
#path = "/home/aswin_chander/EECE5554/LAB1/src/Data/Open.bag"
#bag = bagreader(path)
#Uncomment below for plotting occluded data
#path = "/home/aswin_chander/EECE5554/LAB1/src/Data/Occluded.bag"
#bag = bagreader(path)
#Uncomment below for plotting walking data
path = "/home/aswin_chander/EECE5554/LAB1/src/Data/Walking.bag"
bag = bagreader(path)

bag.topic_table
data = bag.message_by_topic('/gps')
print("Data Path:", data)
readings = pd.read_csv(data)

x = readings['UTM_easting']
y = readings['UTM_northing']

#for error analysis
easting = readings['UTM_easting']
northing =  readings['UTM_northing']

readings['UTM_easting'] = readings['UTM_easting'] - readings['UTM_easting'].min()
readings['UTM_northing'] = readings['UTM_northing'] - readings['UTM_northing'].min()
print(readings[['UTM_easting', 'UTM_northing']])
print(readings)

#(Dont uncomment) Easting vs Northing Plot for Stationary Data
#fig, ax1 = bagpy.create_fig(1)
#ax1[0].scatter(x = 'UTM_easting', y = 'UTM_northing', data = readings, s = 20, label = 'Scatter Plot of UTM_easting VS UTM_northing')
#for axis in ax1:
    #axis.legend()
    #axis.set_xlabel('UTM_easting in meters', fontsize = 20)
    #axis.set_ylabel('UTM_northing in meters', fontsize = 20)
#plt.show()

# Easting vs Northing Plot with Best Fit Line for walking data
fig, ax1 = bagpy.create_fig(1)
ax1[0].scatter(x='UTM_easting', y='UTM_northing', data=readings, s=20, label='Scatter Plot of UTM_easting VS UTM_northing')
coefficients = np.polyfit(readings['UTM_easting'], readings['UTM_northing'], 1)
m, c = coefficients
east_values = np.array(readings['UTM_easting'])  # Convert to NumPy array
north_values = m * east_values + c
ax1[0].plot(east_values, north_values, color='black', label='Scatterplot with best line fit')
for axis in ax1:
    axis.set_xlabel('UTM_easting in meters', fontsize=20)
    axis.set_ylabel('UTM_northing in meters', fontsize=20)
    #axis.legend()

plt.show()



#Altitude vs Time Plot
fig, ax2 = bagpy.create_fig(1)
ax2[0].scatter(x = 'Time', y = 'Altitude', data = readings, s = 20, label = 'Scatter Plot of Altitude VS Time')
for axis in ax2:
    #axis.legend()
    axis.set_xlabel('Time in seconds', fontsize = 20)
    axis.set_ylabel('Altitude in meters', fontsize = 20)
plt.show()


#uncomment the below for stationary open and occluded data 

#(Dont uncomment) known position for open data
#north = 4689328.86
#east = 327799.50  

#(Dont uncomment) known position for o data
#north = 4689418.90
#east = 327924.54

#(Dont uncomment) mean,variance and std for easting
#east_mean = np.mean(easting)
#east_var = np.var(easting)
#east_std = east_var**0.5

#print(f"east_mean: {east_mean}")
#print(f"east_var: {east_var}")
#print(f"east_std: {east_std}")
#(Dont uncomment) mean,variance and std for northing
#north_mean = np.mean(northing)
#north_var = np.var(northing)
#north_std = north_var**0.5

#print(f"north_mean: {north_mean}")
#print(f"north_var: {north_var}")
#print(f"north_std: {north_std}")

#(Dont uncomment) Error Estimation
#error_open_easting = easting - east
#error_open_northing = northing - north


#mean_open_easting = np.mean(error_open_easting)
#mean_open_northing = np.mean(error_open_northing)

#print("Mean of error for east for open space:", mean_open_easting)
#print("Mean of error for north for open space:", mean_open_northing)

#median_open_easting = np.median(error_open_easting)
#median_open_northing = np.median(error_open_northing)

#print("Median of error for east for open space:", median_open_easting)
#print("Median of error for north for open space:", median_open_northing)

#(Dont uncomment) histogram plot
#fig3,ax3 = plt.subplots(2)
#ax3[0].hist(error_open_easting, bins = 20)
#ax3[0].set_title('Easting error(m)')
#ax3[0].set_xlabel('Error from known(m) Measured Easting(m)')
#ax3[0].set_ylabel('Frequency of error in Easting(m)')

#ax3[1].hist(error_open_northing, bins = 20)
#ax3[1].set_title('Northing error(m)')
#ax3[1].set_xlabel('Error from known(m) Measured Northing(m)')
#ax3[1].set_ylabel('Frequency of error in Northing(m)')

#plt.show()

