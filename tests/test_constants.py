"""Tests for ``reflex_charts.constants``.

Traceability:
- PRD §2 (goal 1): the eight Chart.js chart types must be supported.
- PRD §6 (NFR reproducibility): npm versions are pinned to
  ``chart.js@4.5.0`` and ``react-chartjs-2@5.3.0``.
- API spec §4: ``CHART_TYPES`` and ``PALETTE`` are part of the public surface.
- data-model §4: builders cycle through a colour palette, so an opaque palette
  and its translucent counterpart must stay aligned.
"""

from __future__ import annotations

from reflex_charts import constants


def test_chart_types_are_the_eight_chartjs_controllers():
    # PRD §2: line, bar, radar, doughnut, pie, polarArea, bubble, scatter.
    assert constants.CHART_TYPES == (
        "line",
        "bar",
        "radar",
        "doughnut",
        "pie",
        "polarArea",
        "bubble",
        "scatter",
    )


def test_chart_types_is_an_immutable_tuple_of_eight():
    assert isinstance(constants.CHART_TYPES, tuple)
    assert len(constants.CHART_TYPES) == 8
    # No duplicates.
    assert len(set(constants.CHART_TYPES)) == 8


def test_npm_versions_are_pinned_for_reproducibility():
    # PRD §6 / FR-10: exact pins, not floating ranges.
    assert constants.CHARTJS_NPM == "chart.js@4.5.0"
    assert constants.REACT_CHARTJS_2_NPM == "react-chartjs-2@5.3.0"


def test_palette_is_non_empty_tuple_of_hex_colours():
    assert isinstance(constants.PALETTE, tuple)
    assert len(constants.PALETTE) >= 1
    assert all(c.startswith("#") for c in constants.PALETTE)


def test_palette_alpha_aligns_one_to_one_with_palette():
    # data-model §4: builders pick an opaque colour and its translucent
    # variant by the same index, so the two pools must be the same length.
    assert len(constants.PALETTE_ALPHA) == len(constants.PALETTE)
    assert all(c.startswith("rgba(") for c in constants.PALETTE_ALPHA)