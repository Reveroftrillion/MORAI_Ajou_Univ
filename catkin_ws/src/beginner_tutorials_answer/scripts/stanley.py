#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy, os
import numpy as np
from math import cos,sin,pi,sqrt,pow,atan2
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry,Path
from morai_msgs.msg import CtrlCmd, EgoVehicleStatus, GetTrafficLightStatus, ObjectStatusList
from tf.transformations import euler_from_quaternion


class stanly_controller :
    def __init__(self):
        #subscribe and publish
        rospy.init_node('stanly_controller', anonymous=True)
        rospy.Subscriber("lattice_path", Path, self.path_callback)
        rospy.Subscriber("odom", Odometry, self.odom_callback)
        rospy.Subscriber("Ego_topic", EgoVehicleStatus, self.status_callback)
        rospy.Subscriber("global_path", Path, self.global_path_callback)
        rospy.Subscriber("GetTrafficLightStatus", GetTrafficLightStatus, self.trafficlight_callback)
        rospy.Subscriber("Object_topic", ObjectStatusList, self.object_callback)
        self.ctrl_cmd_pub = rospy.Publisher('ctrl_cmd',CtrlCmd, queue_size=1)
        self.ctrl_cmd_msg = CtrlCmd()
        self.ctrl_cmd_msg.longlCmdType = 1
        self.is_path = False
        self.is_odom = False
        self.is_status = False
        self.is_global_path = False
        self.is_traffic = False
        self.is_object = False
        self.is_close = False
        self.ped_thresh = 0.1
        self.forward_point = Point()
        self.current_postion = Point()
        self.target_vel = 38.0
        self.current_vel = 0.0
        self.traffic_index = ""
        self.traffic_status = 0
        self.is_look_forward_point = False
        self.vehicle_length = 3
        self.k = 0.9 #stanley constant
        self.v_t = 1.2 #vel constant to get crosstrack error
        self.prev_steering_angle = 0
        self.pid = pidControl()
        self.vel_planning = velocityPlanning(self.target_vel/3.6, 0.15)
        self.mode = 0
        self.stop = False
        self.first_traffic = "C119BS010046"
        self.second_traffic = "C119BS010021"
        while True:
            if self.is_global_path == True:
                self.velocity_list = self.vel_planning.curvedBaseVelocity(self.global_path, 50)
                break
            else:
                rospy.loginfo('Waiting global path data')

        rate = rospy.Rate(15) # 15hz
        while not rospy.is_shutdown():
            if self.is_path ==True and self.is_odom==True and self.is_status and self.is_traffic:
                if not self.is_close:
                    self.current_waypoint = self.get_current_waypoint(self.status_msg,self.global_path)

                    if self.current_postion.y>1322.0:
                        self.target_vel = 38.0
                    else:
                        self.target_vel = self.velocity_list[self.current_waypoint]*3.6

                    vehicle_position=self.current_postion
                    self.is_look_forward_point= False
                    translation=[vehicle_position.x, vehicle_position.y]
                    #translation matrix global to local(vehicle)
                    t=np.array([
                            [cos(self.vehicle_yaw), -sin(self.vehicle_yaw),translation[0]],
                            [sin(self.vehicle_yaw),cos(self.vehicle_yaw),translation[1]],
                            [0                    ,0                    ,1            ]])
                    det_t=np.array([
                        [t[0][0],t[1][0],-(t[0][0]*translation[0]+t[1][0]*translation[1])],
                        [t[0][1],t[1][1],-(t[0][1]*translation[0]+t[1][1]*translation[1])],
                        [0      ,0      ,1                                               ]])
                    temp = np.zeros((2,2)) #for save local point of distant minimum path point
                    dis_min = 10000
                    j = 0
                    #roop all path to get distance minimun path point from vehicle
                    for num,i in enumerate(self.path.poses) :
                        path_point=i.pose.position
                        global_path_point=[path_point.x,path_point.y,1]
                        local_path_point=det_t.dot(global_path_point)
                        if local_path_point[0] < 0:
                            continue
                        dis = sqrt(pow(local_path_point[0],2)+pow(local_path_point[1],2))
                        if dis <= dis_min :
                            dis_min = dis
                            j = num
                            temp[0][0] = local_path_point[0]
                            temp[0][1] = local_path_point[1]
                            temp_global = global_path_point
                            self.is_look_forward_point = True
                        #path point to get path yaw
                        if num == j + 1 :
                            temp[1][0] = local_path_point[0]
                            temp[1][1] = local_path_point[1]
                    if self.is_look_forward_point :
                        #get yaw_term through distance minimum path point
                        heading_error = atan2(temp[1][1] - temp[0][1], temp[1][0] - temp[0][0])
                        #get cross track error through distance minimum path point
                        cte = sin(self.vehicle_yaw)*(temp_global[0] - vehicle_position.x) - cos(self.vehicle_yaw)*(temp_global[1] - vehicle_position.y)
                        crosstrack_error = -atan2(self.k * cte, self.current_vel + self.v_t)

                        # get steering angle with heading_error anf crosstrack_error
                        steering_angle = heading_error + crosstrack_error
                        
                        #clip steering angle between (-40, 40) degree
                        steering_angle = np.clip(steering_angle, -2*pi/9, 2*pi/9)
                        self.ctrl_cmd_msg.steering = steering_angle

                        # == 여기 ====
                        self.mode = self.mode_check(self.current_waypoint)
                        
                        if self.mode != 0:
                            if self.mode == 1 or self.mode == 2:
                                self.target_vel = 15.0
                                self.stop = False
                            else:
                                self.target_vel = 0.0
                                self.stop = True
                        elif self.mode == 0:
                            self.stop = False

                        output = self.pid.pid(self.target_vel,self.status_msg.velocity.x*3.6)

                        if output > 0.0:
                            self.ctrl_cmd_msg.accel = output
                            self.ctrl_cmd_msg.brake = 0.0
                        elif output <=0.0:
                            self.ctrl_cmd_msg.accel = 0.0
                            self.ctrl_cmd_msg.brake = -(output*0.05)
                        if self.stop:
                            self.ctrl_cmd_msg.accel = 0.0
                            self.ctrl_cmd_msg.brake = 1.0
                        

                        os.system('clear')
                        print("-------------------------------------")
                        print(" steering (deg) = ", self.ctrl_cmd_msg.steering * 180 / pi)
                        print(f'Current_waypoint : {self.current_waypoint}')
                        print("Current mode = ", self.mode)
                        print(self.stop)
                        print("-------------------------------------")

                        # if self.current_waypoint >= 660:
                        #     self.ctrl_cmd_msg.accel = 0.0
                        #     self.ctrl_cmd_msg.brake = 0.0

                        self.ctrl_cmd_pub.publish(self.ctrl_cmd_msg)
                    else :
                        os.system('clear')
                        print("can't find local_forward_point")
                        self.ctrl_cmd_msg.accel = 0.0
                        self.ctrl_cmd_msg.brake = 1.0
                        self.ctrl_cmd_pub.publish(self.ctrl_cmd_msg)
                else:
                    os.system('clear')
                    print("-------------------------------------")
                    print('Pedestrians are too close')
                    print("-------------------------------------")
                    self.ctrl_cmd_msg.accel = 0.0
                    self.ctrl_cmd_msg.brake = 1.0
                    self.ctrl_cmd_pub.publish(self.ctrl_cmd_msg)

            else :
                os.system('clear')
                if not self.is_path:
                    print("[1] can't subscribe '/local_path' topic...")
                if not self.is_odom:
                    print("[2] can't subscribe '/odom' topic...")  
                if not self.is_status:
                    print("[3] can't subscribe '/Ego_topic' topic")
            self.is_path = self.is_odom = False
            rate.sleep()

    def mode_check(self, way_point):
        
        if (way_point >= 190 and way_point<=231): # 첫번째 신호등 차로
            if (self.traffic_index == self.first_traffic) and (self.traffic_status != 33): # 신호등 조건 만족할때만
                if way_point >=227:

                    return 1.5 # 정지

                return 1 # 서행
            else:
                # print(self.traffic_index, '\n', self.traffic_status)

                return 0
        
        elif (way_point >= 360 and way_point<=410): # 두번째 신호등 차로
            if self.traffic_index == self.second_traffic and self.traffic_status not in (16, 48, 20):
                if way_point >=406:
                    return 2.5 # 정지
                return 2 # 서행
            else:
                return 0
            
        else: # 나머지
            return 0
    #callback function for subscribe
    def trafficlight_callback(self, msg):
        self.is_traffic = True
        self.traffic_index = msg.trafficLightIndex
        self.traffic_status = msg.trafficLightStatus

    def object_callback(self, msg):

        self.is_object = True
        self.is_close  = False                 # 매 콜백마다 먼저 리셋

        cur_x = self.current_postion.x
        cur_y = self.current_postion.y
        thr2  = self.ped_thresh ** 2           # 제곱값으로 비교 → sqrt() 생략

        for ped in msg.pedestrian_list:
            dx = ped.position.x - cur_x
            dy = ped.position.y - cur_y
            if dx*dx + dy*dy <= thr2:          # 임계거리 이내?
                self.is_close = True
                break                          # 하나라도 가까우면 끝


    def status_callback(self, msg):
        self.is_status = True
        self.current_vel = msg.velocity.x
        self.status_msg=msg
    def path_callback(self,msg):
        self.is_path=True
        self.path=msg
    def odom_callback(self,msg):
        self.is_odom=True
        odom_quaternion=(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
        _,_,self.vehicle_yaw=euler_from_quaternion(odom_quaternion)
        self.current_postion.x=msg.pose.pose.position.x
        self.current_postion.y=msg.pose.pose.position.y
    def global_path_callback(self,msg):
        self.global_path = msg
        self.is_global_path = True
    def get_current_waypoint(self,ego_status,global_path):
        min_dist = float('inf')        
        currnet_waypoint = -1
        for i,pose in enumerate(global_path.poses):
            dx = ego_status.position.x - pose.pose.position.x
            dy = ego_status.position.y - pose.pose.position.y

            dist = sqrt(pow(dx,2)+pow(dy,2))
            if min_dist > dist :
                min_dist = dist
                currnet_waypoint = i
        return currnet_waypoint
    
class pidControl:
    def __init__(self):
        self.p_gain = 0.52
        self.i_gain = 0.00
        self.d_gain = 0.01
        self.prev_error = 0
        self.i_control = 0
        self.controlTime = 0.02

    def pid(self,target_vel, current_vel):
        error = target_vel - current_vel

        #TODO: (5) PID 제어 생성
        p_control = self.p_gain * error
        self.i_control += self.i_gain * error * self.controlTime
        d_control = self.d_gain * (error-self.prev_error) / self.controlTime

        output = p_control + self.i_control + d_control
        self.prev_error = error

        return output

class velocityPlanning:
    def __init__ (self,car_max_speed, road_friciton):
        self.car_max_speed = car_max_speed
        self.road_friction = road_friciton
        self.SAFETY_GAIN = 1.2

    def curvedBaseVelocity(self, gloabl_path, point_num):
        out_vel_plan = []

        for i in range(0,point_num):
            out_vel_plan.append(self.car_max_speed)

        for i in range(point_num, len(gloabl_path.poses) - point_num):
            x_list = []
            y_list = []
            for box in range(-point_num, point_num):
                x = gloabl_path.poses[i+box].pose.position.x
                y = gloabl_path.poses[i+box].pose.position.y
                x_list.append([-2*x, -2*y ,1])
                y_list.append((-x*x) - (y*y))

            #TODO: (6) 도로의 곡률 계산
            x_matrix = np.array(x_list)
            y_matrix = np.array(y_list)
            x_trans = x_matrix.T

            a_matrix = np.linalg.inv(x_trans.dot(x_matrix)).dot(x_trans).dot(y_matrix)
            a = a_matrix[0]
            b = a_matrix[1]
            c = a_matrix[2]
            r = sqrt(a*a+b*b-c)

            #TODO: (7) 곡률 기반 속도 계획
            v_max = sqrt(r*9.8*self.road_friction*self.SAFETY_GAIN)

            if v_max > self.car_max_speed:
                v_max = self.car_max_speed
            out_vel_plan.append(v_max)

        for i in range(len(gloabl_path.poses) - point_num, len(gloabl_path.poses)-10):
            out_vel_plan.append(30)

        for i in range(len(gloabl_path.poses) - 10, len(gloabl_path.poses)):
            out_vel_plan.append(0)

        return out_vel_plan
    

if __name__ == '__main__':
    try:
        test_track=stanly_controller()
    except rospy.ROSInterruptException:
        pass