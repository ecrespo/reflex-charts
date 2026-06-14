"""Smoke tests that exercise the public API without a running frontend.

These avoid importing Reflex's heavy app machinery where possible; they verify
that the package exposes its documented surface and that the pure-Python data
builders produce well-formed Chart.js dictionaries.
"""

from __future__ import annotations


def test_public_api_exports():
    import reflex_charts as rxc

    for name in (
        "chart",
        "line",
        "bar",
        "radar",
        "doughnut",
        "pie",
        "polar_area",
        "bubble",
        "scatter",
        "dataset",
        "categorical_dataset",
        "chart_data",
        "options",
    ):
        assert hasattr(rxc, name), f"missing public symbol: {name}"


def test_chart_types_constant():
    from reflex_charts.constants import CHART_TYPES

    assert "line" in CHART_TYPES
    assert "polarArea" in CHART_TYPES
    assert len(CHART_TYPES) == 8


def test_dataset_builder_colors_cycle():
    from reflex_charts.helpers import dataset

    ds = dataset("Sales", [1, 2, 3], index=0)
    assert ds["label"] == "Sales"
    assert ds["data"] == [1, 2, 3]
    assert "borderColor" in ds and "backgroundColor" in ds


def test_chart_data_shape():
    from reflex_charts.helpers import chart_data, dataset

    data = chart_data(["a", "b"], [dataset("s", [1, 2])])
    assert data["labels"] == ["a", "b"]
    assert isinstance(data["datasets"], list) and len(data["datasets"]) == 1


def test_chart_data_without_labels():
    from reflex_charts.helpers import chart_data, dataset

    data = chart_data(None, [dataset("pts", [{"x": 1, "y": 2}])])
    assert "labels" not in data


def test_options_builder():
    from reflex_charts.helpers import options

    opts = options(title="T", legend_position="bottom")
    assert opts["responsive"] is True
    assert opts["plugins"]["title"]["text"] == "T"
    assert opts["plugins"]["legend"]["position"] == "bottom"
