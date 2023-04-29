#!/usr/bin/env python3

import rospy
import os
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time

# This node will start localization process when it receives the message 'Start' on topic 'self_localize'
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

def callback(data):
    
    rospy.loginfo("Starting self localization")
    rospy.sleep(1)

    # This rosservice distributes the initial probable robot locations on the whole map evenly 
    os.system("rosservice call /global_localization")

    # Start moving procedure after giving 1 second for the rosserive execution  
    rospy.sleep(1)

    cmd = Twist()

    print("Spinning")

    t1 = time.time()
    tNow = t1
    duration = 3.14 / 6.28
    while (tNow-t1) <duration*2:
        tNow=time.time()
        cmd.angular.z = 0.7
        pub.publish(cmd)
    print("------------------")
    rospy.sleep(2)


    print("Move forward")    
    t1 = time.time()
    tNow = t1
    while tNow-t1<5:
        tNow=time.time()
        cmd.angular.z = 0
        cmd.linear.x = 0.05
        pub.publish(cmd)
    print("------------------")
    rospy.sleep(2)

    print("Move back to start")
    t1 = time.time()
    tNow = t1
    while tNow-t1<5:
        tNow=time.time()
        cmd.linear.x = -0.05
        pub.publish(cmd)
    
    
    rospy.sleep(2)
    cmd.linear.x = 0
    cmd.angular.z = 0
    pub.publish(cmd)
    rospy.loginfo("Localization complete")

    # This terminates the ros node
    rospy.signal_shutdown("finished localization")

    
def listener():
    rospy.init_node('Localizer', anonymous=True)
    rospy.Subscriber("self_localize", String, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
