#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
import numpy as np
#import cv2
import time
from std_msgs.msg import String
from a_star import AStar
#a_star = AStar()

key_mapping = { 'w': [80, 80], 'x': [-80, -80], 'a': [-60, 60], 'd': [60, -60], 's': [0, 0] }

def keys_mtr(kmsg):
  a_star = AStar()
  if len(kmsg.data) == 0 or not key_mapping.has_key(kmsg.data[0]):
    return
  mtrs = key_mapping[kmsg.data[0]]
  mtrs = np.array(mtrs, dtype='int16')
  mleft = mtrs[0]
  mright = mtrs[1]
#  print(mleft, mleft.dtype)
#  print(mright, mright.dtype)
  a_star.motors(mleft,mright)
  time.sleep(0.1)

if __name__ == '__main__':
#  a_star = AStar()
  rospy.init_node('keys_mtrctrl')
  rospy.Subscriber('keys', String, keys_mtr)
  rospy.spin()

