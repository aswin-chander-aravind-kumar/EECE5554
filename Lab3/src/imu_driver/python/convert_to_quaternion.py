 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

from imu_driver.srv import convert_to_quaternion, convert_to_quaternionResponse 
import rospy
import numpy as np

def conversion(roll, pitch, yaw):
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)    
    return (qx, qy, qz, qw)
    
def convert_to_quaternion_1(req):
    (qx, qy, qz, qw) = conversion(req.roll, req.pitch, req.yaw)
    
    return convert_to_quaternionResponse(qx, qy, qz, qw)

def convert_to_quaternion_srv():
    rospy.init_node('convert_to_quaternion_srv')
    s = rospy.Service('convert_to_quaternion', convert_to_quaternion, convert_to_quaternion_1)
    rospy.spin()
 
if __name__ == "__main__":
    convert_to_quaternion_srv()
