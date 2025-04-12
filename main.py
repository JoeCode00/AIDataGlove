import struct
import numpy as np
import dearpygui.dearpygui as dpg

from src.threaded_queue import ComThread
from src.handle_time import Timer

# from src.dead_reckoning import Dynamics
from src.motion import Position, GlyphPlane
from src.gui import stop_gui, plothelper, CalibrationThemes
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
            dpg.add_button(
                label="ESTOP",
                callback=lambda: stop_gui(),
                width=dpg.get_item_width("Window") - 15,
            )
            dpg.add_button(
                label="Reset World",
                callback=lambda: pos.reset_world(),
                width=dpg.get_item_width("Window") - 15,
            )
        ColumnWidth = dpg.get_item_width("Window") / 2 * 0.95
        RowHeight = dpg.get_item_height("Window") / 3 * 0.95
        with dpg.group(horizontal=True):
            with dpg.child_window(
                tag="Calibration", height=RowHeight, width=ColumnWidth
            ):
                dpg.add_text("Calibration")
                dpg.add_text("", tag="Calibration Help")
                dpg.add_input_text(
                    default_value="System",
                    tag="Calibration System",
                    readonly=True,
                    width=dpg.get_item_width("Calibration"),
                )
                dpg.add_input_text(
                    default_value="Mag",
                    tag="Calibration Mag",
                    readonly=True,
                    width=dpg.get_item_width("Calibration"),
                )
                dpg.add_input_text(
                    default_value="Accel",
                    tag="Calibration Accel",
                    readonly=True,
                    width=dpg.get_item_width("Calibration"),
                )
                dpg.add_input_text(
                    default_value="Gyro",
                    tag="Calibration Gyro",
                    readonly=True,
                    width=dpg.get_item_width("Calibration"),
                )

            with dpg.child_window(tag="TBD", height=RowHeight, width=ColumnWidth):
                pass

    with dpg.window(
        label="Glyph",
        tag="Glyph",
        no_close=True,
        width=dpg.get_viewport_width() / 2,
        height=dpg.get_viewport_height() / 2,
        pos=[dpg.get_viewport_width() / 2, 0],
    ):
        ColumnWidth = dpg.get_item_width("Glyph") / 2 * 0.95
        RowHeight = dpg.get_item_height("Glyph") * 0.95
        with dpg.group(horizontal=True, height=RowHeight):
            with dpg.group(width=ColumnWidth):
                plothelper(
                    plotlabel="Plane Viewer",
                    xaxis="X",
                    xaxisunits="-",
                    xaxismin=-5,
                    xaxismax=5,
                    yaxis="Y",
                    yaxisunits="-",
                    yaxismin=5,
                    yaxismax=-5,
                    axis_labels=[
                        ["X", "Red"],
                        ["Y", "Green"],
                        ["Z", "Blue"],
                        ["Pointer", "White"],
                        ["Plane Right", "White"],
                        ["Plane Top", "White"],
                        ["Plane Left", "White"],
                        ["Plane Bottom", "White"],
                    ],
                    legend_show=False,
                )

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


def handle_calibration(frame, cal_themes):
    cal_sys, cal_gyro, cal_accel, cal_mag = frame["Calibration"]
    dpg.bind_item_theme(
        dpg.get_alias_id("Calibration System"),
        cal_themes[cal_sys],
    )
    dpg.bind_item_theme(
        dpg.get_alias_id("Calibration Mag"),
        cal_themes[cal_mag],
    )
    dpg.bind_item_theme(
        dpg.get_alias_id("Calibration Accel"),
        cal_themes[cal_accel],
    )
    dpg.bind_item_theme(
        dpg.get_alias_id("Calibration Gyro"),
        cal_themes[cal_gyro],
    )
    if cal_mag != 3:
        dpg.set_value("Calibration Help", "Mag: Move in figure-8")
        return False
    if cal_accel != 3:
        dpg.set_value("Calibration Help", "Accel: Place on orthogonal sides")
        return False
    if cal_gyro != 3:
        dpg.set_value("Calibration Help", "Gyro: Stop moving the sensor")
        return False
    if cal_sys < 2:
        dpg.set_value("Calibration Help", "System: Move the sensor around")
        return False
    dpg.set_value("Calibration Help", "")
    return True


