import numpy as np
import math

class Ball:
    def __init__(self, pos, v, r):
    # pos: (x, y)
    # v: (v_x, v_y)
        self.pos = pos
        self.v = v
        self.r = r
 
class Board:
    def __init__(self, L, pos, angle, v, omega):
        self.L = L
        self.pos = pos
        self.angle = angle # normal angle
        self.v = v
        self.omega = omega

class Robot:
    def __init__(self):
        pass

class R3bot(Robot):
    def __init__(self, basepos, Bd: Board, L1, theta_1, L2, theta_2, L3, theta_3, om1 = 0, om2 = 0, om3 = 0):
        super(Robot, self).__init__()
        self.basepos = basepos
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.theta_3 = theta_3
        self.Bd = Bd
        self.om1 = om1
        self.om2 = om2
        self.om3 = om3

    def posing(self):
        #self.theta_1 = theta_1
        #self.theta_2 = theta_2
        #self.theta_3 = theta_3
        endpos_x = self.basepos[0] + self.L3*math.cos(self.theta_1+self.theta_2+self.theta_3) + self.L2*math.cos(self.theta_1+self.theta_2) + self.L1*math.cos(self.theta_1)
        endpos_y = self.basepos[1] + self.L3*math.sin(self.theta_1+self.theta_2+self.theta_3) + self.L2*math.sin(self.theta_1+self.theta_2) + self.L1*math.sin(self.theta_1)
        self.Bd.pos = [endpos_x, endpos_y]
        self.Bd.angle = self.theta_1 + self.theta_2 + self.theta_3 

    def velocity_passdown(self, om1, om2, om3):
        self.om1 = om1
        self.om2 = om2
        self.om3 = om3
        v_x = -self.L1*math.sin(self.theta_1)*self.om1-self.L2*math.sin(self.theta_1+self.theta_2)*(self.om1+self.om2) - self.L3*math.sin(self.theta_1+self.theta_2+self.theta_3)*(self.om1+self.om2+self.om3)
        v_y = self.L1*math.cos(self.theta_1)*self.om1+self.L2*math.cos(self.theta_1+self.theta_2)*(self.om1+self.om2) + self.L3*math.cos(self.theta_1+self.theta_2+self.theta_3)*(self.om1+self.om2+self.om3)
        self.Bd.v = [v_x, v_y]
        self.Bd.omega = om1 + om2 + om3

    def update_timestep(self):
        self.theta_1 += self.om1
        self.theta_2 += self.om2
        self.theta_3 += self.om3
        self.Bd.pos[0] += self.Bd.v[0]
        self.Bd.pos[1] += self.Bd.v[1]
        self.Bd.angle += self.Bd.omega

    
