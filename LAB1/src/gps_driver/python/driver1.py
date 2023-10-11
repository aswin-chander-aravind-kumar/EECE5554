#!/usr/bin/env python3
# -- coding: utf-8 --

import rospy
import serial
import utm
from std_msgs.msg import Header
from gps_driver.msg import gps_msg

if _name_ == '_main_':
    SENSOR_NAME = 'gps'
    rospy.init_node('gps_node', anonymous=True)
    
    # serial_port = rospy.get_param('~port', '/dev/ttyUSB0')
    serial_port = rospy.get_param('~port', '/dev/pts/4')
    serial_baud = rospy.get_param('~baudrate', 4800)
    
    
    try:
        port = serial.Serial(serial_port, serial_baud, timeout=3.)
        gps_pub = rospy.Publisher('gps_driver_data', gps_msg, queue_size=10)
        gps_msg_fields = gps_msg()
        
        while not rospy.is_shutdown():
            line = port.readline()
            print(line)
            
            
            if line:
                # Decode the received line as a UTF-8 string
                line_str = line.decode("utf-8").strip()
                
                # Check if the line contains the '$GPGGA' NMEA sentence
                if '$GPGGA' in line_str:
                    gps_data = line_str.split(",")
                    
                    # Extract latitude, longitude, and other relevant GPS data
                    lat_dec = float(gps_data[2]) / 100.0
                    lat_dec += (float(gps_data[2]) - (int(lat_dec) * 100)) / 60.0
                    lat_dec *= 1 if gps_data[3] == 'N' else -1
                    
                    lon_dec = float(gps_data[4]) / 100.0
                    lon_dec += (float(gps_data[4]) - (int(lon_dec) * 100)) / 60.0
                    lon_dec *= 1 if gps_data[5] == 'E' else -1
                    
                    utm_latlon = utm.from_latlon(lat_dec, lon_dec)
                    
                    #Converting UTC to secs and nsecs
                    utc = gps_data[1]
                    utc_hrs = utc[:2]
                    utc_mint = utc[2:4]
                    utc_sec = utc[4:]
                    utc_secs = float(utc_hrs)*3600 + float(utc_mint)*60 + float(utc_sec)
                    utc_nsecs = int((utc_secs * (10*9)) % (10*9))

                    # Extract and set the timestamp
                    time_str = gps_data[1]
                    time_sec = float(time_str[:2]) * 3600 + float(time_str[2:4]) * 60 + float(time_str[4:])
                    gps_msg_fields.Header.stamp.secs = int(time_sec)

                    # Create a ROS message for GPS data
                    gps_msg_fields.Header.frame_id = 'GPS1_Frame'
                    gps_msg_fields.Header.stamp.secs = int(utc_secs)
                    gps_msg_fields.Header.stamp.nsecs = int(utc_nsecs)

                    gps_msg_fields = gps_msg()
                    gps_msg_fields.Latitude = lat_dec
                    gps_msg_fields.Longitude = lon_dec
                    gps_msg_fields.Altitude = float(gps_data[9])
                    gps_msg_fields.UTM_northing = float(utm_latlon[0])
                    gps_msg_fields.UTM_easting = float(utm_latlon[1])
                    gps_msg_fields.Zone = int(utm_latlon[2])
                    gps_msg_fields.Letter = utm_latlon[3]
                    gps_msg_fields.HDOP = float(gps_data[8])
                    gps_msg_fields.UTC = gps_data[1]
                                                     
                    gps_pub.publish(gps_msg_fields)
    except rospy.ROSInterruptException:
		    port.close()
