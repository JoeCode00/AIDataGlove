import struct
import numpy as np
import dearpygui.dearpygui as dpg

from src.threaded_queue import ComThread
from src.handle_time import Timer

# from src.dead_reckoning import Dynamics
from src.motion import Position
from src.gui import setup_gui, redraw_grid


np.set_printoptions(suppress=True)


def communicate(
    com: ComThread,
    data_write: bytes | tuple,
    struct_pattern: str,
    disable_read: bool = False,
):
    if data_write is not None:
        if isinstance(data_write, tuple):
            if struct_pattern is None:
                raise TypeError("Must pass in a struct pattern with tuple to be packed")
            data_write = struct.pack(struct_pattern, *data_write)
        com.writer(data_write)

    data_read = None
    if not disable_read:
        data_read = com.reader()
        if data_read is not None:
            struct_size = struct.calcsize(struct_pattern)
            if len(data_read) != struct_size:
                return
            data_read = struct.unpack(struct_pattern, data_read)

    return data_read


def handle_pos(data_read, timestamp):
    accelerometer_x, accelerometer_y, accelerometer_z, euler_0, euler_1, euler_2, *_ = (
        data_read
    )
    accel = pos.make_accel(accelerometer_x, accelerometer_y, accelerometer_z)
    euler = pos.make_euler(euler_0, euler_1, euler_2)
    pos.set(world_acceleration=accel, euler=euler)
    pos.get(timestamp)


com = ComThread()
time = Timer()
pos = Position()


def main():
    dpg.create_context()
    setup_gui()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.render_dearpygui_frame()
    dpg.show_metrics()

    old_viewport_width = None
    old_viewport_height = None

    com.start()
    data_write = (0, 0, 0, 0, 0, 0, 0, 0)

    # bias_timer = Timer()
    # bias_set = False
    timestamp = time.now()

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        new_viewport_width = dpg.get_viewport_width()
        new_viewport_height = dpg.get_viewport_height()

        if (
            new_viewport_width != old_viewport_width
            or new_viewport_height != old_viewport_height
        ):
            recursion_levels = 6
            redraw_grid(recursion_levels)
        old_viewport_width = new_viewport_width
        old_viewport_height = new_viewport_height

        data_read = communicate(com, data_write, struct_pattern="8d")
        if data_read is not None:
            data_write = data_read
            timestamp = time.now()
            handle_pos(data_read, timestamp)

            for scope in ["World", "Local"]:
                for axis in ["X", "Y", "Z"]:
                    dpg.set_value(
                        f"{scope} Acceleration VS Time {axis} Line",
                        [
                            (pos.history.index - timestamp).tolist(),
                            pos.history.loc[:, f"{scope} Acceleration {axis}"].tolist(),
                        ],
                    )
            dpg.set_value(
                "Angle VS Time 0 Line",
                [
                    (pos.history.index - timestamp).tolist(),
                    pos.history.loc[:, "Euler 0"].tolist(),
                ],
            )
            dpg.set_value(
                "Angle VS Time 1 Line",
                [
                    (pos.history.index - timestamp).tolist(),
                    pos.history.loc[:, "Euler 1"].tolist(),
                ],
            )
            dpg.set_value(
                "Angle VS Time 2 Line",
                [
                    (pos.history.index - timestamp).tolist(),
                    pos.history.loc[:, "Euler 2"].tolist(),
                ],
            )
            print(pos.history.loc[timestamp, ["World Acceleration Y"]].tolist())
            # for order in ["Acceleration", "Velocity", "Position"]:
            #     for axis in ["X", "Y", "Z"]:
            #         dpg.set_value(
            #             f"{order} VS Time {axis} Line",
            #             [
            #                 pos.process_history(order="Time", timer=time),
            #                 pos.process_history(order=order, axis=axis),
            #             ],
            #         )
            # dpg.set_value(
            #     "Position Y VS Position X Line",
            #     [
            #         pos.process_history(order="Position", axis="X")[-10:-1],
            #         pos.process_history(order="Position", axis="Y")[-10:-1],
            #     ],
            # )

            # dpg.set_value(
            #     "Position Y VS Position X Marker",
            #     [
            #         [pos.process_history(order="Position", axis="X")[-1]],
            #         [pos.process_history(order="Position", axis="Y")[-1]],
            #     ],
            # )

            # dpg.set_value('Acceleration VS Time X Line', [[0, -time.now()], [0, accelerometer_x]])
            # print(pos.history.loc[:, 'pos'].loc[:, 'x'].tolist()[:-1])
            # if pos.history.shape[0]>500:
            #     breakpoint()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
