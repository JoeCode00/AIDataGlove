import dearpygui.dearpygui as dpg


def stop_gui():
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
    legend_show=True,
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
        if legend_show:
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


class CalibrationThemes:
    def __init__(self):
        with dpg.theme() as calibrated_0:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, (255, 0, 0), category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core
                )
        with dpg.theme() as calibrated_1:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, (128, 64, 0), category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core
                )
        with dpg.theme() as calibrated_2:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, (64, 128, 0), category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core
                )
        with dpg.theme() as calibrated_3:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, (0, 255, 0), category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core
                )
        self.calibrated_0 = calibrated_0
        self.calibrated_1 = calibrated_1
        self.calibrated_2 = calibrated_2
        self.calibrated_3 = calibrated_3

    def themes(self):
        return [
            self.calibrated_0,
            self.calibrated_1,
            self.calibrated_2,
            self.calibrated_3,
        ]
