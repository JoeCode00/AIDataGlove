import numpy as np
import pandas as pd
from src.handle_time import Timer


class Dynamics:
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
            ["Position"] * 3 + ["Velocity"] * 3 + ["Acceleration"] * 3,
            ["X", "Y", "Z"] * 3,
        ]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples, names=["order", "axis"])

        self.history = pd.DataFrame(
            np.array(
                np.zeros(
                    (1, len(["Position"] * 3 + ["Velocity"] * 3 + ["Acceleration"] * 3))
                ),
                dtype=float,
            ),
            columns=index,
        )

    def set(self, accel_array, bias: bool = False):
        self.acceleration = accel_array - self.bias_acceleration

        deadband = 0.2
        if abs(self.acceleration[0]) < deadband:
            self.acceleration[0] = 0
        if abs(self.acceleration[1]) < deadband:
            self.acceleration[1] = 0
        if abs(self.acceleration[2]) < deadband:
            self.acceleration[2] = 0

        if np.max(np.abs(self.acceleration)) < deadband:
            self.bias()

        if bias:
            self.bias()

    def get(self, current_time: float, time_step: int | float, accel_array=None):
        if accel_array is not None:
            self.set(accel_array)

        self.time_step = time_step

        self.velocity = (
            self.velocity + self.acceleration * self.time_step - self.bias_velocity
        )
        self.position = (
            self.position
            + self.velocity * self.time_step
            + 0.5 * self.acceleration**2
            - self.bias_position
        )
        # if pd.shape(self.history)[0] > self.max_samples_stored:
        #     pass  # TODO add roling
        self.history.loc[current_time, :] = (
            self.position.T.tolist()[0]
            + self.velocity.T.tolist()[0]
            + self.acceleration.T.tolist()[0]
        )

    def process_history(self, order: str, axis: str = None, timer: Timer = None):
        if order == "Time" or axis == "Time":
            return (self.history.index - timer.now()).tolist()
        else:
            return self.history.loc[:, order].loc[:, axis].tolist()

    def bias(self):
        self.bias_acceleration = self.acceleration
        self.bias_velocity = self.velocity
        self.bias_position = self.position
