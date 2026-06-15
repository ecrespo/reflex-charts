"""Tests for ``reflex_charts.examples.data``.

Traceability:
- FR-9: ship a demo app showcasing every chart type + an interactive example.
- phases P3 / tasks P3: 11 canonical figures registered in ``GALLERY``.
- data-model §3: the chart-type -> required-shape matrix (scatter/bubble have
  no labels and use ``{x, y[, r]}`` points).
"""

from __future__ import annotations

import pytest

from reflex_charts.constants import CHART_TYPES
from reflex_charts.examples import data as ex


EXPECTED_SLUGS = {
    "line",
    "area",
    "bar",
    "horizontal-bar",
    "radar",
    "doughnut",
    "pie",
    "polar-area",
    "bubble",
    "scatter",
    "mixed",
}


def test_gallery_registers_all_eleven_figures():
    # tasks P3: exactly the 11 documented examples.
    assert set(ex.GALLERY) == EXPECTED_SLUGS
    assert len(ex.GALLERY) == 11


@pytest.mark.parametrize("slug", sorted(EXPECTED_SLUGS))
def test_gallery_entry_shape(slug):
    # Each entry is (title, chart_type, builder).
    title, chart_type, builder = ex.GALLERY[slug]
    assert isinstance(title, str) and title
    assert callable(builder)


@pytest.mark.parametrize("slug", sorted(EXPECTED_SLUGS))
def test_gallery_chart_type_is_a_supported_controller(slug):
    # FR-4 / data-model §3: the registered Chart.js controller must be one of
    # the eight supported types (variants like area/horizontal-bar/mixed reuse
    # an underlying controller).
    _title, chart_type, _builder = ex.GALLERY[slug]
    assert chart_type in CHART_TYPES


@pytest.mark.parametrize("slug", sorted(EXPECTED_SLUGS))
def test_builder_returns_data_and_options(slug):
    _title, _type, builder = ex.GALLERY[slug]
    data, options = builder()
    assert isinstance(data, dict)
    assert isinstance(options, dict)
    # data-model §1: at least one dataset, each carrying a ``data`` array.
    assert data["datasets"], "expected at least one dataset"
    for ds in data["datasets"]:
        assert "data" in ds


def test_scatter_and_bubble_have_no_labels():
    # data-model §3: scatter/bubble use {x,y[,r]} points, not category labels.
    for slug in ("scatter", "bubble"):
        data, _opts = ex.GALLERY[slug][2]()
        assert "labels" not in data


def test_point_charts_use_xy_point_dicts():
    scatter_data, _ = ex.GALLERY["scatter"][2]()
    first = scatter_data["datasets"][0]["data"][0]
    assert {"x", "y"} <= set(first)

    bubble_data, _ = ex.GALLERY["bubble"][2]()
    first_bubble = bubble_data["datasets"][0]["data"][0]
    assert {"x", "y", "r"} <= set(first_bubble)


def test_category_charts_align_data_length_with_labels():
    # data-model §3: for category charts, dataset data aligns with labels.
    for slug in ("line", "bar", "radar"):
        data, _ = ex.GALLERY[slug][2]()
        n_labels = len(data["labels"])
        for ds in data["datasets"]:
            assert len(ds["data"]) == n_labels


def test_horizontal_bar_sets_index_axis_y():
    # data-model §3: horizontal bar == bar controller + indexAxis "y".
    _data, opts = ex.GALLERY["horizontal-bar"][2]()
    assert opts["indexAxis"] == "y"


def test_mixed_chart_sets_per_dataset_type():
    # data-model §3: mixed charts carry a per-dataset ``type``.
    data, _ = ex.GALLERY["mixed"][2]()
    types = {ds.get("type") for ds in data["datasets"]}
    assert types == {"bar", "line"}
