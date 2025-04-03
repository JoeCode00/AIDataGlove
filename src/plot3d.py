import matplotlib.pyplot as plt

# import numpy as np


class PLT:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection="3d")

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_title("Real-time 3D Plot")

    def axesplot(self, axes: list, format: list = ["r-"]):
        self.ax.cla()
        # for index, axis in enumerate(axes):
        x, y, z = axes[0].tolist()
        self.ax.plot(x, y, z, format[0])

        self.ax.set_xlim3d(-2, 2)
        self.ax.set_ylim3d(-2, 2)
        self.ax.set_zlim3d(-2, 2)
        self.ax.autoscale(False)
        plt.pause(0.001)


# ploter = PLT()

# # Main loop for updating the plot
# while True:
#     num_points = 50
#     x = np.linspace(0, 10, num_points)
#     y = 0.1 * np.random.rand(num_points) - 0.05
#     z = 0.1 * np.random.rand(num_points) - 0.05
#     ploter.plot(x, y, z)
