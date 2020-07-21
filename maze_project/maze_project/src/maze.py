#! /usr/bin/env python

import rospy
from threading import Thread, Lock
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from apriltag_ros.msg import AprilTagDetectionArray
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class MazeSolver:

    
    def __init__(self):
	"""Inizializzazione del nodo e delle proprieta del robot"""
        rospy.init_node('MazeSolverNode')
        self.rate = rospy.Rate(10)
        rospy.Subscriber('/odom', Odometry, self.get_rotation)
        rospy.Subscriber('/tag_detections', AprilTagDetectionArray, self.detection_callback)

        self.velPub = rospy.Publisher('/cmd_vel', Twist, queue_size = 5)
	
	#il robot parte con yaw = 3.14
	self.yawToUpdate = 3.14
    self.vel = Twist()
    self.odom = None
    self.detection = None
    self.angle = 90 
	self.mutex = Lock()

    def detection_callback(self, detection_msg):
	"""Metodo di callback per la detection degli april tag"""
  		self.detection = detection_msg.detections
        
    def startSolver(self):
	"""Metodo che si occupa di guidare il robot"""
        rospy.loginfo("start Maze Solver Node")
        while not rospy.is_shutdown():
            if(self.odom and self.mutex.locked() == False): 
                self.vel.linear.x = 0.2
                self.vel.angular.z = 0.0
                self.velPub.publish(self.vel)
			if(self.detection):
		        if (len(self.detection) > 0 and self.detection[0].pose.pose.pose.position.z < 1.2):
		            self.vel.linear.x = 0.0
		            self.vel.angular.z = 0.0
		            self.velPub.publish(self.vel)
			    	rospy.loginfo("Detections: " + str(self.detection))
			    if (self.detection[0].id[0] == 1):
			        self.rotate_angle(self.angle)
			    elif(self.detection[0].id[0] == 0):
			       	self.rotate_angle(-self.angle)
			    else:
					rospy.signal_shutdown("Fuga dal labirinto completata")
	    	self.rate.sleep()
        rospy.spin()

    def get_rotation (self, msg):
	"""Metodo di callback per l'odometria"""
     	self.odom = msg
		orientation_q = self.odom.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(self.roll, self.pitch, self.yaw) = euler_from_quaternion (orientation_list)

    def rotate_angle(self,angle):
	"""Metodo incaricato della rotazione del robot"""
		self.mutex.acquire()
		diff = 0 
    	try:
			angle_rad = angle*3.14/180
			rotation_angle = self.yawToUpdate - angle_rad
			rospy.loginfo("*******Rotation_angle: " + str(rotation_angle))
			diff = rotation_angle - self.yaw
		   	while(abs(diff) >= 0.008): 
	    		self.vel.angular.z = rotation_angle - self.yaw
	    		self.velPub.publish(self.vel)
	    		diff = rotation_angle - self.yaw 
			self.vel.angular.z = 0.0
			self.velPub.publish(self.vel)
		finally:
        	self.yawToUpdate = rotation_angle
        	self.mutex.release()


if __name__ == "__main__":
    maze_solver = MazeSolver()
    maze_solver.startSolver()
