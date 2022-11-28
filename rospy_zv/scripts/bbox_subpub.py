#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
import cv2
import sys
import numpy
from cv_bridge import CvBridge
from darknet_ros_msgs.msg import BoundingBoxes
from darknet_ros_msgs.msg import BoundingBox 
from std_msgs.msg import Int32
# from sensor_msgs.msg import Image

pub_1 = rospy.Publisher('max_bbox', BoundingBox, queue_size=10)
pub_2 = rospy.Publisher('num_person', Int32, queue_size=10)


# rate = rospy.Rate(30)
# pub_msg = Int32()

def callback(data):
    # initalize
    rate = rospy.Rate(20) # pub rate
    # find max bbox
    bboxes = data.bounding_boxes
    # print(bboxes)
    print("=====start=====")
    if len(bboxes) == 0: # 아무 물체도 검출되지 않으면
        print("nothing detected")
        pub_2.publish(0) # num_person = 0 publish
    
    else:
        area = []
        bbox = []
        # print("num object",len(bboxes))
        for i in range(len(bboxes)):
            if bboxes[i].id == 0: # objet class가 person일 경우
                area.append((bboxes[i].xmax-bboxes[i].xmin)*(bboxes[i].ymax-bboxes[i].ymin)) # bbox의 면적 계산, area 리스트에 해당 object 추가.
                bbox.append(bboxes[i]) # bbox 리스트에 해당 object 추가

        if(len(bbox) == 0): # 물체중 사람이 검출되지 않으면
            print("no person detected")
            pub_2.publish(0) # num_person = 0 publish

        elif(len(bbox) == 1): # only one person detected
            print("only one person detected")
            print(bbox[0])
            pub_1.publish(bbox[0])
            pub_2.publish(1)
        
        else: # bbox 리스트의 길이가 1보다 크면 (=사람이 2명 이상 검출됐으면) 
            # std = numpy.std(area)
            # print("std:", std)
            print("several people detected")
            if sorted(area)[-1] > sorted(area)[-2]*1.4: # biggest bbox 1.4 times bigger than 2nd biggest bbox
                print("select biggest bbox")
                max_idx = area.index(max(area)) # max area index 찾고
                target_bbox = bbox[max_idx] # 해당 bbox 찾고
                print("num person", len(bbox))
                print("max person", target_bbox)
                pub_1.publish(target_bbox) # max bbox publish
                pub_2.publish(len(bbox)) # num person publish
            else:
                # select bbox closest to center(x:320)
                print("select center closest bbox")
                target_bbox = bbox[0]
                center_dist = abs(320 - (target_bbox.xmax - target_bbox.xmin)/2)
                for box in bbox:
                    new_center_dist = abs(320 - (box.xmax - box.xmin)/2)
                    if new_center_dist < center_dist:
                        target_bbox = box
                print("num person", len(bbox))
                print("closest person", target_bbox)
                pub_1.publish(target_bbox) # closest bbox publish
                pub_2.publish(len(bbox)) # num person publish

    # img processing
    '''
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(sensor_msgs/Image, desired_encoding='passthrough')
    cv2.imshow('test', frame)
    bbox_img = cv_image[target_bbox.ymin: target_bbox.ymax, target_bbox.xmin: target_bbox.xmax]
    # print(bbox_img[0])
    cv2.imshow('test', bbox_img)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        sys.exit(0)
    '''

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()


