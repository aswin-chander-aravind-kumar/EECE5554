;; Auto-generated. Do not edit!


(when (boundp 'imu_driver::convert_to_quaternion)
  (if (not (find-package "IMU_DRIVER"))
    (make-package "IMU_DRIVER"))
  (shadow 'convert_to_quaternion (find-package "IMU_DRIVER")))
(unless (find-package "IMU_DRIVER::CONVERT_TO_QUATERNION")
  (make-package "IMU_DRIVER::CONVERT_TO_QUATERNION"))
(unless (find-package "IMU_DRIVER::CONVERT_TO_QUATERNIONREQUEST")
  (make-package "IMU_DRIVER::CONVERT_TO_QUATERNIONREQUEST"))
(unless (find-package "IMU_DRIVER::CONVERT_TO_QUATERNIONRESPONSE")
  (make-package "IMU_DRIVER::CONVERT_TO_QUATERNIONRESPONSE"))

(in-package "ROS")





(defclass imu_driver::convert_to_quaternionRequest
  :super ros::object
  :slots (_roll _pitch _yaw ))

(defmethod imu_driver::convert_to_quaternionRequest
  (:init
   (&key
    ((:roll __roll) 0.0)
    ((:pitch __pitch) 0.0)
    ((:yaw __yaw) 0.0)
    )
   (send-super :init)
   (setq _roll (float __roll))
   (setq _pitch (float __pitch))
   (setq _yaw (float __yaw))
   self)
  (:roll
   (&optional __roll)
   (if __roll (setq _roll __roll)) _roll)
  (:pitch
   (&optional __pitch)
   (if __pitch (setq _pitch __pitch)) _pitch)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:serialization-length
   ()
   (+
    ;; float64 _roll
    8
    ;; float64 _pitch
    8
    ;; float64 _yaw
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _roll
     (setq _roll (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pitch
     (setq _pitch (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yaw
     (setq _yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass imu_driver::convert_to_quaternionResponse
  :super ros::object
  :slots (_qx _qy _qz _qw ))

(defmethod imu_driver::convert_to_quaternionResponse
  (:init
   (&key
    ((:qx __qx) 0.0)
    ((:qy __qy) 0.0)
    ((:qz __qz) 0.0)
    ((:qw __qw) 0.0)
    )
   (send-super :init)
   (setq _qx (float __qx))
   (setq _qy (float __qy))
   (setq _qz (float __qz))
   (setq _qw (float __qw))
   self)
  (:qx
   (&optional __qx)
   (if __qx (setq _qx __qx)) _qx)
  (:qy
   (&optional __qy)
   (if __qy (setq _qy __qy)) _qy)
  (:qz
   (&optional __qz)
   (if __qz (setq _qz __qz)) _qz)
  (:qw
   (&optional __qw)
   (if __qw (setq _qw __qw)) _qw)
  (:serialization-length
   ()
   (+
    ;; float64 _qx
    8
    ;; float64 _qy
    8
    ;; float64 _qz
    8
    ;; float64 _qw
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _qx
       (sys::poke _qx (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _qy
       (sys::poke _qy (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _qz
       (sys::poke _qz (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _qw
       (sys::poke _qw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _qx
     (setq _qx (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _qy
     (setq _qy (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _qz
     (setq _qz (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _qw
     (setq _qw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass imu_driver::convert_to_quaternion
  :super ros::object
  :slots ())

(setf (get imu_driver::convert_to_quaternion :md5sum-) "59f14f944460f58582f2733eafd6de47")
(setf (get imu_driver::convert_to_quaternion :datatype-) "imu_driver/convert_to_quaternion")
(setf (get imu_driver::convert_to_quaternion :request) imu_driver::convert_to_quaternionRequest)
(setf (get imu_driver::convert_to_quaternion :response) imu_driver::convert_to_quaternionResponse)

(defmethod imu_driver::convert_to_quaternionRequest
  (:response () (instance imu_driver::convert_to_quaternionResponse :init)))

(setf (get imu_driver::convert_to_quaternionRequest :md5sum-) "59f14f944460f58582f2733eafd6de47")
(setf (get imu_driver::convert_to_quaternionRequest :datatype-) "imu_driver/convert_to_quaternionRequest")
(setf (get imu_driver::convert_to_quaternionRequest :definition-)
      "float64 roll
float64 pitch
float64 yaw
---
float64 qx
float64 qy
float64 qz
float64 qw

")

(setf (get imu_driver::convert_to_quaternionResponse :md5sum-) "59f14f944460f58582f2733eafd6de47")
(setf (get imu_driver::convert_to_quaternionResponse :datatype-) "imu_driver/convert_to_quaternionResponse")
(setf (get imu_driver::convert_to_quaternionResponse :definition-)
      "float64 roll
float64 pitch
float64 yaw
---
float64 qx
float64 qy
float64 qz
float64 qw

")



(provide :imu_driver/convert_to_quaternion "59f14f944460f58582f2733eafd6de47")


