import struct
import numpy as np
import dearpygui.dearpygui as dpg

from src.threaded_queue import ComThread
from src.handle_time import Timer

# from src.dead_reckoning import Dynamics
from src.motion import Position
from src.gui import stop_gui, plothelper
from src.gui_help import _create_dynamic_textures, _create_static_textures

np.set_printoptions(suppress=True)


def setup_gui():
    dpg.create_viewport(
        title="GUI",
        x_pos=-1920,
        y_pos=218,
        width=1920,
        height=1080,
        # decorated=False,
        always_on_top=False,
        vsync=False,
    )
    dpg.set_global_font_scale(1.2)

    dpg.add_texture_registry(
        label="Demo Texture Container", tag="__demo_texture_container"
    )
    dpg.add_colormap_registry(
        label="Demo Colormap Registry", tag="__demo_colormap_registry"
    )

    with dpg.theme(tag="__demo_hyperlinkTheme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [29, 151, 236, 25])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [29, 151, 236])

    _create_static_textures()
    _create_dynamic_textures()

    with dpg.theme(tag="Red Plot Line"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvPlotCol_Line, (255, 0, 0), category=dpg.mvThemeCat_Plots
            )
    with dpg.theme(tag="Green Plot Line"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvPlotCol_Line, (0, 255, 0), category=dpg.mvThemeCat_Plots
            )
    with dpg.theme(tag="Blue Plot Line"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvPlotCol_Line, (0, 0, 255), category=dpg.mvThemeCat_Plots
            )
    with dpg.theme(tag="White Plot Line"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvPlotCol_Line, (255, 255, 255), category=dpg.mvThemeCat_Plots
            )

    with dpg.window(
        label="Window",
        tag="Window",
        no_close=True,
        width=dpg.get_viewport_width() / 2,
        height=dpg.get_viewport_height() / 2,
        pos=[0, 0],
    ):
        with dpg.collapsing_header(label="Buttons", default_open=True):
            dpg.add_button(label="ESTOP", callback=lambda: stop_gui(), width=200)

    with dpg.window(
        label="Acceleration",
        tag="Acceleration",
        no_close=True,
        width=dpg.get_viewport_width() / 2,
        height=dpg.get_viewport_height() / 2,
        pos=[0, dpg.get_viewport_height() / 2],
    ):
        ColumnWidth = dpg.get_item_width("Acceleration") * 0.95
        RowHeight = dpg.get_item_height("Acceleration") / 2 * 0.95
        with dpg.group(horizontal=True, height=RowHeight):
            with dpg.group(width=ColumnWidth):
                plothelper(
                    plotlabel="World Acceleration History",
                    xaxis="Time",
                    xaxisunits="s",
                    xaxismin=-5,
                    xaxismax=0,
                    yaxis="World Acceleration",
                    yaxisunits="",
                    yaxismin=-5,
                    yaxismax=5,
                )
        with dpg.group(horizontal=True, height=RowHeight):
            with dpg.group(width=ColumnWidth):
                plothelper(
                    plotlabel="Local Acceleration History",
                    xaxis="Time",
                    xaxisunits="s",
                    xaxismin=-5,
                    xaxismax=0,
                    yaxis="Local Acceleration",
                    yaxisunits="",
                    yaxismin=-5,
                    yaxismax=5,
                )

    with dpg.window(
        label="Orientation",
        tag="Orientation",
        no_close=True,
        width=dpg.get_viewport_width() / 2,
        height=dpg.get_viewport_height() / 2,
        pos=[dpg.get_viewport_width() / 2, dpg.get_viewport_height() / 2],
    ):
        ColumnWidth = dpg.get_item_width("Orientation") / 2 * 0.95
        RowHeight = dpg.get_item_height("Orientation") * 0.95
        with dpg.group(horizontal=True, height=RowHeight):
            with dpg.group(width=ColumnWidth):
                plothelper(
                    plotlabel="Angle XY",
                    xaxis="Angle X",
                    xaxisunits="-",
                    xaxismin=-1,
                    xaxismax=1,
                    yaxis="Angle Y",
                    yaxisunits="-",
                    yaxismin=-1,
                    yaxismax=1,
                    axis_labels=[["RX", "Red"], ["RY", "Green"], ["RZ", "Blue"]],
                )
            with dpg.group(width=ColumnWidth):
                plothelper(
                    plotlabel="Angle ZY",
                    xaxis="Angle Z",
                    xaxisunits="-",
                    xaxismin=-1,
                    xaxismax=1,
                    yaxis="Angle Y",
                    yaxisunits="-",
                    yaxismin=-1,
                    yaxismax=1,
                    axis_labels=[["RX", "Red"], ["RY", "Green"], ["RZ", "Blue"]],
                )


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
    (
        accelerometer_x,
        accelerometer_y,
        accelerometer_z,
        quat_w,
        quat_x,
        quat_y,
        quat_z,
        *_,
    ) = data_read
    accel = pos.make_accel(accelerometer_x, accelerometer_y, accelerometer_z)
    quat = pos.make_quat(quat_w, quat_x, quat_y, quat_z)
    try:
        pos.set(world_acceleration=accel, quat=quat)
        pos.get(timestamp)
    except ValueError:
        raise ValueError("Could not handle pos")


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

    # old_viewport_width = None
    # old_viewport_height = None

    com.start()
    data_write = (0, 0, 0, 0, 0, 0, 0, 0)

    # bias_timer = Timer()
    # bias_set = False
    timestamp = time.now()

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        # new_viewport_width = dpg.get_viewport_width()
        # new_viewport_height = dpg.get_viewport_height()

        # if (
        #     new_viewport_width != old_viewport_width
        #     or new_viewport_height != old_viewport_height
        # ):
        #     recursion_levels = 8
        #     redraw_grid(recursion_levels)
        # old_viewport_width = new_viewport_width
        # old_viewport_height = new_viewport_height

        data_read = communicate(com, data_write, struct_pattern="8d")
        if data_read is not None:
            data_write = data_read
            timestamp = time.now()
            try:
                handle_pos(data_read, timestamp)
            except ValueError:
                continue

            for scope in ["World", "Local"]:
                for axis in ["X", "Y", "Z"]:
                    dpg.set_value(
                        f"{scope} Acceleration VS Time {axis} Line",
                        [
                            (pos.history.index - timestamp).tolist(),
                            pos.history.loc[:, f"{scope} Acceleration {axis}"].tolist(),
                        ],
                    )

            for str, R in [["RX", pos.Rx], ["RY", pos.Ry], ["RZ", pos.Rz]]:
                dpg.set_value(f"Angle Y VS Angle X {str} Line", [[0, R[0]], [0, R[1]]])

            for str, R in [["RX", pos.Rx], ["RY", pos.Ry], ["RZ", pos.Rz]]:
                dpg.set_value(f"Angle Y VS Angle Z {str} Line", [[0, R[2]], [0, R[1]]])

    dpg.destroy_context()


if __name__ == "__main__":
    main()
