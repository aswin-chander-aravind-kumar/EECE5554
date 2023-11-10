#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import rospy
import serial
import utm
import numpy as np
from imu_driver.msg import imu_msg
from imu_driver.srv import convert_to_quaternion
import datetime


def euler_to_quaternion(roll, pitch, yaw):
    try:
        rospy.wait_for_service("convert_to_quaternion")
        service = rospy.ServiceProxy('convert_to_quaternion', convert_to_quaternion)
        
        # Call the service with the provided Euler angles
        resp = service(roll, pitch, yaw)
        return (resp.qx, resp.qy, resp.qz, resp.qw)
    
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)
        return None

def talker():
    pub = rospy.Publisher('imu',imu_msg, queue_size=10)
    rospy.init_node('imu_driver')
    rate = rospy.Rate(1)
    port = rospy.get_param('driver/port')
    serial_baud = rospy.get_param('~baudrate',115200)
    port = serial.Serial(port, serial_baud, timeout=3)
    msg = imu_msg()
    
    while not rospy.is_shutdown():
        line = port.readline()
        print(line)
        if "$VNYMR" in str(line):
            data_input = str(line).split(",")


            yaw = float(data_input[1])
            pitch = float(data_input[2])
            roll = float(data_input[3])
            print("Roll,Pitch,Yaw:",roll,pitch,yaw)
        
            (qx, qy, qz, qw) = quaternion = euler_to_quaternion(roll, pitch, yaw)

            

            mag_field_x = float(data_input[4])
            mag_field_y = float(data_input[5])
            mag_field_z = float(data_input[6])

            lin_acc_x = float(data_input[7])
            lin_acc_y = float(data_input[8])
            lin_acc_z = float(data_input[9])

            gyro_x = float(data_input[10])
            gyro_y = float(data_input[11])
            gyro_z = float(data_input[12][0:9])


            #If the coordinates arent received, stop the code
            if data_input[2]=='':
                print("Data not being received")
                break
            
            #Publish to msg
            msg.header.frame_id = 'IMU1_Frame'
            msg.header.stamp = rospy.Time.now()

            msg.imu.orientation.x = qx
            msg.imu.orientation.y = qy
            msg.imu.orientation.z = qz
            msg.imu.orientation.w = qw
            msg.imu.angular_velocity.x = gyro_x
            msg.imu.angular_velocity.y = gyro_y   
            msg.imu.angular_velocity.z = gyro_z
            msg.imu.linear_acceleration.x = lin_acc_x
            msg.imu.linear_acceleration.y = lin_acc_y   
            msg.imu.linear_acceleration.z = lin_acc_z
            msg.mag_field.magnetic_field.x = mag_field_x
            msg.mag_field.magnetic_field.y = mag_field_y
            msg.mag_field.magnetic_field.z = mag_field_z
            #imu_msg.raw_values = str(new_data)
            pub.publish(msg)   
            #print(rospy.Time.now())

if __name__ == '__main__':
    try:
        talker()

    except rospy.ROSInterruptException:
        pass
