import numpy as np
import pandas as pd


class Dynamics():
    def __init__(self):
        self.position = np.zeros((3, 1))
        self.velocity = np.zeros((3, 1))
        self.acceleration = np.zeros((3, 1))
        self.time_step = None

        self.bias_acceleration = np.zeros((3, 1))
        self.bias_velocity = np.zeros((3, 1))
        self.bias_position = np.zeros((3, 1))

        self.max_samples_stored = 100

        arrays = [
            ['pos']*3 + ['vel']*3+['accel']*3,
            ['x', 'y', 'z']*3
        ]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples, names=["order", "axis"])

        # self.history_columns = ['pos_x', 'pos_y', 'pos_z',
        #                         'vel_x', 'vel_y', 'vel_z',
        #                         'accel_x', 'accel_y', 'accel_z'
        #                         ]
        self.history = pd.DataFrame(
            np.array(np.zeros((1, len(['pos']*3 + ['vel']*3+['accel']*3))),
                     dtype=float),
            columns=index)

    def get(self,
            current_time: float,
            time_step: int | float,
            accel_x: int | float,
            accel_y: int | float,
            accel_z: int | float
            ):
        self.acceleration = np.array(
            [[accel_x], [accel_y], [accel_z]]) - self.bias_acceleration
        self.time_step = time_step

        self.velocity = self.velocity + self.acceleration * \
            self.time_step - self.bias_velocity
        self.position = (self.position
                         + self.velocity * self.time_step
                         + 0.5 * self.acceleration ** 2
                         - self.bias_position)

        self.history.loc[current_time, :] = (self.position.T.tolist()[0]
                                             + self.velocity.T.tolist()[0]
                                             + self.acceleration.T.tolist()[0])

    def bias(self, accel=None):
        if accel is not None:
            self.bias_acceleration = accel
        else:
            self.bias_acceleration = self.acceleration
        self.bias_velocity = self.velocity
        self.bias_position = self.position