def handle_pos(frame, timestamp):
    accelerometer_x, accelerometer_y, accelerometer_z = frame["Accelerometer"]
    accel = pos.make_accel(accelerometer_x, accelerometer_y, accelerometer_z)
    quat_w, quat_x, quat_y, quat_z = frame["Quaternion"]
    quat = pos.make_quat(quat_w, quat_x, quat_y, quat_z)
    try:
        pos.set(world_acceleration=accel, quat=quat)
        pos.get(timestamp)
    except ValueError:
        raise ValueError("Could not handle pos")


def draw_plane():
    plane_sides = [
        ["Right", plane.world_bottom_right, plane.world_top_right],
        ["Top", plane.world_top_left, plane.world_top_right],
        ["Left", plane.world_bottom_left, plane.world_top_left],
        ["Bottom", plane.world_bottom_left, plane.world_bottom_right],
    ]
    for side, coords_1, coords_2 in plane_sides:
        dpg.set_value(
            f"Y VS X Plane {side} Line",
            [[coords_1[0], coords_2[0]], [coords_1[1], coords_2[1]]],
        )


def draw_axes(timestamp):
    for scope in ["World", "Local"]:
        for axis in ["X", "Y", "Z"]:
            dpg.set_value(
                f"{scope} Acceleration VS Time {axis} Line",
                [
                    (pos.history.index - timestamp).tolist(),
                    pos.history.loc[:, f"{scope} Acceleration {axis}"].tolist(),
                ],
            )
        for angle_axis, axis_index in [["X", 0], ["Z", 2]]:
            for str, R in [["RX", pos.Rx], ["RY", pos.Ry], ["RZ", pos.Rz]]:
                dpg.set_value(
                    f"Angle Y VS Angle {angle_axis} {str} Line",
                    [[0, R[axis_index]], [0, R[1]]],
                )

        for str, R in [["X", pos.Rx], ["Y", pos.Ry], ["Z", pos.Rz]]:
            dpg.set_value(f"Y VS X {str} Line", [[0, R[0]], [0, R[1]]])

        if True:
            traced_point = plane.trace_point(pos.pointer_S, pos.pointer_SOL)
            dpg.set_value(
                "Y VS X Pointer Line", [[0, traced_point[0]], [0, -traced_point[1]]]
            )
        else:
            dpg.set_value("Y VS X Pointer Line", [[0, 0], [0, 0]])


com = ComThread()
time = Timer()
pos = Position()
plane = GlyphPlane(distance=5, size=8)


def main():
    dpg.create_context()
    setup_gui()
    cal_themes = CalibrationThemes().themes()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.render_dearpygui_frame()
    # dpg.show_metrics()

    draw_plane()

    com.start()
    data_write = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    timestamp = time.now()

    # data_read = None
    # while data_read is None:
    #     data_read = communicate(com, data_write, struct_pattern="16d")
    # handle_pos(data_read, timestamp)
    # pos.reset_world()

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        data_read = communicate(com, data_write, struct_pattern="16d")
        if data_read is not None:
            data_write = data_read
            timestamp = time.now()
            try:
                (
                    accelerometer_x,
                    accelerometer_y,
                    accelerometer_z,
                    quat_w,
                    quat_x,
                    quat_y,
                    quat_z,
                    cal_sys,
                    cal_gyro,
                    cal_accel,
                    cal_mag,
                    *_,
                ) = data_read

                frame = {
                    "Accelerometer": [
                        accelerometer_x,
                        accelerometer_y,
                        accelerometer_z,
                    ],
                    "Quaternion": [quat_w, quat_x, quat_y, quat_z],
                    "Calibration": [
                        int(cal_sys),
                        int(cal_gyro),
                        int(cal_accel),
                        int(cal_mag),
                    ],
                }

                if handle_calibration(frame, cal_themes):
                    handle_pos(frame, timestamp)
                    # pos.low_accel_homing_check()
            except ValueError:
                continue

            draw_axes(timestamp)

    dpg.destroy_context()


if __name__ == "__main__":
    main()
