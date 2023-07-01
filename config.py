class config():
    def __init__(self):
        #env.py
        self.env_size = (2000, 500)
        self.board_length = 80
        self.L_1 = 100
        self.L_2 = 100
        self.L_3 = 60
        self.ball_r = 10
        self.update_rate = 1
        self.initial_ball_vx = 5
        self.initial_ball_vy = 3
        #run.py
        self.total_step = int(1e4)
        self.step_per_render = 10
        #action.py
        self.maxtry = 5
        self.max_v = 1
        self.velocity_rate = 10
        self.delta = 1
        self.hit_time = 2

