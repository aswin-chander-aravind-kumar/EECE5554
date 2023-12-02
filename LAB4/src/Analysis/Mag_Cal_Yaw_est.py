#!/usr/bin/env python
# coding: utf-8


import bagpy
import math
import csv
import time
import statistics
from bagpy import bagreader
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from quaternion import quaternion, from_rotation_vector, rotate_vectors
import scipy.integrate as integrate
from scipy.signal import butter
from scipy import signal
from scipy import integrate
from scipy.signal import butter, filtfilt
bag_path = '/home/aswin_chander/EECE5554/LAB4/src/Data/Data_Going_in_Circles.bag'
bag = bagreader(bag_path)

# Extract IMU data
data = bag.message_by_topic('/imu')
readings = pd.read_csv(data)

# Plot raw/uncalibrated data
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.scatter(readings['mag_field.magnetic_field.x'], readings['mag_field.magnetic_field.y'],
            marker='.', label='Raw(or)Uncalibrated Data', color='orange')
plt.gca().set_aspect("equal")

# Calibration
minimum_x = readings['mag_field.magnetic_field.x'].min()
maximum_x = readings['mag_field.magnetic_field.x'].max()
minimum_y = readings['mag_field.magnetic_field.y'].min()
maximum_y = readings['mag_field.magnetic_field.y'].max()

# Hard-iron calibration
x_axis_Offset = (minimum_x + maximum_x) / 2.0
y_axis_Offset = (minimum_y + maximum_y) / 2.0
print("hard-iron x_axis_Offset=", x_axis_Offset)
print("hard-iron y_axis_Offset=", y_axis_Offset)

hard_iron_x = readings['mag_field.magnetic_field.x'] - x_axis_Offset
hard_iron_y = readings['mag_field.magnetic_field.y'] - y_axis_Offset

# Plot hard-iron calibrated data
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.scatter(hard_iron_x, hard_iron_y, marker='+', label='Hard-Iron Calibrated Data', color='darkcyan')
plt.gca().set_aspect("equal")
plt.title('Hard_Iron_Calibration Plot Of Magnetic Field X vs Y')
plt.xlabel('Hard_Iron_X (Guass)')
plt.ylabel('Hard_Iron_Y (Guass)')
plt.legend(loc="best")
plt.show()

# Soft-iron calibration
X_major = hard_iron_x.iloc[2000]
Y_major = hard_iron_y.iloc[2000]

radius = math.sqrt((X_major**2) + (Y_major**2))
theta = np.arcsin((Y_major/radius))

R = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
v = np.array([hard_iron_x, hard_iron_y])

matrix = np.dot(R, v)

# Plot soft-iron calibrated data
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.scatter(matrix[0], matrix[1], marker='x', label='Soft-Iron Calibrated', color='olivedrab')
plt.gca().set_aspect("equal")
plt.title('Soft_Iron_Calibration Of Magnetic Field X vs Y')
plt.xlabel('Soft_Iron_X (Guass)')
plt.ylabel('Soft_Iron_Y (Guass)')
plt.legend()
plt.show()

# Find Major and Minor axis using distance formula
r = 0.2
q = 0.15
sigma = q / r
print('sigma = ', sigma)

# Scaling
matrix2 = np.array([[1, 0], [0, sigma]])
rotate = np.dot(matrix2, matrix)
theta = -theta
R1 = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
v1 = np.dot(R1, rotate)

# Plot final calibrated data
plt.grid(color='grey', linestyle='--', linewidth=1)
plt.scatter(v1[0], v1[1], marker='x', label='Hard and Soft Iron Calibrated Data', color='darkviolet')
plt.gca().set_aspect("equal")
plt.title('Final Calibrated Plot Of Magnetic Field X vs Y')
plt.xlabel('Mx (Guass)')
plt.ylabel('My (Guass)')
plt.rcParams.update({'font.size': 10})
plt.legend()
plt.show()

bag = bagreader('/home/aswin_chander/EECE5554/LAB4/src/Data/Data_Driving.bag')
data = bag.message_by_topic('/imu')
data1 = bag.message_by_topic('/gps')
readings = pd.read_csv(data)
readings1 = pd.read_csv(data1)
#Magnetic Field Calibration
min_x = min(readings['MagField.magnetic_field.x'])
max_x = max(readings['MagField.magnetic_field.x'])
min_y = min(readings['MagField.magnetic_field.y'])
max_y = max(readings['MagField.magnetic_field.y'])

