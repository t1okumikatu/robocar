#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, select, tty, termios
import rospy
from std_msgs.msg import String

if __name__ == '__main__':

  #KeysトピックにString型のメッセージを毎秒一回送る
  key_pub = rospy.Publisher('keys', String, queue_size=1)
  #keyboard_driverノード作成
  rospy.init_node("keyboard_driver")
  rate = rospy.Rate(100)

  old_attr = termios.tcgetattr(sys.stdin)
  tty.setcbreak(sys.stdin.fileno())

  print "Publishing [z], [x] or [a]. Press Ctrl-C to exit..."

  while not rospy.is_shutdown():

    if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
      key_pub.publish(sys.stdin.read(1))
    rate.sleep()

  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
