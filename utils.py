import numpy as np
import math
from elements import Ball, Board

def check_collision(ball: Ball, board: Board): # check if the ball and the board collide
    # if collide, return the position of collision; if not, return false
    s = math.sqrt((ball.pos[0]-board.pos[0])**2 + (ball.pos[1]-board.pos[1])**2)
    if ball.pos[0] == board.pos[0]:
        if ball.pos[1] > board.pos[1]: 
            alpha = math.pi/2
        elif ball.pos[1] < board.pos[1]:
            alpha = -math.pi/2
        else:
            return board.pos
    else:
        alpha = math.atan((ball.pos[1]-board.pos[1])/(ball.pos[0]-board.pos[0]))
        l = abs(s*math.cos(alpha-board.angle-math.pi/2))
        d = abs(s*math.sin(alpha-board.angle-math.pi/2))
        if l < board.L/2 and d < ball.r:
            return [board.pos[0]+l*math.cos(board.angle+math.pi/2), board.pos[1]+l*math.sin(board.angle+math.pi/2)]
        else:
            return False


def collision(ball: Ball, board: Board, cpos):
    l = math.sqrt((cpos[0]-board.pos[0])**2 + (cpos[1]-board.pos[1])**2)
    if cpos == board.pos:
        v_board = [0, 0]
    else:
        b_angle = board.angle - math.pi * math.floor(board.angle/math.pi)
        if cpos[0] > board.pos[0]:
            c_angle = b_angle
        elif cpos[0] < board.pos[0]:
            c_angle = b_angle + math.pi
        else: 
            if cpos[1] > board.pos[1]:
                c_angle = math.pi
            else:
                c_angle = 0
        v_board_x = board.omega*l*math.cos(c_angle) + board.v[0]
        v_board_y = board.omega*l*math.sin(c_angle) + board.v[1]
        v_board = [v_board_x, v_board_y]
    v_ball = [2*v_board[0] - ball.v[0], 2*v_board - ball.v[1]]
    return v_ball



