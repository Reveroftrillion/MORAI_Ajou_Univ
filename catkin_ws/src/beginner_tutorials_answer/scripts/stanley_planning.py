#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, rospy, rospkg
from math import cos, sin, pi, sqrt, atan2
from geometry_msgs.msg import Point, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry, Path
from morai_msgs.msg import CtrlCmd, EgoVehicleStatus
import numpy as np
from tf.transformations import euler_from_quaternion


class stanley_controller:
    """
    Stanley + PID 종·횡방향 통합 제어 노드
    ───────────────────────────────
    * lateral : Stanley controller
    * longitudinal : 원래 파일의 속도 계획(curvedBaseVelocity) + PID
    """
    def __init__(self):
        rospy.init_node('stanley_controller', anonymous=True)

        # ───── (1) Subscribe & Publish ─────
        rospy.Subscriber("/global_path",  Path, self.global_path_callback)
        rospy.Subscriber("/lattice_path", Path, self.path_callback)   # 지역 경로
        rospy.Subscriber("/odom",         Odometry, self.odom_callback)
        rospy.Subscriber("/Ego_topic",    EgoVehicleStatus, self.status_callback)

        self.ctrl_pub = rospy.Publisher("ctrl_cmd", CtrlCmd, queue_size=1)
        self.cmd = CtrlCmd(); self.cmd.longlCmdType = 1  # Throttle control

        # ───── 상태 플래그 ─────
        self.is_path = self.is_odom = self.is_status = self.is_global = False
        self.is_look_forward_point = False

        # ───── 차량·제어 파라미터 ─────
        self.current_pos = Point()
        self.vehicle_yaw = 0.0
        self.vehicle_length = 2.6

        # Stanley 계수
        self.k   = 0.9   # CTE gain
        self.v_t = 1.0   # 저속 안정화 상수

        # 종방향 계획
        self.target_vel_kph = 20.0
        self.pid = pidControl()
        self.vel_plan = velocityPlanning(self.target_vel_kph / 3.6, 0.15)

        # 전역 경로 대기 후 속도 프로파일 계산
        while not rospy.is_shutdown() and not self.is_global:
            rospy.loginfo("Waiting /global_path ...")
            rospy.sleep(0.2)
        self.vel_list = self.vel_plan.curvedBaseVelocity(self.global_path, 50)

        # ───── 메인 루프 ─────
        rate = rospy.Rate(30)  # 30 Hz
        while not rospy.is_shutdown():
            if self.is_path and self.is_odom and self.is_status:
                # ① 목표 속도(커브 기반)
                wp_idx = self.get_current_waypoint(self.status_msg, self.global_path)
                self.target_vel_kph = self.vel_list[wp_idx] * 3.6

                # ② 횡방향 Stanley
                steer = self.calc_stanley()

                if self.is_look_forward_point:
                    self.cmd.steering = steer
                else:
                    rospy.loginfo("No forward point, steer=0")
                    self.cmd.steering = 0.0

                # ③ 종방향 PID (kph → kph)
                out = self.pid.pid(self.target_vel_kph,
                                   self.status_msg.velocity.x * 3.6)
                self.cmd.accel = max(out, 0.0)
                self.cmd.brake = -min(out + 0.2, 0.0)

                # ④ Publish & 디버깅 출력
                os.system('clear')
                print("-------------------------------------")
                print(f" steering (deg) = {self.cmd.steering * 180 / pi:7.3f}")
                print(f" target_vel(kph)= {self.target_vel_kph:7.2f}")
                print(f" accel          = {self.cmd.accel:7.3f}")
                print(f" brake          = {self.cmd.brake:7.3f}")
                print("-------------------------------------")
                self.ctrl_pub.publish(self.cmd)

                # 다음 loop에서 새 데이터 수신하도록 플래그 초기화
                self.is_path = self.is_odom = False
            else:
                os.system('clear')
                if not self.is_path:   print("[1] waiting /lattice_path ...")
                if not self.is_odom:   print("[2] waiting /odom ...")
                if not self.is_status: print("[3] waiting /Ego_topic ...")

            rate.sleep()

    # ───── 콜백 ─────
    def path_callback(self, msg):
        self.path, self.is_path = msg, True

    def odom_callback(self, msg):
        self.is_odom = True
        q = (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
             msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)
        _, _, self.vehicle_yaw = euler_from_quaternion(q)
        self.current_pos.x = msg.pose.pose.position.x
        self.current_pos.y = msg.pose.pose.position.y

    def status_callback(self, msg):
        self.status_msg, self.is_status = msg, True
        self.current_vel = msg.velocity.x  # m/s

    def global_path_callback(self, msg):
        self.global_path, self.is_global = msg, True

    # ───── 보조 함수 ─────
    def get_current_waypoint(self, ego, gpath):
        best, idx = float('inf'), -1
        ex, ey = ego.position.x, ego.position.y
        for i, p in enumerate(gpath.poses):
            dx, dy = ex - p.pose.position.x, ey - p.pose.position.y
            d = dx*dx + dy*dy
            if d < best:
                best, idx = d, i
        return idx

    # ───── Stanley Controller ─────
    def calc_stanley(self):
        self.is_look_forward_point = False
        tx, ty = self.current_pos.x, self.current_pos.y

        # 글로벌 → 차량 좌표 변환행렬의 역행렬
        t = np.array([[ cos(self.vehicle_yaw),  sin(self.vehicle_yaw), -(cos(self.vehicle_yaw)*tx + sin(self.vehicle_yaw)*ty)],
                      [-sin(self.vehicle_yaw),  cos(self.vehicle_yaw),  (sin(self.vehicle_yaw)*tx - cos(self.vehicle_yaw)*ty)],
                      [ 0,                      0,                       1]])
        # 최근접 경로점 탐색
        min_d, idx, local_near, local_next, global_near = 1e9, -1, None, None, None
        for i, pose in enumerate(self.path.poses):
            gp = pose.pose.position
            lp = t.dot([gp.x, gp.y, 1])
            if lp[0] < 0:  # 차량 뒤쪽
                continue
            d = lp[0]**2 + lp[1]**2
            if d < min_d:
                min_d, idx = d, i
                local_near = lp[:2]
                global_near = gp
                self.is_look_forward_point = True
            elif i == idx + 1:
                local_next = lp[:2]

        if not self.is_look_forward_point or local_next is None:
            return 0.0

        # Heading 오차
        heading_error = atan2(local_next[1] - local_near[1],
                              local_next[0] - local_near[0])
        # Crosstrack 오차
        cte =  sin(self.vehicle_yaw)*(global_near.x - tx) \
             - cos(self.vehicle_yaw)*(global_near.y - ty)
        cte_term = atan2(self.k * cte, self.current_vel + self.v_t)

        steer = heading_error + cte_term
        return np.clip(steer, -pi/6, pi/6)  # ±30°


