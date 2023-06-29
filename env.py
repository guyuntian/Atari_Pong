from elements import Ball, Board, Robot, R3bot
from utils import check_collision, collision
import numpy as np
import random
import gym

class World(gym.Env):
    def __init__(self, size = (1200, 500), board_length = 80, L_1 = 100, L_2 = 100, L_3 = 60, ball_r = 10, update_rate = 10):
        self.size = size
        self.update_rate = update_rate # 计数器，每十帧接收一次输入
        self.board_length = board_length
        self.L1 = L_1
        self.L2 = L_2
        self.L3 = L_3
        self.ball_r = ball_r
        self.left_score = 0
        self.right_score = 0
        self.Left_Player = R3bot((0, self.size[1]/2), Board(board_length, (self.L1+self.L2+self.L3), 0, [0, 0], 0), self.L1, 0, self.L2, 0, self.L3, 0, 0, 0, 0)
        self.Right_Player = R3bot((0, self.size[1]/2), Board(board_length, (self.L1+self.L2+self.L3), 0, [0, 0], 0), self.L1, 0, self.L2, 0, self.L3, 0, 0, 0, 0)
        self.ball = Ball([size[0]/2, size[1]/2], [0, 0], self.ball_r)
        # We'll do a 180 degree turn for all coordinates for Right_Player

    def get_obs(self, right=False):
        if right:
            ball_pos = [self.size[0] - self.ball.pos[0], self.size[1] - self.ball.pos[1]]
            ball_v = [-self.ball.v[0], -self.ball.v[1]]
            return self.Right_Player, ball_pos, ball_v
        return self.Left_Player, self.ball.pos, self.ball.v
    
    def render(self):
        #print(self.ball.pos)
        return


    def step(self, actions): # actions: list of tuple (om1, om2, om3)
        # do the next 10 frames
        left_action = actions[0]
        right_action = actions[1]
        for i in range(self.update_rate):
            self.Left_Player.velocity_passdown(left_action[0], left_action[1], left_action[2])
            self.Left_Player.posing()
            self.Left_Player.update_timestep()
            self.Right_Player.velocity_passdown(right_action[0], right_action[1], right_action[2])
            self.Right_Player.posing()
            self.Right_Player.update_timestep()
            self.ball.pos[0] += self.ball.v[0] # update ball pos
            self.ball.pos[1] += self.ball.v[1]
            if self.ball.pos[0] <= -self.ball.r:  # out of ground
                self.finish(True)
                return self.get_obs(False), self.get_obs(True), True
            elif self.ball.pos[0] >= self.size[0] + self.ball.r:
                self.finish(False)
                return self.get_obs(False), self.get_obs(True), True
            if self.ball.pos[1] < self.ball.r: # bounce back
                self.ball.pos[1] = self.ball.r
                self.ball.v[1] = -self.ball.v[1]
            elif self.ball.pos[1] > self.size[1] - self.ball.r:
                self.ball.pos[1] = self.size[1] - self.ball.r
                self.ball.v[1] = -self.ball.v[1]
            Right_ball = Ball([self.size[0]-self.ball.pos[0], self.size[1]-self.ball.pos[1]], [-self.ball.v[0], -self.ball.v[1]], self.ball.r)
            if check_collision(self.ball, self.Left_Player.Bd):
                v_ball = collision(self.ball, self.Left_Player.Bd, check_collision(self.ball, self.Left_Player.Bd))
                self.ball.v = v_ball
            elif check_collision(Right_ball, self.Right_Player.Bd):
                v_ball = collision(Right_ball, self.Right_Player.Bd, check_collision(Right_ball, self.Right_Player.Bd))
                self.ball.v = [-v_ball[0], -v_ball[1]]
            self.render()
        return self.get_obs(False), self.get_obs(True), False # Terminated

    def finish(self, right_win = False):
        if right_win: self.right_score += 1
        else: self.left_score += 1
        return

    def reset(self): # game start right after calling reset() 
        self.Left_Player = R3bot((0, self.size[1]/2), Board(self.board_length, (self.L1+self.L2+self.L3), 0, [0, 0], 0), self.L1, 0, self.L2, 0, self.L3, 0, 0, 0, 0)
        self.Right_Player = R3bot((0, self.size[1]/2), Board(self.board_length, (self.L1+self.L2+self.L3), 0, [0, 0], 0), self.L1, 0, self.L2, 0, self.L3, 0, 0, 0, 0)
        self.ball = Ball([self.size[0]/2, self.size[1]/2], [0, 0], self.ball_r)
        if random.random() > 0.5:
            self.ball.v = [5, 0]
        else:
            self.ball.v = [-5, 0]
        self.ball.v[1] = np.random.randint(-2, 2)
        
        return self.get_obs(False), self.get_obs(True)

