#!/usr/bin/env python3
import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Range
from vision_msg.msg import YoloBoundingBox
from sensor_msgs.msg import Image as msg_Image
from cv_bridge import CvBridge, CvBridgeError

# ------------------------------arduino

import serial
import time
import sys
import signal
from time import sleep
from PyMata.pymata import PyMata

COM_PORT = '/dev/ttyACM0'
BAUD_RATES = 9600

class Arduino:
    def __init__(self):
        self.BOARD_LED = 7  # led
        self.BEEPER = 3  # beep
        # Lcd
        self.LCD_data = serial.Serial(COM_PORT, BAUD_RATES)

    def turnon(self):
        self.LCD_data.write(b'LCD_SHOW_a\n')  # 訊息必須是位元組類型
        sleep(0.5)              # 暫停0.5秒，再執行底下接收回應訊息的迴圈

    def turnoff(self):
        self.LCD_data.write(b'LCD_SHOW_b\n')  # 訊息必須是位元組類型
        sleep(0.5)              # 暫停0.5秒，再執行底下接收回應訊息的迴圈

# ------------------------------arduino


# depth from camera to replace ultrasonic
camera_depth = 0
yolo_bbox_x = 0
yolo_bbox_y = 0


def yolo_callback(data):  # detect person
    #global person
    #person = data.object_name
    # record camera depth
    global yolo_bbox_x, yolo_bbox_y
    yolo_bbox_x = data.x + data.width / 2  # uint16 = int
    yolo_bbox_y = data.y + data.height / 2  # uint16 = int
    # rospy.loginfo("yolo_width: %d", yolo_bbox_x)
    # rospy.loginfo("yolo_height: %d", yolo_bbox_y)
    # Arduino part
    if data.object_name == 'person' and camera_depth <= 2000:  # 2000(mm)
        arduino.turnoff()
        rospy.loginfo("Detect person: led turnoff/ beeper off/ LCD show")
    else:
        arduino.turnon()
        rospy.loginfo("No person: led turnon/ beeper on/ LCD show")


def imageDepthCallback(data):
    global camera_depth
    try:
        # Convert the depth image using the default passthrough encoding
        cv_image = bridge.imgmsg_to_cv2(
            data, desired_encoding="passthrough")  # 1280 × 720 # uint16
        # 1280 × 720 # /camera/depth/image_rect_raw
        # 1920 × 1080 # /camera/aligned_depth_to_color/image_raw
        camera_depth = cv_image[int(yolo_bbox_y), int(yolo_bbox_x)]
        # rospy.loginfo("center: (%d,%d)", yolo_bbox_y, yolo_bbox_x)
        rospy.loginfo("Depth: %f (mm)",
                      cv_image[int(yolo_bbox_y), int(yolo_bbox_x)])
    except CvBridgeError as e:
        rospy.loginfo(e)


#def detect_callback1(data):  # ultrasonic1
    #ultrasonic_range1 = data.range
    #rospy.loginfo("Get range_1: %f", ultrasonic_range1)
    #if person == 'person' and ultrasonic_range1 <= 200:
        #arduino.turnoff()
    #else:
        #arduino.turnon()


#def detect_callback2(data):  # ultrasonic2
    #ultrasonic_range2 = data.range
    #rospy.loginfo("Get range_2: %f", ultrasonic_range2)
    #if person == 'person' and ultrasonic_range2 <= 200:
        #arduino.turnoff()
    #else:
        #arduino.turnon()


#def detect_callback3(data):  # ultrasonic3
    #ultrasonic_range3 = data.range
    #rospy.loginfo("Get range_3: %f", ultrasonic_range3)
    #if person == 'person' and ultrasonic_range3 <= 200:
        #arduino.turnoff()
    #else:
        #arduino.turnon()


def listener():
    rospy.init_node('sub_depth_and_yolo', anonymous=True)
    rospy.Subscriber('yolo/person/box', YoloBoundingBox,
                     yolo_callback, queue_size=1)
    rospy.Subscriber('/camera/aligned_depth_to_color/image_raw',
                     msg_Image, imageDepthCallback, queue_size=1)
    # /camera/aligned_depth_to_color/image_raw: 將深度圖(depth)align成彩色圖(color)
    #rospy.Subscriber('/range_sensor/sonar_1', Range, detect_callback1 , queue_size=1)
    #rospy.Subscriber('/range_sensor/sonar_2', Range, detect_callback2 , queue_size=1)
    #rospy.Subscriber('/range_sensor/sonar_3', Range, detect_callback3 , queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    bridge = CvBridge()
    arduino = Arduino()
    listener()

