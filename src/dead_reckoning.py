import numpy as np

class Dynamics():
    def __init__(self):
        self.position = np.zeros((3, 1))
        self.velocity = np.zeros((3, 1))
        self.acceleration = np.zeros((3, 1))
        self.time_step = None

        self.bias_acceleration = np.zeros((3,1))
        self.bias_velocity = np.zeros((3,1))
        self.bias_position = np.zeros((3,1))

    def get(self, time_step:int|float, accel_x:int|float, accel_y:int|float, accel_z:int|float):
        self.acceleration = np.array([[accel_x], [accel_y], [accel_z]]) - self.bias_acceleration
        self.time_step = time_step

        self.velocity = self.velocity + self.acceleration * self.time_step - self.bias_velocity
        self.position = (self.position
                            + self.velocity * self.time_step
                            + 0.5 * self.acceleration ** 2
                            - self.bias_position)

    def bias(self, accel=None):
        if accel is not None:
            self.bias_acceleration = accel
        else:
            self.bias_acceleration = self.acceleration
        self.bias_velocity = self.velocity
        self.bias_position = self.position
