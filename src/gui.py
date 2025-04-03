import dearpygui.dearpygui as dpg
from src.gui_help import _create_dynamic_textures, _create_static_textures


def stop():
    dpg.stop_dearpygui()
    dpg.destroy_context()


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

        dpg.add_plot_legend()
        for axis, color in axis_labels:
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
            dpg.add_button(label="ESTOP", callback=lambda: stop(), width=200)

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
