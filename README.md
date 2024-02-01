# Robotic Perception and Movement

I worked on different lab projects, learning a lot about how robots percieve and move. The hands-on experiences gave me a practical understanding of how the sensors work, intergration of the sensors, and expanded my knowledge in the exciting world of robotics.

### Hardware Used: GPS based GNSS puck, RTK GPS, VectorNav IMU, Lidar,and Cameras
### Softwares Used: Linux, ROS, Github, Matlab,and Python
### Skills Acquired : Statistical Analysis, Real-Time Data Processing, Device Driver Creation, Data Visualization, Parameter Identification, Image Mosiacing, Corner Feature Identification, Sensor Fusion,and Hardware Calibration.

## 1. Lab 0 : Establishing ROS and Linux: Installation and Configuration 

I gained skills in Ubuntu's command line, performing tasks like creating directories and files, and pushing files to a Git repository. The focus extended to ROS basics, where I learned about core systems such as packaging, build systems, messaging, CLI and GUI tools. I gained hands-on experience in creating ROS packages, nodes, topics, services, and parameters, as well as writing and examining simple Python-based ROS nodes for publishing and subscribing.

## 2. Lab 1: Capturing, Disseminating, and Evaluating Geospatial Information

In this project, I explored fundamental concepts in perception and movement, employing a GPS based GNSS receiver to collect and convert latitude and longitude data into UTM coordinates. Through Python programming, I defined custom ROS messages, published them with ROS nodes, and preserved the data in .bag files. The project extends to statistical analysis, where I applied appropriate python tools and discussed results, fostering proficiency in GPS-based GNSS puck manipulation. Upon implementation, I  gained practical skills in real-time data processing, message definition, and statistical analysis.

## 3. Lab 2: Advanced RTK GPS Analysis: Setup and Data Acquisition

In this project, I delved into the details of Real-Time Kinematic (RTK) GPS, mastering its high-level principles and discerning setup variations compared to conventional GPS. I personally modified the driver to 'GNGGA' NMEA strings, incorporating GNSS fix quality for robust data analysis. Tasked with hardware setup, I collected four diverse datasets, ranging from clear environments to challenging scenarios with occlusion and reflections. The acquired insights empowered me to apply analytical tools, ensuring accurate plotting and deviation estimation for an understanding of RTK system performance. 

## 4. Lab 3: Inertial Measurement Unite: Noise Assessment and Performance Characterization

I worked on the project to understand the sensor noise and the process of selecting Inertial Measurement Unit (IMU) sensors for diverse robotic applications. My focus was in crafting a device driver for the VectorNav IMU, facilitating data collection on rotation, acceleration, magnetometer, and rotational rate, followed by a comprehensive analysis using Allan variance plots. Upon completion, I gained proficiency in device driver creation, parameter identification,and environmental noise sources.

## 5. Lab 4: Multi Sensor Integration (GPS and IMU) for Robust Robotic Navigation

The Project objective was to build a navigation stack utilizing GPS and IMU sensors, emphasizing multi-senor integration for data accuracy and collection. Data acquisition involves a circular motion dataset and a Boston tour dataset collected from an autonomous vehicle, adhering to safety protocols. The analysis of the collected data includes magnetometer calibration, sensor fusion for yaw angle, estimation of forward velocity, and dead reckoning with IMU. Plots illustrating corrections and comparisons between IMU and GPS measurements provide insights into sensor performance and potential enhancements. The hands-on experience involved Sensor fusion technique, writing device drivers, performing magnetometer calibration, and analyzing sensor noise parameters.

## 6. Lab 5: Photomosaic Integration

Throughout the project, I worked in the realm of calibrated cameras, leveraging my camera phone for the art of photomosaicing. Grasping the understanding of the Harris corner detector, I refined my skill in recognizing corner features within images. Engaging in conversations about image mosaic algorithms such as ICP, I practically applied these techniques to weave together mural photographs seamlessly. This hands-on experience not only enhanced my technical proficiency but also provided valuable insights into assessing scenes for optimal outcomes in image mosaicing. 

