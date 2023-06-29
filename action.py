import numpy as np
from elements import R3bot

class Action():
    def __init__(self, obs):
        self.player, self.ball_pos, self.ball_v = obs
        self.L1, self.L2, self.L3 = self.player.L1, self.player.L2, self.player.L3

    def get_hit_position(self):
        size1, size2 = 800, 600
        ball_x, ball_y = self.ball_pos
        ball_vx, ball_vy = self.ball_v
        while ball_x > 0:
            ball_x += ball_vx
            ball_y += ball_vy
            if ball_y <= 0:
                ball_vy = -ball_vy
            elif ball_y >= size2:
                ball_vy = -ball_vy
        return ball_x, ball_y, np.arctan(ball_vy/ball_vx)
    
    def get_angle(self, x, y, angle):
        tmp1 = x - self.L3 * np.cos(angle)
        tmp2 = y - self.L3 * np.sin(angle)
        tmp3 = tmp1**2 + tmp2**2 + self.L1 ** 2 - self.L2 ** 2
        A = 2 * tmp2 * self.L1
        B = 2 * tmp1 * self.L1
        C = tmp3 / np.sqrt(A**2 + B**2)
        phi = np.arctan(B/A)
        theta1 = np.arcsin(C) - phi
        theta2 = np.arccos((tmp1 - self.L1 * np.cos(theta1))/self.L2) - theta1
        theta3 = angle - theta1 - theta2
        return theta1, theta2, theta3
    
    def get_velocity(self, theta1, theta2, theta3):
        return (theta1 - self.player.theta_1) / 10, (theta2 - self.player.theta_2) / 10, (theta3 - self.player.theta_3) / 10

    def get_action(self):
        if self.ball_v[0] >= 0:
            return 0, 0, 0
        
        ball_x, ball_y, angle = self.get_hit_position()
        if abs(ball_y - self.player.basepos[1]) > self.L1 + self.L2 + self.L3:
            return 0, 0, 0

        angle1, angle2, angle3 = self.get_angle(ball_x - self.player.basepos[0], ball_y - self.player.basepos[1], angle)
        return self.get_velocity(angle1, angle2, angle3)

    
