#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from a_star import AStar

class Follower:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
#    cv2.namedWindow("window", 1)
    self.image_sub = rospy.Subscriber('cv_camera/image_raw', 
                                      Image, self.image_callback)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel',
                                       Twist, queue_size=1)
    self.twist = Twist()
    self.a_star = AStar()
  def image_callback(self, msg):
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_black = numpy.array([  0,   0,   0])
    upper_black = numpy.array([120, 100,  80])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    
    h, w, d = image.shape
    search_top = 3*h/4
    search_bot = 3*h/4 + 20
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    M = cv2.moments(mask)
    if M['m00'] > 0:
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00'])
#      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
      cv2.circle(mask, (cx, cy), 20, (0,0,255), -1)
      # BEGIN CONTROL
      err = cx - w/2
      self.twist.linear.x = 0.2
      self.twist.angular.z = -float(err) / 100
      self.cmd_vel_pub.publish(self.twist)
      self.a_star.motors(int(40+0.3*err), int(40-0.3*err))
      # END CONTROL
#    cv2.imshow("window", mask)
#    cv2.waitKey(3)

rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL
