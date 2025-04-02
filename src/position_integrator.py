from scipy.integrate import trapezoid
import numpy as np

np.set_printoptions(suppress=True)


def integrate(data_array: np.array, time_array: np.array):
    data_array = data_array[~np.isnan(data_array)]
    time_array = time_array[~np.isnan(time_array)]

    if len(np.shape(data_array)) != 1:
        raise Exception("The data array must be a 1-dimensional array.")
    if len(np.shape(time_array)) != 1:
        raise Exception("The time array must be a 1-dimensional array.")
    if np.shape(data_array) != np.shape(time_array):
        raise Exception("The data and time arrays must be the same shape.")
    try:
        return trapezoid(data_array, x=time_array)
    except Exception as e:
        raise Exception(f"Position integration error {repr(e)}") from e


def integrated_array(data_length, data_width):
    arr = np.zeros(
        (
            data_length,
            data_width,
        )
    )
    arr[:, :] = np.nan
    return arr


class dynamics:
    def __init__(self, *args, **kwargs):
        self.data_length = 10  # doubles in each array
        self.time = integrated_array(self.data_length, 1)
        self.accel = integrated_array(self.data_length, 3)
        self.vel = integrated_array(self.data_length, 3)
        self.pos = integrated_array(self.data_length, 3)

        self.accel_bias_x = 0
        self.accel_bias_y = 0
        self.accel_bias_z = 0

        self.vel_bias_x = 0
        self.vel_bias_y = 0
        self.vel_bias_z = 0

        self.pos_bias_x = 0
        self.pos_bias_y = 0
        self.pos_bias_z = 0

    def get(
        self,
        time: float,
        accelerometer_x: float,
        accelerometer_y: float,
        accelerometer_z: float,
    ):
        self.time = np.roll(self.time, -1, axis=0)
        self.accel = np.roll(self.accel, -1, axis=0)
        self.vel = np.roll(self.vel, -1, axis=0)
        self.pos = np.roll(self.pos, -1, axis=0)

        self.time[self.data_length - 1] = time
        self.accel[self.data_length - 1, :] = np.array(
            [
                accelerometer_x - self.accel_bias_x,
                accelerometer_y - self.accel_bias_y,
                accelerometer_z - self.accel_bias_z,
            ]
        )

        new_vel_x = integrate(self.accel[:, 0], self.time) - self.vel_bias_x
        new_vel_y = integrate(self.accel[:, 1], self.time) - self.vel_bias_y
        new_vel_z = integrate(self.accel[:, 2], self.time) - self.vel_bias_z

        self.vel[self.data_length - 1, :] = np.array([new_vel_x, new_vel_y, new_vel_z])

        new_pos_x = integrate(self.vel[:, 0], self.time) - self.pos_bias_x
        new_pos_y = integrate(self.vel[:, 1], self.time) - self.pos_bias_y
        new_pos_z = integrate(self.vel[:, 2], self.time) - self.pos_bias_z

        self.pos[self.data_length - 1, :] = np.array([new_pos_x, new_pos_y, new_pos_z])
        print(np.round(self.pos[self.data_length - 1, :] * 300, 0))

    def bias(self):
        self.accel_bias_x, self.accel_bias_y, self.accel_bias_z = self.accel[
            self.data_length - 1, :
        ].tolist()
        self.vel_bias_x, self.vel_bias_y, self.vel_bias_z = self.vel[
            self.data_length - 1, :
        ].tolist()
        self.pos_bias_x, self.pos_bias_y, self.pos_bias_z = self.pos[
            self.data_length - 1, :
        ].tolist()

        self.time = integrated_array(self.data_length, 1)
        self.accel = integrated_array(self.data_length, 3)
        self.vel = integrated_array(self.data_length, 3)
        self.pos = integrated_array(self.data_length, 3)
