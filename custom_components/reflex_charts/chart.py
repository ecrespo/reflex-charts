"""The generic Chart.js component and its typed convenience factories.

The package is intentionally built around a *single* versatile component,
:class:`ChartCanvas`, which wraps the generic ``Chart`` export of
``react-chartjs-2``. Because the base class registers every Chart.js controller
(see :mod:`reflex_charts.base`), one component can render any chart ``type``.

Two usage styles are offered:

* The generic factory ``chart(type="bar", data=..., options=...)``.
* Named helpers ``line``, ``bar``, ``radar``, ``doughnut``, ``pie``,
  ``polar_area``, ``bubble`` and ``scatter`` that pre-fill ``type`` for you.

All of them accept the same ``data`` / ``options`` dictionaries that the Chart.js
documentation uses, so any example from chartjs.org translates directly.
"""

from __future__ import annotations

import reflex as rx
from reflex.vars import Var

from .base import ChartJSBase


class ChartCanvas(ChartJSBase):
    """A single, type-agnostic Chart.js canvas.

    Mirrors the props of the generic ``<Chart>`` component from
    ``react-chartjs-2``. The ``data`` and ``options`` props accept the exact
    object shapes documented at https://www.chartjs.org, passed as plain Python
    dictionaries (or state Vars resolving to dictionaries).
    """

    # Named export ``Chart`` from react-chartjs-2 (not a default export).
    tag = "Chart"

    # The chart controller to use: one of reflex_charts.constants.CHART_TYPES.
    type: Var[str]

    # Chart.js ``data`` object: ``{"labels": [...], "datasets": [...]}``.
    data: Var[dict]

    # Chart.js ``options`` object (scales, plugins, animations, ...).
    options: Var[dict]

    # Per-chart inline plugins (advanced; usually configured via options).
    plugins: Var[list]

    # Fallback width/height in pixels when the parent does not constrain size.
    width: Var[int]
    height: Var[int]

    # Native canvas click. The Chart.js onClick receives
    # ``(event, activeElements, chart)``; we surface the active elements so a
    # Reflex state handler can react to clicked datapoints.
    on_click: rx.EventHandler[lambda event, elements: [elements]]


# --- factories ------------------------------------------------------------ #
def chart(type: str = "line", **props) -> rx.Component:  # noqa: A002 - mirrors JS prop
    """Create a chart of an arbitrary ``type``.

    Args:
        type: One of ``reflex_charts.constants.CHART_TYPES``.
        **props: ``data``, ``options`` and any other supported prop.

    Returns:
        A Reflex component instance.
    """
    return ChartCanvas.create(type=type, **props)


def line(**props) -> rx.Component:
    """Line chart (also the base for filled *area* charts via dataset ``fill``)."""
    return ChartCanvas.create(type="line", **props)


def bar(**props) -> rx.Component:
    """Vertical or horizontal bar chart (set ``indexAxis: 'y'`` in options)."""
    return ChartCanvas.create(type="bar", **props)


def radar(**props) -> rx.Component:
    """Radar (spider) chart."""
    return ChartCanvas.create(type="radar", **props)


def doughnut(**props) -> rx.Component:
    """Doughnut chart."""
    return ChartCanvas.create(type="doughnut", **props)


def pie(**props) -> rx.Component:
    """Pie chart."""
    return ChartCanvas.create(type="pie", **props)


def polar_area(**props) -> rx.Component:
    """Polar-area chart."""
    return ChartCanvas.create(type="polarArea", **props)


def bubble(**props) -> rx.Component:
    """Bubble chart (datasets of ``{x, y, r}`` points)."""
    return ChartCanvas.create(type="bubble", **props)


def scatter(**props) -> rx.Component:
    """Scatter chart (datasets of ``{x, y}`` points)."""
    return ChartCanvas.create(type="scatter", **props)
