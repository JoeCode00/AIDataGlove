import struct
import numpy as np
import dearpygui.dearpygui as dpg
from src.threaded_queue import ComThread
# from src.handle_time import Timer
# from src.dead_reckoning import Dynamics
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
                raise TypeError(
                    "Must pass in a struct pattern with tuple to be packed")
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


def main():
    dpg.create_context()
    setup_gui()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.render_dearpygui_frame()
    dpg.show_metrics()

    old_viewport_width = None
    old_viewport_height = None

    com = ComThread()
    # time = Timer()
    # pos = Dynamics()
    com.start()
    data_write = (0, 0, 0, 0, 0, 0, 0, 0)

    # bias_timer = Timer()
    # bias_set = False
    # old_timestamp = time.now()

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
            accelerometer_x, accelerometer_y, accelerometer_z, *_ = data_read
            # time_step = time.now() - old_timestamp
            # pos.get(time_step, accelerometer_x, accelerometer_y, accelerometer_z)
            # old_timestamp = time.now()
            dpg.set_value('Force VS Time X Line', [[], []])

    dpg.destroy_context()


if __name__ == "__main__":
    main()
