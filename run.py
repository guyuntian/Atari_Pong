import numpy as np
import os
import random
import gym
from env import World
from utils import check_collision, collision
from elements import Ball, Board, Robot, R3bot
from action import Action
from tqdm import tqdm

env = World()
left_obs, right_obs = env.reset()
terminated = False
random.seed(2023)
for i in tqdm(range(100000)):
    # print("Running...Step %d" % i) 

    actions = []
    # Action here
    act1 = Action(left_obs)
    act2 = Action(right_obs)
    actions.append(act1.get_action())
    actions.append(act2.get_sota_action())
    # print(actions)
    left_obs, right_obs, terminated = env.step(actions)
    if terminated:
        left_obs, right_obs = env.reset()
    # if terminated: 
    #     print(env.Left_Player.Bd.pos, env.Left_Player.Bd.angle)
    #     print(env.Right_Player.Bd.pos, env.Right_Player.Bd.angle)

    #     break

print(env.left_score, env.right_score)