#!/usr/bin/env python3

import rospy
import serial
import utm
from std_msgs.msg import Header
import math
from imu_driver.msg import imu_msg
import argparse
from imu_driver.srv import convert_to_quaternion

port_ = rospy.get_param('driver/port')

def euler_to_quaternion(roll, pitch, yaw):
    print('waiting')
    rospy.wait_for_service('convert_to_quaternion')
    try:
        print("found server")
        service = rospy.ServiceProxy(
            'convert_to_quaternion', convert_to_quaternion)
        resp = service(roll, pitch, yaw)
        return resp.x, resp.y, resp.z, resp.w
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

def data_read(port):
    pub = rospy.Publisher('imu', imu_msg, queue_size=10)
    rospy.init_node('imu_data')
    port = serial.Serial(port, 115200)
    while not rospy.is_shutdown():
        data = port.readline().decode('utf-8')
        data_input = data.split(',')
        if '$VNYMR' in data_input[0]:
            yaw = float(data_input[1])
            pitch = float(data_input[2])
            roll = float(data_input[3])

            msg = imu_msg()
            h = Header()
            h.stamp = rospy.Time.now()
            h.frame_id = "IMU1_Frame"
            msg.Header = h
            msg.MagField.magnetic_field.x = float(data_input[4]) * 0.0001
            msg.MagField.magnetic_field.y = float(data_input[5]) * 0.0001
            msg.MagField.magnetic_field.z = float(data_input[6]) * 0.0001

            msg.IMU.linear_acceleration.x = float(data_input[7])
            msg.IMU.linear_acceleration.y = float(data_input[8])
            msg.IMU.linear_acceleration.z = float(data_input[9])

            msg.IMU.angular_velocity.x = float(data_input[10])
            msg.IMU.angular_velocity.y = float(data_input[11])
            msg.IMU.angular_velocity.z = float(data_input[12].split('*')[0])

            msg.IMU_backup = data

            res = euler_to_quaternion(roll, pitch, yaw)
            msg.IMU.orientation.x = res[0]
            msg.IMU.orientation.y = res[1]
            msg.IMU.orientation.z = res[2]
            msg.IMU.orientation.w = res[3]

            pub.publish(msg)

if __name__ == '__main__':
    try:
        data_read(port_)
    except rospy.ROSInterruptException:
        port.close()
    except serial.serialutil.SerialException:
        rospy.loginfo("Shutting down IMU Driver node ...")