# ───────────────────────────────────────────────────────────────
#           ↓↓↓ 아래 두 클래스는 원본 그대로 유지 ↓↓↓
# ───────────────────────────────────────────────────────────────
class pidControl:
    def __init__(self):
        self.p_gain, self.i_gain, self.d_gain = 0.3, 0.0, 0.03
        self.prev_err, self.i_term = 0.0, 0.0
        self.dt = 0.02  # 50 Hz
    def pid(self, target_kph, current_kph):
        err = target_kph - current_kph
        p = self.p_gain * err
        self.i_term += self.i_gain * err * self.dt
        d = self.d_gain * (err - self.prev_err) / self.dt
        self.prev_err = err
        return p + self.i_term + d


class velocityPlanning:
    def __init__(self, v_max_mps, mu):
        self.v_max = v_max_mps; self.mu = mu
    def curvedBaseVelocity(self, gpath, n):
        out = [self.v_max]*n
        for i in range(n, len(gpath.poses)-n):
            xs, ys = [], []
            for b in range(-n, n):
                p = gpath.poses[i+b].pose.position
                xs.append([-2*p.x, -2*p.y, 1])
                ys.append(-(p.x**2 + p.y**2))
            A = np.array(xs);  b = np.array(ys)
            a1, a2, a3 = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(b)
            r = sqrt(a1*a1 + a2*a2 - a3)
            vmax = min(sqrt(r * 9.8 * self.mu), self.v_max)
            out.append(vmax)
        out.extend([30/3.6]*10)  # 30 kph
        out.extend([0.0]*10)
        return out


if __name__ == '__main__':
    try:
        stanley_controller()
    except rospy.ROSInterruptException:
        pass