#Hard Iron Calibration
x_axis_Offset = (min_x + max_x)/2.0
y_axis_Offset = (min_y + max_y)/2.0
print("hard-iron x_axis_Offset=", x_axis_Offset)
print("hard-iron y_axis_Offset=", y_axis_Offset)
hard_iron_x = []
p = hard_iron_x.extend((readings['MagField.magnetic_field.x']-x_axis_Offset))
hard_iron_y = []
q = hard_iron_y.extend((readings['MagField.magnetic_field.y']-y_axis_Offset))

X_major = float(hard_iron_x[2000])
Y_major = float(hard_iron_y[2000])


#Soft Iron Calibration
radius = math.sqrt((X_major**2) + (Y_major**2))
print('radius = ', radius)
theta = np.arcsin((Y_major/radius))
print('theta = ', theta)

R = [[np.cos(theta), np.sin(theta)], [np.sin(-theta), np.cos(theta)]]
v = [hard_iron_x, hard_iron_y]

matrix = np.matmul(R, v)
print(np.shape(matrix))

# Major and Minor axis calculation
r = 0.2
q = 0.15
sigma = q/r
print('sigma = ', sigma)

# Scaling factor 
matrix2 = [[1, 0], [0, sigma]]
rotate = np.matmul(matrix2, matrix)
theta = -theta
R1 = [[np.cos(theta), np.sin(theta)], [np.sin(-theta), np.cos(theta)]]
v1 = np.matmul(R1, rotate)
v1 = np.expand_dims(v1, axis=0)

# Yaw calculation
w = readings['IMU.orientation.w']
x = readings['IMU.orientation.x']
y = readings['IMU.orientation.y']
z = readings['IMU.orientation.z']

# Euler from Quaternion(x, y, z, w):
t0 = +2.0 * (w * x + y * z)
t1 = +1.0 - 2.0 * (x * x + y * y)
roll_x = np.arctan2(t0, t1)

t2 = +2.0 * (w * y - z * x)
pitch_y = np.arcsin(t2)

t3 = +2.0 * (w * z + x * y)
t4 = +1.0 - 2.0 * (y * y + z * z)
yaw_z = np.arctan2(t3, t4)

roll = roll_x
pitch = pitch_y
yaw = yaw_z

mag_x = v1[:, 0]
mag_y = v1[:, 1]
mag_z1 = readings['MagField.magnetic_field.z']
data_x = readings['MagField.magnetic_field.x']
data_y = readings['MagField.magnetic_field.y']
data_z = readings['MagField.magnetic_field.z']
mag_z2 = mag_z1.to_numpy()
mag_z = np.reshape(mag_z2, (1, 68307))

# YAW calculation with calibrated data
xa = mag_z*list(np.sin(roll))
xb = mag_y*list(np.cos(roll))
X = xa - xb
ya = mag_x*list(np.cos(pitch))
yb = mag_y*list(np.sin(pitch)*np.sin(roll))
yc = mag_z*list(np.sin(pitch)*np.cos(roll))

Y = ya+yb+yc
calibrated_yaw = np.arctan2(X, Y)
yaw_cal = np.unwrap(calibrated_yaw)
yaw_cmax = max(yaw_cal)
final_cal_yaw = pd.Series(yaw_cmax)
final_cal_yaw = final_cal_yaw * (180 / np.pi)

time = readings['Header.stamp.secs']
# YAW calculation with non_calibrated data
xra = data_z*list(np.sin(roll))
xrb = data_y*list(np.cos(roll))

raw_X = xra - xrb
yra = data_x*list(np.cos(pitch))
yrb = data_y*list(np.sin(pitch)*np.sin(roll))
yrc = data_z*list(np.sin(pitch)*np.cos(roll))

yra = yra.squeeze()
yrb = yrb.squeeze()
yrc = yrc.squeeze()

raw_Y = yra + yrb + yrc
raw_X = raw_X.squeeze()

cal_raw_yaw = np.arctan2(raw_X, raw_Y)
cal_raw_yaw1 = np.unwrap(cal_raw_yaw)
final_cal_raw_yaw = pd.Series(cal_raw_yaw)
final_cal_raw_yaw = final_cal_raw_yaw * (180 / np.pi)
# Integration part

gyro_int = integrate.cumtrapz(readings['IMU.angular_velocity.z'], initial=0)
gyro_int_wrap = np.unwrap(gyro_int)

plt.figure(figsize=(10, 6))

# Plot Gyro Integrated Yaw
plt.plot(time, gyro_int, label='Gyro Integrated Yaw', c='palevioletred', linewidth=2)

