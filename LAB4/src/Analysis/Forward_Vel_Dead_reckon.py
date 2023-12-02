import rosbag
from matplotlib import pyplot as plt
import numpy as np
import sys
from scipy import integrate
from scipy.signal import butter, filtfilt

def quaternion_to_euler(ori):
	x, y, z, w = ori.x, ori.y, ori.z, ori.w
	t3 = 2.0 * (w * z + x * y)
	t4 = 1.0 - 2.0 * (y * y + z * z)
	yaw_ = np.arctan2(t3, t4)

	return yaw_


def wrap_to_pi(x):
	res = np.remainder(x, 2*np.pi)
	mask = np.abs(res) > np.pi
	res[mask] -= 2*np.pi*np.sign(res[mask])
	return res 


def filter(x, pass_type):
	normal_cutoff = 0.1 / 38
	b, a = butter(2, normal_cutoff, btype=pass_type, analog=False)
	y = filtfilt(b, a, x)
	return y

bag = rosbag.Bag('/home/aswin_chander/EECE5554/LAB4/src/Data/Data_Driving.bag')
mag_field_x, mag_field_y = [], []
time = []
yaw = []
acceleration_x, acceleration_y = [], []
gyro_z = []

for topic, msg, t in bag.read_messages(topics=['/imu']):
    mag_field_x.append(msg.MagField.magnetic_field.x)
    mag_field_y.append(msg.MagField.magnetic_field.y)
    time.append(msg.Header.stamp.secs)
    yaw.append(quaternion_to_euler(msg.IMU.orientation))
    gyro_z.append(msg.IMU.angular_velocity.z)
    acceleration_x.append(msg.IMU.linear_acceleration.x)
    acceleration_y.append(msg.IMU.linear_acceleration.y)

# Move the initialization inside the loop
mag_field_x = np.array(mag_field_x)
mag_field_y = np.array(mag_field_y)

# Continue with the rest of your code
minimum_x = mag_field_x.min()
maximum_x = mag_field_x.max()
minimum_y = mag_field_y.min()
maximum_y = mag_field_y.max()
x_axis_offset = (minimum_x + maximum_x) / 2.0
y_axis_offset = (minimum_y + maximum_y) / 2.0

hard_iron_x = mag_field_x - x_axis_offset
hard_iron_y = mag_field_y - y_axis_offset

time_imu = np.array(time)
time_imu = time_imu - time_imu[0]

easting, northing = [], []
time = []
for topic, msg, t in bag.read_messages(topics=['/gps']):
    easting.append(msg.UTM_easting)
    northing.append(msg.UTM_northing)
    time.append(msg.Header.stamp.secs)
    
easting, northing = np.array(easting), np.array(northing)
easting -= easting[0]
northing -= northing[0]
time_gps = np.array(time)
time_gps = time_gps - time_gps[0]

mag_field_x_corr = mag_field_x - x_axis_offset
mag_field_y_corr = mag_field_y - y_axis_offset

yaw_magnetometer_raw = np.arctan2(mag_field_x, mag_field_y)
yaw_magnetometer_corr = np.arctan2(mag_field_x_corr, mag_field_y_corr)

yaw_gyro = integrate.cumtrapz(gyro_z, time_imu, initial=0)
yaw_gyro = wrap_to_pi(yaw_gyro)
yaw_magnetometer_corr_smooth = filter(yaw_magnetometer_corr, pass_type='low')
yaw_gyro_high = filter(yaw_gyro, pass_type='high')
yaw_filtered = 0.95*yaw_magnetometer_corr_smooth + 0.05*yaw_gyro_high


velocity_acc = integrate.cumtrapz(acceleration_x, time_imu, initial=0)
m, b = np.polyfit([time_imu[1800], time_imu[-1]], 
	np.array([velocity_acc[1800], velocity_acc[-1]]), 1)
m0, b0 = np.polyfit([time_imu[0], time_imu[8100]], 
	np.array([velocity_acc[0], velocity_acc[8100]]), 1)
m1, b1 = np.polyfit([time_imu[8100], time_imu[17000]], 
	np.array([velocity_acc[8100], velocity_acc[17000]]), 1)
m1_, b1_ = np.polyfit([time_imu[17000], time_imu[23000]], 
	np.array([velocity_acc[17000], velocity_acc[23000]]), 1)
m1__, b1__ = np.polyfit([time_imu[23000], time_imu[26000]], 
	np.array([velocity_acc[23000], velocity_acc[26000]]), 1)
m2, b2 = np.polyfit([time_imu[26000], time_imu[30500]], 
	np.array([velocity_acc[26000], velocity_acc[30500]]), 1)
m3, b3 = np.polyfit([time_imu[30500], time_imu[36000]], 
	np.array([velocity_acc[30500], velocity_acc[36000]]), 1)
