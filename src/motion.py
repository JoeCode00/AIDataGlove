from scipy.spatial.transform import Rotation
import numpy as np
import pandas as pd
from src.Robots2 import aligned_P, aligned_R, aligned_T, T_from_RP, P_from_TP


class Position:
    def __init__(self):
        self.world_acceleration = aligned_P()
        self.euler = np.zeros(3)
        self.R = aligned_R()
        self.Rx = np.zeros((3, 1))
        self.Ry = np.zeros((3, 1))
        self.Rz = np.zeros((3, 1))
        self.T = aligned_T()
        self.local_acceleration = aligned_P()

        self.accel_euler_columns = [
            "World Acceleration X",
            "World Acceleration Y",
            "World Acceleration Z",
            "Euler 0",
            "Euler 1",
            "Euler 2",
            "Local Acceleration X",
            "Local Acceleration Y",
            "Local Acceleration Z",
        ]
        self.history = pd.DataFrame(
            np.array(
                np.zeros((1, len(self.accel_euler_columns))),
                dtype=float,
            ),
            columns=self.accel_euler_columns,
        )

    def set(self, world_acceleration: np.ndarray = None, euler: np.ndarray = None):
        if world_acceleration is not None:
            self.world_acceleration = world_acceleration
        if euler is not None:
            self.euler = euler

    def get(self, timestamp: float):
        self.R = Rotation.from_euler("zyx", self.euler).as_matrix()
        self.Rx = self.R[:, 0]
        self.Ry = self.R[:, 1]
        self.Rz = self.R[:, 2]
        self.T = T_from_RP(R=self.R, P=self.world_acceleration)
        self.local_acceleration = P_from_TP(T=self.T, P=self.world_acceleration)
        self.history.loc[timestamp, self.accel_euler_columns] = (
            self.world_acceleration.T[0].tolist()
            + self.euler.tolist()
            + self.local_acceleration.T[0].tolist()
        )

    def make_accel(self, accelerometer_x, accelerometer_y, accelerometer_z):
        accel = aligned_P()
        accel[0] = accelerometer_x
        accel[1] = accelerometer_y
        accel[2] = accelerometer_z
        return accel

    def make_euler(self, euler_1, euler_2, euler_3):
        euler = np.array([euler_1, euler_2, euler_3])
        return euler
