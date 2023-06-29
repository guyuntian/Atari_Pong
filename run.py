import numpy as np
import os
import random
import gym
from env import World
from utils import check_collision, collision
from elements import Ball, Board, Robot, R3bot
from action import Action

env = World()
left_obs, right_obs = env.reset()
terminated = False

for i in range(100):
    print("Running...Step %d" % i) 

    actions = []
    # Action here
    act1 = Action(left_obs)
    act2 = Action(right_obs)
    actions.append(act1.get_action())
    actions.append(act2.get_action())
    # print(actions)
    left_obs, right_obs, terminated = env.step(actions)
    if terminated: 
        print(env.Left_Player.theta_1 * 180 / np.pi, env.Left_Player.theta_2 * 180 / np.pi, env.Left_Player.theta_3 * 180 / np.pi)
        print(env.Left_Player.Bd.pos, env.Left_Player.Bd.angle)
        break

