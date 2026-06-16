"""Static example data mirroring the canonical chartjs.org samples.

Each function returns a ``(data, options)`` tuple so the demo pages stay tiny.
These intentionally reuse the public builders in :mod:`reflex_charts.helpers`
to double as documentation of the recommended API.
"""

from __future__ import annotations

from typing import Any

from ..helpers import categorical_dataset, chart_data, dataset, options

MONTHS = ["January", "February", "March", "April", "May", "June", "July"]


def line_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Multi-series line chart."""
    data = chart_data(
        labels=MONTHS,
        datasets=[
            dataset("Dataset 1", [65, 59, 80, 81, 56, 55, 40], index=0, tension=0.3),
            dataset("Dataset 2", [28, 48, 40, 19, 86, 27, 90], index=1, tension=0.3),
        ],
    )
    return data, options(title="Line chart")


def area_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Filled line chart (area)."""
    data = chart_data(
        labels=MONTHS,
        datasets=[
            dataset("Filled", [65, 59, 80, 81, 56, 55, 40], index=4, fill="origin", tension=0.4),
        ],
    )
    return data, options(title="Area chart")


def bar_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Grouped vertical bar chart."""
    data = chart_data(
        labels=MONTHS,
        datasets=[
            dataset("Dataset 1", [65, 59, 80, 81, 56, 55, 40], index=0),
            dataset("Dataset 2", [28, 48, 40, 19, 86, 27, 90], index=1),
        ],
    )
    return data, options(title="Bar chart")


def horizontal_bar_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Horizontal bar chart via ``indexAxis: 'y'``."""
    data = chart_data(
        labels=MONTHS,
        datasets=[dataset("Dataset 1", [65, 59, 80, 81, 56, 55, 40], index=2)],
    )
    return data, options(title="Horizontal bar", indexAxis="y")


def radar_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Radar chart comparing two profiles."""
    labels = ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"]
    data = chart_data(
        labels=labels,
        datasets=[
            dataset("Dataset 1", [65, 59, 90, 81, 56, 55, 40], index=0, fill=True),
            dataset("Dataset 2", [28, 48, 40, 19, 96, 27, 100], index=1, fill=True),
        ],
    )
    return data, options(title="Radar chart")


def doughnut_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Doughnut chart."""
    data = chart_data(
        labels=["Red", "Blue", "Yellow"],
        datasets=[categorical_dataset("Votes", [300, 50, 100])],
    )
    return data, options(title="Doughnut chart")


def pie_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Pie chart."""
    data = chart_data(
        labels=["Red", "Blue", "Yellow", "Green", "Purple"],
        datasets=[categorical_dataset("Votes", [12, 19, 3, 5, 2])],
    )
    return data, options(title="Pie chart")


def polar_area_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Polar-area chart."""
    data = chart_data(
        labels=["Red", "Green", "Yellow", "Grey", "Blue"],
        datasets=[categorical_dataset("Series", [11, 16, 7, 3, 14])],
    )
    return data, options(title="Polar area chart")


def bubble_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Bubble chart of ``{x, y, r}`` points."""
    points = [
        {"x": 20, "y": 30, "r": 15},
        {"x": 40, "y": 10, "r": 10},
        {"x": 30, "y": 20, "r": 25},
        {"x": 10, "y": 40, "r": 8},
    ]
    data = chart_data(labels=None, datasets=[dataset("Bubbles", points, index=5)])
    return data, options(title="Bubble chart")


def scatter_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Scatter chart of ``{x, y}`` points."""
    points = [
        {"x": -10, "y": 0},
        {"x": 0, "y": 10},
        {"x": 10, "y": 5},
        {"x": 8, "y": -2},
        {"x": -5, "y": -8},
    ]
    data = chart_data(labels=None, datasets=[dataset("Scatter", points, index=1)])
    return data, options(
        title="Scatter chart",
        scales={"x": {"type": "linear", "position": "bottom"}},
    )


def mixed_example() -> tuple[dict[str, Any], dict[str, Any]]:
    """Mixed bar + line chart sharing one axis."""
    data = chart_data(
        labels=MONTHS,
        datasets=[
            {**dataset("Bar", [65, 59, 80, 81, 56, 55, 40], index=0), "type": "bar"},
            {**dataset("Line", [28, 48, 40, 19, 86, 27, 90], index=1, tension=0.3), "type": "line"},
        ],
    )
    return data, options(title="Mixed chart")


#: Registry consumed by the demo app: slug -> (title, chart-type, builder).
GALLERY: dict[str, tuple[str, str, Any]] = {
    "line": ("Line", "line", line_example),
    "area": ("Area", "line", area_example),
    "bar": ("Bar", "bar", bar_example),
    "horizontal-bar": ("Horizontal bar", "bar", horizontal_bar_example),
    "radar": ("Radar", "radar", radar_example),
    "doughnut": ("Doughnut", "doughnut", doughnut_example),
    "pie": ("Pie", "pie", pie_example),
    "polar-area": ("Polar area", "polarArea", polar_area_example),
    "bubble": ("Bubble", "bubble", bubble_example),
    "scatter": ("Scatter", "scatter", scatter_example),
    "mixed": ("Mixed", "bar", mixed_example),
}
