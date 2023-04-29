
#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from flask import Flask, render_template, request

app = Flask(__name__)

def start_ros_node():
    rospy.init_node('web_interface')

def txt_callback(msg):
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cmd_vel', methods=['POST'])
def cmd_vel():
    cmd = request.form['cmd']
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    if cmd == 'forward':
        twist = Twist()
        twist.linear.x = 0.15
        pub.publish(twist)
    elif cmd == 'backward':
        twist = Twist()
        twist.linear.x = -0.15
        pub.publish(twist)
    elif cmd == 'left':
        twist = Twist()
        twist.angular.z = 0.1
        pub.publish(twist)
    elif cmd == 'right':
        twist = Twist()
        twist.angular.z = -0.1
        pub.publish(twist)
    elif cmd == 'stop':
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
    return 'OK'

if __name__ == '__main__':
    start_ros_node()
    rospy.Subscriber('/txt_msg', String, txt_callback)
    app.run(debug=True, threaded=True)
