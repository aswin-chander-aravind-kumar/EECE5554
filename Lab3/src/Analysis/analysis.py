import bagpy
import math
import csv
import statistics
from bagpy import bagreader
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
plt.rcParams.update({'font.size': 16})

bag = bagreader('/home/aswin_chander/EECE5554/LAB3/src/Data/Moving.bag')
data = bag.message_by_topic('/imu')
readings = pd.read_csv(data)
print(readings.columns)
w = readings['IMU.orientation.w'] * (np.pi/180)
x = readings['IMU.orientation.x']* (np.pi/180)
y = readings['IMU.orientation.y']* (np.pi/180)
z = readings['IMU.orientation.z']* (np.pi/180)
print(w, readings['IMU.orientation.w'])



#def euler_from_quaternion(x, y, z, w):
t0 = +2.0 * (w * x + y * z)
t1 = +1.0 - 2.0 * (x * x + y *y)
roll_x = np.degrees(np.arctan2(t0, t1))

t2 = +2.0 * (w * y - z * x)
t2 = np.where(t2>+1.0, +1.0,t2)
t2 = np.where(t2<-1.0, -1.0,t2)
pitch_y = np.degrees(np.arcsin(t2))

t3 = +2.0 * (w * z + x * y)
t4 = +1.0 - 2.0 * (y * y+ z * z)
yaw_z = np.degrees(np.arctan2(t3, t4))

readings['Time'] = readings['Time'] - readings['Time'].min()
readings['IMU.angular_velocity.x'] = readings['IMU.angular_velocity.x'] - readings['IMU.angular_velocity.x'].min()
readings['IMU.angular_velocity.y'] = readings['IMU.angular_velocity.y'] - readings['IMU.angular_velocity.y'].min()
readings['IMU.angular_velocity.z'] = readings['IMU.angular_velocity.z'] - readings['IMU.angular_velocity.z'].min()
readings['IMU.linear_acceleration.x'] = readings['IMU.linear_acceleration.x'] - readings['IMU.linear_acceleration.x'].min()
readings['IMU.linear_acceleration.y'] = readings['IMU.linear_acceleration.y'] - readings['IMU.linear_acceleration.y'].min()
readings['IMU.linear_acceleration.z'] = readings['IMU.linear_acceleration.z'] - readings['IMU.linear_acceleration.z'].min()
readings['MagField.magnetic_field.x'] = readings['MagField.magnetic_field.x'] - readings['MagField.magnetic_field.x'].min()
readings['MagField.magnetic_field.y'] = readings['MagField.magnetic_field.y'] - readings['MagField.magnetic_field.y'].min()
readings['MagField.magnetic_field.z'] = readings['MagField.magnetic_field.z'] - readings['MagField.magnetic_field.z'].min()

#MEAN CALCULATION OF RPY
print('Mean & Standard Deviation of RPY:')
print('mean = ',statistics.mean(roll_x))
print('mean = ',statistics.mean(pitch_y))
print('mean = ',statistics.mean(yaw_z))
print('standard deviation = ',statistics.stdev(roll_x))
print('standard deviation = ',statistics.stdev(pitch_y))
print('standard deviation = ',statistics.stdev(yaw_z))

#MEAN CALCULATION OF ANGULAR VELOCITY
print('Mean & Standard Deviation of Angular Velocity:')
for i in ['IMU.angular_velocity.x', 'IMU.angular_velocity.y', 'IMU.angular_velocity.z']:
    print('mean = ',readings[i].mean())
    print('standard deviation = ',readings[i].std())


#MEAN CALCULATION OF LINEAR ACCELERATION
print('Mean & Standard Deviation of Linear Acceleration:')
for i in ['IMU.linear_acceleration.x', 'IMU.linear_acceleration.y', 'IMU.linear_acceleration.z']:
    print('mean = ',readings[i].mean())
    print('standard deviation = ',readings[i].std())
    print('median = ',readings[i].median())

#MEAN CALCULATION OF MAGNETIC FIELD
print('Mean & Standard Deviation of Magnetic Field:')
for i in ['MagField.magnetic_field.x', 'MagField.magnetic_field.y', 'MagField.magnetic_field.z']:
    print('mean = ',readings[i].mean())
    print('standard deviation = ',readings[i].std())
