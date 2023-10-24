import bagpy
import sklearn.metrics
from bagpy import bagreader
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

#Uncomment below for plotting Occluded Stationary data
#path = "/home/aswin_chander/EECE5554/LAB2/src/Data/Stationary_Occluded.bag"
#bag = bagreader(path)
#Uncomment below for plotting Open Stationary data
#path = "/home/aswin_chander/EECE5554/LAB2/src/Data/Carter_Stationary.bag"
#bag = bagreader(path)
#Uncomment below for plotting walking open data
#path = "/home/aswin_chander/EECE5554/LAB2/src/Data/Carter_Open_Square.bag"
#bag = bagreader(path)
#Uncomment below for plotting walking open data
path = "/home/aswin_chander/EECE5554/LAB2/src/Data/Occluded_Square.bag"
bag = bagreader(path)

bag.topic_table
data = bag.message_by_topic('/gps')
print("Data Path:", data)
readings = pd.read_csv(data)


#for error analysis
easting = readings['UTM_easting']
northing =  readings['UTM_northing']

readings['UTM_easting'] = readings['UTM_easting'] - readings['UTM_easting'].min()
readings['UTM_northing'] = readings['UTM_northing'] - readings['UTM_northing'].min()
print(readings[['UTM_easting', 'UTM_northing']])
print(readings)

#(Dont uncomment) Easting vs Northing Plot for Stationary Data
fig, ax1 = bagpy.create_fig(1)
ax1[0].scatter(x = 'UTM_easting', y = 'UTM_northing', data = readings, s = 20, label = 'Scatter Plot of UTM_easting VS UTM_northing')
for axis in ax1:
    axis.legend()
    axis.set_xlabel('UTM_easting in meters', fontsize = 20)
    axis.set_ylabel('UTM_northing in meters', fontsize = 20)
plt.show()


#Altitude vs Time Plot
fig, ax2 = bagpy.create_fig(1)
ax2[0].scatter(x = 'Time', y = 'Altitude', data = readings, s = 20, label = 'Scatter Plot of Altitude VS Time')
for axis in ax2:
    #axis.legend()
    axis.set_xlabel('Time in seconds', fontsize = 20)
    axis.set_ylabel('Altitude in meters', fontsize = 20)
plt.show()


#(Dont uncomment) mean,variance and std for easting
east_mean = np.mean(easting)
east_var = np.var(easting)
east_std = east_var**0.5

print(f"east_mean: {east_mean}")
print(f"east_var: {east_var}")
print(f"east_std: {east_std}")
#(Dont uncomment) mean,variance and std for northing
north_mean = np.mean(northing)
north_var = np.var(northing)
north_std = north_var**0.5

print(f"north_mean: {north_mean}")
print(f"north_var: {north_var}")
print(f"north_std: {north_std}")

#(Dont uncomment) Error Estimation
error_open_easting = easting - east_mean
error_open_northing = northing - north_mean

#mean of error
mean_open_easting = np.mean(error_open_easting)
mean_open_northing = np.mean(error_open_northing)
print("Mean of error for east for open space:", mean_open_easting)
print("Mean of error for north for open space:", mean_open_northing)

#RMSE error of northing and easting
rmse = np.sqrt((np.mean((error_open_easting - mean_open_easting)**2))+(np.mean((error_open_easting - mean_open_easting)**2)))
print("RMSE for UTM_easting:", rmse)

#meadian of error
median_open_easting = np.median(error_open_easting)
median_open_northing = np.median(error_open_northing)

print("Median of error for east for open space:", median_open_easting)
print("Median of error for north for open space:", median_open_northing)

#(Dont uncomment) 2D histogram plot
fig3,ax3 = bagpy.create_fig(1)
plt.hist2d(easting, northing, cmap='viridis', density=True)
ax3[0].set_title('Easting and Northing histogram')
ax3[0].set_xlabel(' Easting')
ax3[0].set_ylabel(' Northing')

plt.show()


