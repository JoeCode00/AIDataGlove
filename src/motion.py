from scipy.spatial.transform import Rotation
import numpy as np
import pandas as pd
from src.Robots2 import aligned_P, aligned_R, aligned_T, T_from_RP, P_from_TP


class Position:
    def __init__(self):
        self.rot = None
        self.world_acceleration = aligned_P()
        self.quat = np.zeros(4)
        self.R = aligned_R()
        self.Rx = np.zeros((3, 1))
        self.Ry = np.zeros((3, 1))
        self.Rz = np.zeros((3, 1))
        self.T = aligned_T()
        self.local_acceleration = aligned_P()

        self.accel_euler_quat_columns = [
            "World Acceleration X",
            "World Acceleration Y",
            "World Acceleration Z",
            "Quat W",
            "Quat X",
            "Quat Y",
            "Quat Z",
            "Local Acceleration X",
            "Local Acceleration Y",
            "Local Acceleration Z",
        ]
        self.history = pd.DataFrame(
            np.array(
                np.zeros((1, len(self.accel_euler_quat_columns))),
                dtype=float,
            ),
            columns=self.accel_euler_quat_columns,
        )

    def set(self, world_acceleration: np.ndarray = None, quat: np.ndarray = None):
        if world_acceleration is not None:
            self.world_acceleration = world_acceleration
        if quat is not None and (quat[1]**2+quat[2]**2+quat[3]**2) != 0:
            self.quat = quat
        else:
            raise ValueError('Invalid Quat')

    def get(self, timestamp: float):
        # breakpoint()
        self.rot = Rotation.from_quat(self.quat)
        self.R = self.rot.as_matrix()
        self.Rx = self.R[:, 0]
        self.Ry = self.R[:, 1]
        self.Rz = self.R[:, 2]
        self.T = T_from_RP(R=self.R, P=self.world_acceleration)
        self.local_acceleration = P_from_TP(T=self.T, P=self.world_acceleration)
        self.history.loc[timestamp, self.accel_euler_quat_columns] = (
            self.world_acceleration.T[0].tolist()
            + self.quat.tolist()
            + self.local_acceleration.T[0].tolist()
        )

    def make_accel(self, accelerometer_x, accelerometer_y, accelerometer_z):
        accel = aligned_P()
        accel[0] = accelerometer_x
        accel[1] = accelerometer_y
        accel[2] = accelerometer_z
        return accel

    def make_quat(self, quat_w, quat_x, quat_y, quat_z):
        quat = np.array([quat_w, quat_x, quat_y, quat_z])
        return quat
