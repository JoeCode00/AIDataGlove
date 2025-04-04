from scipy.spatial.transform import Rotation
import numpy as np
import pandas as pd
from src.Robots2 import (
    aligned_P,
    aligned_R,
    aligned_T,
    T_from_RP,
    P_from_TP,
    inv_T,
    R_from_T,
    vector_length,
    line_from_two_points,
    plane_from_point_and_line,
    point_from_point_projected_to_plane,
)


class Position:
    def __init__(self):
        self.accel_deadband = 0.12

        self.rot = None
        self.world_acceleration = aligned_P()
        self.quat = np.zeros(4)
        self.R = aligned_R()
        self.local_R = aligned_R()
        self.Rx = np.zeros((3, 1))
        self.Ry = np.zeros((3, 1))
        self.Rz = np.zeros((3, 1))
        self.T = aligned_T()
        self.local_T = aligned_T()
        self.world_T = aligned_T()
        self.local_acceleration = aligned_P()

        self.pointer_S = aligned_P()
        self.pointer_SOL = aligned_P()

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
        if quat is not None and (quat[1] ** 2 + quat[2] ** 2 + quat[3] ** 2) != 0:
            self.quat = quat
        else:
            raise ValueError("Invalid Quat")

    def get(self, timestamp: float):
        self.rot = Rotation.from_quat(self.quat)
        self.local_R = self.rot.as_matrix()

        self.local_T = T_from_RP(R=self.local_R, P=self.world_acceleration)
        self.T = np.matmul(self.local_T, inv_T(self.world_T))
        self.R = R_from_T(self.T)
        self.Rx = self.R[:, 0]
        self.Ry = self.R[:, 1]
        self.Rz = self.R[:, 2]

        self.local_acceleration = P_from_TP(T=self.T, P=self.world_acceleration)
        self.history.loc[timestamp, self.accel_euler_quat_columns] = (
            self.world_acceleration.T[0].tolist()
            + self.quat.tolist()
            + self.local_acceleration.T[0].tolist()
        )

        self.pointer_S, self.pointer_SOL = line_from_two_points(aligned_P(), -self.Rz)
        print(self.pointer_S)

    def low_accel_homing_check(self):
        if vector_length(self.world_acceleration) < self.accel_deadband:
            self.reset_world()

    def make_accel(self, accelerometer_x, accelerometer_y, accelerometer_z):
        accel = aligned_P()
        accel[0] = accelerometer_x
        accel[1] = accelerometer_y
        accel[2] = accelerometer_z
        return accel

    def make_quat(self, quat_w, quat_x, quat_y, quat_z):
        quat = np.array([quat_w, quat_x, quat_y, quat_z])
        return quat

    def reset_world(self):
        self.world_T = self.local_T


class GlyphPlane:
    def __init__(self, distance, size):

        self.point_on_plane_1 = aligned_P()
        self.point_on_plane_1[0] = 0
        self.point_on_plane_1[1] = 0
        self.point_on_plane_1[2] = -distance

        self.point_on_plane_2 = aligned_P()
        self.point_on_plane_2[0] = 0
        self.point_on_plane_2[1] = 1
        self.point_on_plane_2[2] = -distance

        self.point_on_plane_3 = aligned_P()
        self.point_on_plane_3[0] = 1
        self.point_on_plane_3[1] = 1
        self.point_on_plane_3[2] = -distance

        self.line_on_plane_S = aligned_P()
        self.line_on_plane_SOL = aligned_P()
        self.plane_D0 = 0
        self.plane_S = aligned_P()

        self.display_width_half = size/2
        self.display_height_half = size/2

        self.local_top_right = aligned_P()
        self.local_top_right[0] = self.display_width_half
        self.local_top_right[1] = self.display_height_half

        self.local_top_left = aligned_P()
        self.local_top_left[0] = -self.display_width_half
        self.local_top_left[1] = self.display_height_half

        self.local_bottom_left = aligned_P()
        self.local_bottom_left[0] = -self.display_width_half
        self.local_bottom_left[1] = -self.display_height_half

        self.local_bottom_right = aligned_P()
        self.local_bottom_right[0] = self.display_width_half
        self.local_bottom_right[1] = -self.display_height_half

        self.world_top_right = aligned_P()
        self.world_top_left = aligned_P()
        self.world_bottom_left = aligned_P()
        self.world_bottom_right = aligned_P()

        self.update()

    def update(self):
        self.line_on_plane_S, self.line_on_plane_SOL = line_from_two_points(
            self.point_on_plane_1, self.point_on_plane_2
        )
        self.plane_D0, self.plane_S = plane_from_point_and_line(
            self.point_on_plane_3, self.line_on_plane_S, self.line_on_plane_SOL
        )
        self.world_top_right = point_from_point_projected_to_plane(
            self.local_top_right, self.plane_D0, self.plane_S
        )
        self.world_top_left = point_from_point_projected_to_plane(
            self.local_top_left, self.plane_D0, self.plane_S
        )
        self.world_bottom_left = point_from_point_projected_to_plane(
            self.local_bottom_left, self.plane_D0, self.plane_S
        )
        self.world_bottom_right = point_from_point_projected_to_plane(
            self.local_bottom_right, self.plane_D0, self.plane_S
        )

    def plane(self):
        return self.plane_D0, self.plane_S
