#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

import rospy
import serial
import utm
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Header
from gps_driver.msg import gps_msg
import sys
import argparse


if __name__ == '__main__':
	SENSOR_NAME = 'gps'
	rospy.init_node('gps_node',anonymous = True)
	port = rospy.get_param('driver/port')
	serial_baud = rospy.get_param('~baudrate',4800)
	sampling_rate = rospy.get_param('~sampling_rate',1.0)

	port = serial.Serial(port, serial_baud, timeout=3.)

	gps_pub = rospy.Publisher('gps',gps_msg, queue_size=10)
	
	try:
		while not rospy.is_shutdown():
			line = port.readline()
			if line == '':
				rospy.logwarn("GPS: No data")
			else:
				gps_data_input = None
				line_str = line.decode("utf-8")
				print(line_str)
				if '$GPGGA' in line_str:
					gps_data_input = line_str.split(",")
				else:
					gps_data_input = None
				if gps_data_input is not None:
					if gps_data_input[3]=='N':
						if gps_data_input[2] !='':
							north_south=1
							lat_dec = (float(gps_data_input[2]))/100
							lat_dec = lat_dec + ((float(gps_data_input[2]))-(lat_dec * 100))/60
							lat_dec = north_south*lat_dec
					else:
						if gps_data_input[2] !='':
							north_south=-1
							lat_dec = (float(gps_data_input[2]))/100
							lat_dec = lat_dec + ((float(gps_data_input[2]))-(lat_dec * 100))/60
							lat_dec = north_south*lat_dec
					if gps_data_input[5]=='E':
						if gps_data_input[4] !='':
							east_west=1
							lon_dec = (float(gps_data_input[4]))/100
							lon_dec = lon_dec + (float((gps_data_input[4]))-(lon_dec * 100))/60
							lon_dec = east_west*lon_dec
					else:
						if gps_data_input[4] !='':
							east_west=-1
							lon_dec = (float(gps_data_input[4]))/100
							lon_dec = lon_dec + (float((gps_data_input[4]))-(lon_dec * 100))/60
							lon_dec = east_west*lon_dec
					
					UTM_conv = utm.from_latlon(lat_dec, lon_dec)
					gps_msg_fields = gps_msg()
				
					
					gps_msg_fields.Latitude = lat_dec
					gps_msg_fields.Longitude = lon_dec
					gps_msg_fields.HDOP = float(gps_data_input[8])
					gps_msg_fields.Altitude = float(gps_data_input[9])
					gps_msg_fields.UTM_northing = UTM_conv[1]
					gps_msg_fields.UTM_easting = UTM_conv[0]
					gps_msg_fields.Zone = UTM_conv[2]
					gps_msg_fields.Letter = UTM_conv[3]
					time = gps_data_input[1]
					time_sec=(float(time[:2])*3600)+(float(time[2:4])*60)+float(time[4:6])
					gps_msg_fields.Header.stamp.secs = int(time_sec)
					time_nsec = float(time[6:])*10e9
					gps_msg_fields.Header.stamp.nsecs = int(time_nsec)
					
					gps_msg_fields.Header.frame_id = 'GPS1_Frame'
					
					gps_pub.publish(gps_msg_fields)



	except rospy.ROSInterruptException:
		port.close()
	except serial.serialutil.SerialException:
		rospy.loginfo("Shutting down GPS Driver node ...")
