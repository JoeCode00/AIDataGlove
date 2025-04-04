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
