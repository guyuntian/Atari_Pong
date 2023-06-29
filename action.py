import numpy as np
from elements import R3bot
import random

class Action():
    def __init__(self, obs):
        self.size1, self.size2 = 1200, 500
        self.player, self.ball_pos, self.ball_v = obs
        self.L1, self.L2, self.L3 = self.player.L1, self.player.L2, self.player.L3
        self.maxtry = 5

    def get_hit_position(self):
        ball_x, ball_y = self.ball_pos
        ball_vx, ball_vy = self.ball_v
        t = 0
        while ball_x > 0:
            ball_x += ball_vx
            ball_y += ball_vy
            if ball_y <= 0:
                ball_vy = -ball_vy
            elif ball_y >= self.size2:
                ball_vy = -ball_vy
            t += 1
        return ball_x, ball_y, np.arctan(ball_vy/ball_vx), t
    
    def get_angle(self, x, y, angle):
        tmp1 = x - self.L3 * np.cos(angle)
        tmp2 = y - self.L3 * np.sin(angle)
        tmp3 = tmp1**2 + tmp2**2 + self.L1 ** 2 - self.L2 ** 2
        A = 2 * tmp2 * self.L1
        B = 2 * tmp1 * self.L1
        C = tmp3 / np.sqrt(A**2 + B**2)
        if A == 0:
            phi = np.pi / 2
            if B < 0:
                phi = -phi
        else:
            phi = np.arctan(B/A)
        if abs(C) > 1:
            self.maxtry -= 1
            if self.maxtry == 0:
                return 0, 0, 0
            return self.get_angle(x, y, random.random()*np.pi*2)
        theta1 = np.arcsin(C) - phi
        if abs((tmp1 - self.L1 * np.cos(theta1))/self.L2) > 1:
            self.maxtry -= 1
            if self.maxtry == 0:
                return 0, 0, 0
            return self.get_angle(x, y, random.random()*np.pi*2)
        theta2 = np.arccos((tmp1 - self.L1 * np.cos(theta1))/self.L2) - theta1
        if abs(y - self.L3 * np.sin(angle) - self.L2 * np.sin(theta1 + theta2) - self.L1 * np.sin(theta1)) > 1e-3:
            theta2 = -np.arccos((tmp1 - self.L1 * np.cos(theta1))/self.L2) - theta1
        theta3 = angle - theta1 - theta2
        return theta1, theta2, theta3
    
    def get_velocity(self, theta1, theta2, theta3):
        return (theta1 - self.player.theta_1) / 10, (theta2 - self.player.theta_2) / 10, (theta3 - self.player.theta_3) / 10
    
    def regularize(self, theta):
        while abs(theta) > 0.1:
            return theta / abs(theta) * 0.1
        return theta

    def get_action(self):
        if self.ball_v[0] >= 0:
            return 0, 0, 0
        
        ball_x, ball_y, angle, _ = self.get_hit_position()
        if abs(ball_y - self.player.basepos[1]) > self.L1 + self.L2 + self.L3:
            return 0, 0, 0
        
        angle1, angle2, angle3 = self.get_angle(ball_x - self.player.basepos[0], ball_y - self.player.basepos[1], angle)
        angle1, angle2, angle3 = self.get_velocity(angle1, angle2, angle3)
        return self.regularize(angle1), self.regularize(angle2), self.regularize(angle3)
    
    def get_sota_action(self):
        if self.ball_v[0] >= 0:
            return 0, 0, 0
        if random.random() > 0.5:
            target_x, target_y = self.size1, 0
        else:
            target_x, target_y = self.size1, self.size2
        ball_x, ball_y, angle, t = self.get_hit_position()
        expected_angle = np.arctan((target_y - ball_y) / (target_x - ball_x))
        delta = 1
        if t < 10:
            angle1, angle2, angle3 = self.get_angle(ball_x - self.player.basepos[0] + delta * np.cos(expected_angle), ball_y - self.player.basepos[1] + delta * np.sin(expected_angle), expected_angle)
        else:
            angle1, angle2, angle3 = self.get_angle(ball_x - self.player.basepos[0], ball_y - self.player.basepos[1], expected_angle)
        angle1, angle2, angle3 = self.get_velocity(angle1, angle2, angle3)
        return self.regularize(angle1), self.regularize(angle2), self.regularize(angle3)
    
        
