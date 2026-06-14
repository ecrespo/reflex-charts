"""reflex-charts: a pure-Python Reflex wrapper around Chart.js.

Wraps `react-chartjs-2 <https://react-chartjs-2.js.org>`_ (the React bindings
for `Chart.js <https://www.chartjs.org>`_) as a Reflex custom component, so the
full Chart.js feature set is usable from Python without writing any JavaScript.

Quick start::

    import reflex as rx
    import reflex_charts as rxc

    data = rxc.chart_data(
        labels=["Jan", "Feb", "Mar"],
        datasets=[rxc.dataset("Sales", [10, 25, 18])],
    )

    def index() -> rx.Component:
        return rx.box(
            rxc.line(data=data, options=rxc.options(title="Monthly sales")),
            height="320px",
        )

Every chart type (line, bar, radar, doughnut, pie, polarArea, bubble, scatter)
is available either through the generic :func:`chart` factory or its named
helper. The :func:`dataset`, :func:`categorical_dataset`, :func:`chart_data`
and :func:`options` builders are optional sugar over raw Chart.js dicts.
"""

from __future__ import annotations

from .chart import (
    ChartCanvas,
    bar,
    bubble,
    chart,
    doughnut,
    line,
    pie,
    polar_area,
    radar,
    scatter,
)
from .constants import CHART_TYPES, PALETTE
from .helpers import categorical_dataset, chart_data, dataset, options

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # component
    "ChartCanvas",
    # factories
    "chart",
    "line",
    "bar",
    "radar",
    "doughnut",
    "pie",
    "polar_area",
    "bubble",
    "scatter",
    # builders
    "dataset",
    "categorical_dataset",
    "chart_data",
    "options",
    # constants
    "CHART_TYPES",
    "PALETTE",
]
