#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import numpy as np
import math

def go_to(x, y, theta=0):
        client = None
        client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        client.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        theta = euler_to_quaternion(theta)

        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.position.z = 0
        goal.target_pose.pose.orientation.w = theta

        client.send_goal(goal)
        wait = client.wait_for_result()

        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            rospy.loginfo("Done")
            return client.get_result()

def euler_to_quaternion(yaw):
    pitch = 0
    roll = 0
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    return qw

if __name__ == "__main__":
    try:
        rospy.init_node("test_scenario")
        rospy.loginfo("SimpleNavigationGoals Initialization")
        
        rospy.loginfo("Initializations done")

        # What to do if shut down (e.g. ctrl + C or failure)
        #rospy.on_shutdown("done")

        while True:
            rospy.loginfo("Go to -2, 0, 0")
            if not (go_to(-1.3, 5, 45)):
                break
            '''
            rospy.loginfo("Go to 0.5, 0.5, PI/2")
            if not (go_to(0.5, 0.5, math.pi/2)):
                break
                rospy.loginfo("Go to 1.6, -1.6, 0")
            if not (go_to(1.6, -1.6, 0)):
                break
            '''
        rospy.spin()
    except rospy.ROSInterruptException:
        print("Exception")

    rospy.loginfo("test terminated.")