time = readings['Time'].to_numpy()
ang_vel_x = readings['IMU.angular_velocity.x'].to_numpy()
ang_vel_y = readings['IMU.angular_velocity.y'].to_numpy()
ang_vel_z = readings['IMU.angular_velocity.z'].to_numpy()
lin_acc_x = readings['IMU.linear_acceleration.x'].to_numpy()
lin_acc_y = readings['IMU.linear_acceleration.y'].to_numpy()
lin_acc_z = readings['IMU.linear_acceleration.z'].to_numpy()
mag_field_x = readings['MagField.magnetic_field.x'].to_numpy()
mag_field_y = readings['MagField.magnetic_field.y'].to_numpy()
mag_field_z = readings['MagField.magnetic_field.z'].to_numpy()
# Plot ang_vel_x
fig, ax = plt.subplots()
ax.plot(time, ang_vel_x)
ax.set_xlabel('Time')
ax.set_ylabel('Angular Velocity (x)')
ax.set_title('Time vs Angular Velocity_X')
# Plot ang_vel_y
fig, ay = plt.subplots()
ay.plot(time, ang_vel_y)
ay.set_xlabel('Time')
ay.set_ylabel('Angular Velocity (y)')
ay.set_title('Time vs Angular Velocity_y')
# Plot ang_vel_z
fig, az = plt.subplots()
az.plot(time, ang_vel_z)
az.set_xlabel('Time')
az.set_ylabel('Angular Velocity (z)')
az.set_title('Time vs Angular Velocity_z')
# Plot linear_acc_x
fig, ax = plt.subplots()
ax.plot(time, lin_acc_x)
ax.set_xlabel('Time')
ax.set_ylabel('linear acceleration (x)')
ax.set_title('Time vs linear_acceleration_X')
# Plot linear_acc_y
fig, ay = plt.subplots()
ay.plot(time, lin_acc_y)
ay.set_xlabel('Time')
ay.set_ylabel('linear acceleration (y)')
ay.set_title('Time vs linear_acceleration_y')
# Plot linear_acc_z
fig, az = plt.subplots()
az.plot(time, lin_acc_z)
az.set_xlabel('Time')
az.set_ylabel('linear acceleration (z)')
az.set_title('Time vs linear_acceleration_z')
# Plot mag_field_x
fig, ax = plt.subplots()
ax.plot(time, mag_field_x)
ax.set_xlabel('Time')
ax.set_ylabel('magnetic field (x)')
ax.set_title('Time vs magnetic_field_x')
# Plot mag_field_y
fig, ay = plt.subplots()
ay.plot(time, mag_field_y)
ay.set_xlabel('Time')
ay.set_ylabel('magnetic field (y)')
ay.set_title('Time vs magnetic_field_y')
# Plot mag_field_z
fig, az = plt.subplots()
az.plot(time, mag_field_z)
az.set_xlabel('Time')
az.set_ylabel('magnetic field (z)')
az.set_title('Time vs magnetic_field_z')
#histogram ang_vel_x
fig, ax = plt.subplots()
ax.hist(ang_vel_x, bins=40)
ax.set_xlabel('ang_vel_x')
ax.set_ylabel('frequency')
ax.set_title('Histogram_Angular_Velocity_x')
#histogram ang_vel_y
fig, ay = plt.subplots()
ay.hist(ang_vel_y, bins=40)
ay.set_xlabel('ang_vel_y')
ay.set_ylabel('frequency')
ay.set_title('Histogram_Angular_Velocity_y')
#histogram ang_vel_z
fig, az = plt.subplots()
az.hist(ang_vel_z, bins=40)
az.set_xlabel('ang_vel_z')
az.set_ylabel('frequency')
az.set_title('Histogram_Angular_Velocity_z')
#histogram lin_acc_x
fig, ax = plt.subplots()
ax.hist(lin_acc_x, bins=40)
ax.set_xlabel('lin_acc_x')
ax.set_ylabel('frequency')
ax.set_title('Histogram_Linear_Acceleration_x')
#histogram lin_acc_y
fig, ay = plt.subplots()
ay.hist(lin_acc_y, bins=40)
ay.set_xlabel('lin_acc_y')
ay.set_ylabel('frequency')
ay.set_title('Histogram_Linear_Acceleration_y')
#histogram lin_acc_z
fig, az = plt.subplots()
az.hist(lin_acc_z, bins=40)
az.set_xlabel('lin_acc_z')
az.set_ylabel('frequency')
az.set_title('Histogram_Linear_Acceleration_z')
# histogram mag_field_x
fig, ax = plt.subplots()
ax.hist(mag_field_x, bins=40)
ax.set_xlabel('Magnetic_Field_x')
ax.set_ylabel('Frequency')
ax.set_title('Histogram_Magnetic_Field_x')
# histogram mag_field_y
fig, ay = plt.subplots()
ay.hist(mag_field_y, bins=40)
ay.set_xlabel('Magnetic_Field_y')
ay.set_ylabel('Frequency')
ay.set_title('Histogram_Magnetic_Field_y')
# histogram mag_field_z
fig, az = plt.subplots()
az.hist(mag_field_z, bins=40)
az.set_xlabel('Magnetic_Field_z')
az.set_ylabel('Frequency')
az.set_title('Histogram_Magnetic_Field_z')
#initializing the plot
time_array = np.array(readings['Time'])
roll_x = np.array(roll_x)
pitch_y = np.array(pitch_y)
yaw_z = np.array(yaw_z)
#Plot roll
fig, ax = plt.subplots()
ax.plot(time_array, roll_x)
ax.set_xlabel('Time')
ax.set_ylabel('Roll')
ax.set_title('Time vs Roll')
#Plot roll
fig, ax = plt.subplots()
ax.plot(time_array, pitch_y)
ax.set_xlabel('Time')
ax.set_ylabel('Pitch')
ax.set_title('Time vs Pitch')
#Plot roll
fig, ax = plt.subplots()
ax.plot(time_array, yaw_z)
ax.set_xlabel('Time')
ax.set_ylabel('Yaw')
ax.set_title('Time vs Yaw')
#Plot roll
fig, ax = plt.subplots()
ax.hist(roll_x, bins = 40)
ax.set_xlabel('Roll')
ax.set_ylabel('Frequency')
ax.set_title('Histogram_Roll')
#Plot roll
fig, ay = plt.subplots()
ay.hist(pitch_y, bins=40)
ay.set_xlabel('Pitch')
ay.set_ylabel('Frequency')
ay.set_title('Histogram_Pitch')
#Plot roll
fig, az = plt.subplots()
az.hist(yaw_z, bins=40)
az.set_xlabel('Yaw')
az.set_ylabel('Frequency')
az.set_title('Histogram_Yaw')
plt.show()
