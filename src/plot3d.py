import matplotlib.pyplot as plt
import numpy as np


class PLT:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection="3d")

    def plot(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, format: str = "r-"):
        self.ax.cla()
        self.ax.plot(x, y, z, format)

        # Set plot labels and title
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_title("Real-time 3D Plot")

        # Keep the plot within some bounds.
        self.ax.set_xlim(min(x), max(x))
        self.ax.set_ylim(min(y) - 1, max(y) + 1)
        self.ax.set_zlim(min(z) - 1, max(z) + 1)

        plt.pause(0.00001)


# ploter = PLT()

# # Main loop for updating the plot
# while True:
#     num_points = 50
#     x = np.linspace(0, 10, num_points)
#     y = 0.1 * np.random.rand(num_points) - 0.05
#     z = 0.1 * np.random.rand(num_points) - 0.05
#     ploter.plot(x, y, z)