# Plot Calibrated Yaw
plt.plot(time, final_cal_yaw, label='Calibrated Yaw', linewidth=1.5)

# Plot Raw Yaw
plt.plot(time, final_cal_raw_yaw, label='Raw IMU Yaw', c='lightseagreen', linewidth=1.2)

plt.legend(loc='upper right', fontsize='small')
plt.grid(color='white', linestyle='-', linewidth=0.5)  # Set grid color to white, linestyle to solid
plt.title('Estimation of Yaw for Magnetometer', fontsize=12)
plt.xlabel('Time (Sec)', fontsize=10)
plt.ylabel('Yaw (degrees)', fontsize=10)
plt.show()

# Filteration
lpf = filtfilt(*butter(3, 0.1, "lowpass", fs=40, analog=False), final_cal_yaw)
hpf = filtfilt(*butter(3, 0.0001, 'highpass', fs=40, analog=False), gyro_int)

# Original Yaw vs Calibrated Yaw
alpha = 0.13
omega = readings['IMU.angular_velocity.z']
yaw_filtered = np.zeros(len(final_cal_yaw))
for i in range(len(final_cal_yaw) - 1):
    yaw_filtered[i + 1] = alpha * (yaw_filtered[i] + hpf[i + 1] * 0.025) + ((1 - alpha) * lpf[i + 1])

# Plotting Raw and Calibrated Yaw
plt.figure(figsize=(10, 6))

# Plot Raw Magnetometer Yaw
plt.plot(time, yaw_z * 200, label='Raw Magnetometer Yaw', linewidth=2.0, c='orange')

# Plot Calibrated Magnetometer Yaw
plt.plot(time, final_cal_yaw, label='Calibrated Magnetometer Yaw', linewidth=2.0)

plt.legend(loc='upper right', fontsize='medium')
plt.grid(color='white', linestyle='-', linewidth=0.5)
plt.xlabel('Time (sec)', fontsize=10)
plt.ylabel('Yaw (degrees)', fontsize=10)
plt.title('Magnetometer Yaw Before vs After Calibration', fontsize=12)
plt.show()

# Filteration
lpf = filtfilt(*butter(3, 0.1, "lowpass", fs=40, analog=False), final_cal_yaw)
hpf = filtfilt(*butter(3, 0.0001, 'highpass', fs=40, analog=False), readings['IMU.angular_velocity.z'])

# Plotting Gyro Yaw and Calibrated Magnetometer Yaw
plt.figure(figsize=(10, 6))

# Plot Gyro Yaw
plt.plot(time, gyro_int, label='Gyroscope Yaw', linewidth=2, color = 'Red')

# Plot Calibrated Magnetometer Yaw
plt.plot(time, final_cal_yaw, label='Calibrated Magnetometer Yaw', linewidth=2, color = 'black')

plt.legend(loc='upper right', fontsize='medium')
plt.grid(color='white', linestyle='-', linewidth=1.5)
plt.xlabel('Time (sec)', fontsize=10)
plt.ylabel('Yaw (degrees)', fontsize=10)
plt.title('Vector Nav: Gyroscope Yaw vs Calibrated Magnetometer Yaw', fontsize=12)
plt.show()

# Filteration
lpf = filtfilt(*butter(3, 0.1, "lowpass", fs=40, analog=False), final_cal_yaw)
hpf = filtfilt(*butter(3, 0.0001, 'highpass', fs=40, analog=False), gyro_int)

# Plotting Low-pass Magnetometer Yaw, High-pass Gyro Yaw, and Complementary Filter Yaw
plt.figure(figsize=(10, 6))

# Plot Low-pass Magnetometer Yaw
plt.plot(time, lpf, label='Magnetometer Yaw LP Filtered', linewidth=2, color ='teal')

# Plot High-pass Gyro Yaw
plt.plot(time, hpf, label='Gyro Yaw HP Filtered', linewidth=1.5, color ='orange')

# Plot Complimentary Filter Yaw
plt.plot(time, yaw_filtered, label='Complimentary Filter Yaw HP+LP', linewidth=1.5, color = 'blue')

plt.legend(loc='upper right', fontsize='medium')
plt.grid(color='white', linestyle='-', linewidth=0.5)
plt.title('Low-pass Magnetometer Yaw, High-pass Gyro Yaw, and Complimentary Filter Yaw', fontsize=12)
plt.xlabel('Time (sec)', fontsize=10)
plt.ylabel('Yaw (degrees)', fontsize=10)
plt.show()



