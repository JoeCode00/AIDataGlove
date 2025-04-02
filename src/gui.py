import dearpygui.dearpygui as dpg
from src.gui_help import _create_dynamic_textures, _create_static_textures
import numpy as np


def stop():
    dpg.stop_dearpygui()
    dpg.destroy_context()


def grid_helper(parent_uid=None, viewport=False):

    parent_width = 0
    parent_height = 0
    children_uids = None

    if parent_uid is not None:

        parent_width = dpg.get_item_configuration(parent_uid)["width"]
        grandparent = parent_uid
        while parent_width == 0:
            grandparent = dpg.get_item_parent(grandparent)
            parent_width = dpg.get_item_configuration(grandparent)["width"]

        parent_height = dpg.get_item_configuration(grandparent)["height"]

        children_uids = dpg.get_item_children(parent_uid)[1]

    elif viewport:
        parent_width = dpg.get_viewport_width()
        parent_height = dpg.get_viewport_height()
        children_uids = dpg.get_windows()

    grid_min_x = 0
    grid_min_y = 0
    grid_max_x = 0
    grid_max_y = 0

    for child in children_uids:
        try:
            config = dpg.get_item_configuration(child)
        except SystemError:
            continue
        if isinstance(config["user_data"], tuple):  # Is a configured item
            arrangement_tuple = config["user_data"]
            min_y, min_x, max_y, max_x = arrangement_tuple
            if min_x < grid_min_x:
                grid_min_x = min_x
            if min_y < grid_min_y:
                grid_min_y = min_y
            if max_x > grid_max_x:
                grid_max_x = max_x
            if max_y > grid_max_y:
                grid_max_y = max_y

    grid_spread_x = abs(grid_max_x - grid_min_x)
    grid_spread_y = abs(grid_max_y - grid_min_y)

    if grid_spread_x > 0 and grid_spread_y > 0:
        grid_width = float(np.floor(parent_width / grid_spread_x))
        grid_height = float(np.floor(parent_height / grid_spread_y))
    else:
        return

    # if parent_uid == 42:
    #     breakpoint()
    #     print("start")

    for child in children_uids:
        try:
            config = dpg.get_item_configuration(child)
        except SystemError:
            continue
        if isinstance(config["user_data"], tuple):  # Is a configured item

            arrangement_tuple = config["user_data"]
            min_y, min_x, max_y, max_x = arrangement_tuple
            pos_x = float(np.floor(min_x * grid_width))
            pos_y = float(np.floor(min_y * grid_height))
            spread_x = abs(max_x - min_x)
            spread_y = abs(max_y - min_y)
            width = spread_x * grid_width
            height = spread_y * grid_height
            try:
                childs_child = dpg.get_item_children(child)[1][0]

                childs_child_type = dpg.get_item_type(childs_child)
                if childs_child_type == "mvAppItemType::mvPlot":
                    continue
            except IndexError:
                pass
            if dpg.get_item_type(child) == "mvAppItemType::mvGroup":
                width = 0.98 * width
                height = 0.90 * height
                pos_y = pos_y + 0.05 * height
            dpg.configure_item(
                item=child, pos=(pos_x, pos_y), width=width, height=height
            )


def plothelper(
    plotlabel,
    xaxis,
    xaxisunits,
    xaxismin,
    xaxismax,
    yaxis,
    yaxisunits,
    yaxismin,
    yaxismax,
    axis_labels=[["X", "Red"], ["Y", "Green"], ["Z", "Blue"]],
):

    with dpg.plot(label=plotlabel, fit_button=1):
        # required: create x and y axes
        dpg.set_axis_limits(
            dpg.add_plot_axis(dpg.mvXAxis, label=xaxis + " (" + xaxisunits + ")"),
            xaxismin,
            xaxismax,
        )
        dpg.set_axis_limits(
            dpg.add_plot_axis(
                dpg.mvYAxis,
                label=yaxis + " (" + yaxisunits + ")",
                tag=yaxis + " VS " + xaxis + " Y",
            ),
            yaxismin,
            yaxismax,
        )

        # series belong to a y axis

        if xaxis == "Time":
            dpg.add_plot_legend()
            for axis, color in axis_labels:
                # breakpoint()
                dpg.add_line_series(
                    [],
                    [],
                    label=axis,
                    tag=yaxis + " VS " + xaxis + " " + axis + " Line",
                    parent=yaxis + " VS " + xaxis + " Y",
                )
                dpg.bind_item_theme(
                    yaxis + " VS " + xaxis + " " + axis + " Line", color + " Plot Line"
                )

        else:
            color = "white"
            dpg.add_line_series(
                [],
                [],
                label="a",
                tag=yaxis + " VS " + xaxis + " Line",
                parent=yaxis + " VS " + xaxis + " Y",
            )
            dpg.bind_item_theme(yaxis + " VS " + xaxis + " Line", color + " Plot Line")
            dpg.add_scatter_series(
                [],
                [],
                label="a",
                tag=yaxis + " VS " + xaxis + " Marker",
                parent=yaxis + " VS " + xaxis + " Y",
            )


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

    with dpg.window(label="Window 1", no_close=True, user_data=(0, 0, 1, 2)):
        with dpg.collapsing_header(label="Buttons", default_open=True):
            dpg.add_button(label="ESTOP", callback=lambda: stop(), width=200)

    with dpg.window(label="World Acceleration", no_close=True, user_data=(1, 0, 2, 1)):
        with dpg.group(horizontal=True, user_data=(0, 0, 1, 1)):
            with dpg.group(user_data=(0, 0, 1, 1)):
                plothelper(
                    "World Acceleration History",
                    "Time",
                    "s",
                    -5,
                    0,
                    "World Acceleration",
                    "",
                    -1,
                    1,
                )

    with dpg.window(label="Angles", no_close=True, user_data=(1, 1, 2, 2)):
        with dpg.group(horizontal=True, user_data=(0, 0, 1, 1)):
            with dpg.group(user_data=(0, 0, 1, 1)):
                plothelper(
                    "Angle History",
                    "Time",
                    "s",
                    -5,
                    0,
                    "Angle",
                    "rad",
                    -360,
                    360,
                    axis_labels=[["0", "Red"], ["1", "Green"], ["2", "Blue"]],
                )
    with dpg.window(label="Local Acceleration", no_close=True, user_data=(1, 2, 2, 3)):
        with dpg.group(horizontal=True, user_data=(0, 0, 1, 1)):
            with dpg.group(user_data=(0, 0, 1, 1)):
                plothelper(
                    "Local Acceleration History",
                    "Time",
                    "s",
                    -5,
                    0,
                    "Local Acceleration",
                    "",
                    -1,
                    1,
                )


def redraw_grid(recursion_levels):
    grid_helper(viewport=True)
    level0 = dpg.get_windows()
    for i in range(recursion_levels):
        levels = [level0] + [[]] * recursion_levels
        for parent in levels[i]:
            user_data = dpg.get_item_configuration(parent)["user_data"]
            if isinstance(user_data, tuple):
                grid_helper(parent_uid=parent)
            children = dpg.get_item_children(parent)[1]
            if children != []:
                for child in children:
                    levels[i + 1] = levels[i + 1] + [child]