m4, b4 = np.polyfit([time_imu[36000], time_imu[40000]], 
	np.array([velocity_acc[36000], velocity_acc[40000]]), 1)
m5, b5 = np.polyfit([time_imu[41000], time_imu[46000]], 
	np.array([velocity_acc[41000], velocity_acc[46000]]), 1)
m6, b6 = np.polyfit([time_imu[46000], time_imu[-1000]], 
	np.array([velocity_acc[46000], velocity_acc[-1000]]), 1)

velocity_fit = time_imu[:8100]*m0 + b0
velocity_fit = np.append(velocity_fit, time_imu[8100:17000]*m1 + b1)
velocity_fit = np.append(velocity_fit, time_imu[17000:23000]*m1_ + b1_)
velocity_fit = np.append(velocity_fit, time_imu[23000:26000]*m1__ + b1__)
velocity_fit = np.append(velocity_fit, time_imu[26000:30500]*m2 + b2)
velocity_fit = np.append(velocity_fit, time_imu[30500:36000]*m3 + b3)
velocity_fit = np.append(velocity_fit, time_imu[36000:40000]*m4 + b4)
velocity_fit = np.append(velocity_fit, time_imu[40000:46000]*m5 + b5)
velocity_fit = np.append(velocity_fit, time_imu[46000:]*m6 + b6)


velocity_acc_corr_ = np.absolute(velocity_fit - velocity_acc)
velocity_acc_corr = np.absolute(time_imu*m + b - velocity_acc)

velocity_gps = []
disp = []
disp.append(0)
for i in range(1, len(easting)):
	dist = np.sqrt(np.square(easting[i-1]-easting[i])+np.square(northing[i-1]-northing[i]))
	velocity_gps.append(dist / 1)
	disp.append(disp[i-1]+dist)
	
def plot(x, y, title, x_label, y_label, label, color):
    plt.plot(x, y, label=label,color=color)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.legend() 

plot(time_imu, velocity_acc, 'Velocity vs Time', 'Time (s)', 'Velocity X', 'Velocity from GPS', color = 'pink')
plot(time_imu, velocity_fit, 'Velocity vs Time', 'Time (s)', 'Velocity X', 'Velocity from IMU', color = 'green')
plt.legend(['GPS', 'IMU'])
#plot(timestamps_imu, velocity_acc_corr, 'Velocity vs Time', 'Time (s)', 'Velocity X', 'Velocity from Acceleration Corrected')

plt.show()



plot(time_gps[:-1], velocity_gps, 'Velocity vs Time', 'Time (s)', 'Velocity X', 'Velocity from GPS after',color = 'purple')
plot(time_imu, velocity_acc_corr, 'Velocity vs Time', 'Time (s)', 'Velocity X', 'Velocity from IMU after',color = 'grey')
plt.legend(['GPS', 'IMU'])
plt.show()



# Dead Reckoning
def plot(x, y, title, x_label, y_label, label, color):
    plt.plot(x, y, label=label,color=color)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.legend() 

# Displacement comparison
disp_vel = integrate.cumtrapz(velocity_acc_corr, time_imu, initial=0)
plot(time_imu, disp_vel,'Displacement vs Time', 'Time (s)', 'Displacement X', 'Integrated',color = 'teal')
plot(time_gps, disp, 'Displacement vs Time', 'Time (s)', 'Displacement X', 'Original',color = 'olive')

plt.show()

# Y acceleration
acceleration_y_gyro = gyro_z*velocity_acc
acceleration_y_gyro_corr = gyro_z*velocity_acc_corr
plot(time_imu, acceleration_y, 'Acceleration vs Time', 'Time (s)', 'Acceleration Y', 'Original', color = 'Red')
plot(time_imu, acceleration_y_gyro_corr, 'Acceleration vs Time', 'Time (s)', 'Acceleration Y', 'Estimated Corrected', color = 'blue')

plt.show()

# Forward velocity - easting and northing components
yaw_filtered = -1*yaw_filtered + 180*np.pi/180
Ve = velocity_acc_corr * np.cos(yaw_filtered)
Vn = velocity_acc_corr * np.sin(yaw_filtered)
position_e = integrate.cumtrapz(Ve, time_imu, initial=0)
position_n = integrate.cumtrapz(Vn, time_imu, initial=0)
position_e_corr = integrate.cumtrapz(0.09*Ve, time_imu, initial=0)
position_n_corr = integrate.cumtrapz(0.09*Vn, time_imu, initial=0)

plot(easting, northing, ' Northing vs Easting', 'Easting', 'Northing', 'GPS',color= 'Black')
plot(position_e_corr, position_n_corr, ' Northing vs Easting', 'Easting', 'Northing', 'IMU Derived; Scaled',color = 'orange')

plt.show()

