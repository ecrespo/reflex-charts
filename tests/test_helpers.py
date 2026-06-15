"""Tests for the ``reflex_charts.helpers`` builders.

Traceability:
- API spec §3: signatures and documented behaviour of ``dataset``,
  ``categorical_dataset``, ``chart_data``, ``options``.
- data-model §1–§2: the dict shapes these builders must emit.
- FR-5 (builders) and FR-6 (default palette with cycling).
"""

from __future__ import annotations

from reflex_charts import constants
from reflex_charts.helpers import (
    categorical_dataset,
    chart_data,
    dataset,
    options,
)


# --- dataset() ------------------------------------------------------------ #
def test_dataset_keeps_label_and_copies_data():
    ds = dataset("Sales", [1, 2, 3])
    assert ds["label"] == "Sales"
    assert ds["data"] == [1, 2, 3]


def test_dataset_data_is_a_new_list_not_the_caller_reference():
    # data-model: ``data`` is a plain list; builders should not alias caller
    # state (important when a value comes from rx.State).
    src = [1, 2, 3]
    ds = dataset("S", src)
    src.append(99)
    assert ds["data"] == [1, 2, 3]


def test_dataset_defaults_colours_from_palette_by_index():
    # FR-6: no colour supplied -> opaque border + translucent background by index.
    ds = dataset("S", [1], index=1)
    assert ds["borderColor"] == constants.PALETTE[1]
    assert ds["backgroundColor"] == constants.PALETTE_ALPHA[1]


def test_dataset_palette_cycles_when_index_exceeds_palette():
    # FR-6: index beyond the palette wraps around (modulo).
    n = len(constants.PALETTE)
    ds = dataset("S", [1], index=n + 2)
    assert ds["borderColor"] == constants.PALETTE[2]


def test_dataset_color_sets_both_border_and_background():
    # API §3: ``color`` is a convenience that sets both from one colour.
    ds = dataset("S", [1], color="#123456")
    assert ds["borderColor"] == "#123456"
    assert ds["backgroundColor"] == "#123456"


def test_dataset_explicit_border_and_background_override_palette():
    ds = dataset("S", [1], border_color="#aaa", background_color="#bbb", index=0)
    assert ds["borderColor"] == "#aaa"
    assert ds["backgroundColor"] == "#bbb"


def test_dataset_omits_fill_and_tension_unless_provided():
    ds = dataset("S", [1])
    assert "fill" not in ds
    assert "tension" not in ds


def test_dataset_includes_fill_and_tension_when_provided():
    ds = dataset("S", [1], fill="origin", tension=0.4)
    assert ds["fill"] == "origin"
    assert ds["tension"] == 0.4


def test_dataset_extra_keys_pass_through():
    # API §3: ``**extra`` passes through any native dataset key.
    ds = dataset("S", [1], borderWidth=3, stack="group-a", yAxisID="y2")
    assert ds["borderWidth"] == 3
    assert ds["stack"] == "group-a"
    assert ds["yAxisID"] == "y2"


# --- categorical_dataset() ------------------------------------------------ #
def test_categorical_dataset_assigns_one_colour_per_point():
    # data-model §4: per-point colours for pie/doughnut/polarArea.
    ds = categorical_dataset("Votes", [10, 20, 30])
    assert isinstance(ds["backgroundColor"], list)
    assert isinstance(ds["borderColor"], list)
    assert len(ds["backgroundColor"]) == 3
    assert len(ds["borderColor"]) == 3


def test_categorical_dataset_colours_follow_palette_order():
    ds = categorical_dataset("Votes", [1, 2])
    assert ds["borderColor"] == [constants.PALETTE[0], constants.PALETTE[1]]
    assert ds["backgroundColor"] == [
        constants.PALETTE_ALPHA[0],
        constants.PALETTE_ALPHA[1],
    ]


def test_categorical_dataset_has_border_width_and_passes_extra():
    ds = categorical_dataset("Votes", [1], hoverOffset=8)
    assert ds["borderWidth"] == 1
    assert ds["hoverOffset"] == 8


# --- chart_data() --------------------------------------------------------- #
def test_chart_data_includes_labels_when_given():
    data = chart_data(["a", "b"], [dataset("s", [1, 2])])
    assert data["labels"] == ["a", "b"]
    assert len(data["datasets"]) == 1


def test_chart_data_omits_labels_for_scatter_and_bubble():
    # data-model §1: omit ``labels`` for scatter/bubble (None sentinel).
    data = chart_data(None, [dataset("pts", [{"x": 1, "y": 2}])])
    assert "labels" not in data
    assert "datasets" in data


# --- options() ------------------------------------------------------------ #
def test_options_responsive_defaults():
    # data-model §2 / architecture §8: responsive True, maintainAspectRatio False.
    opts = options()
    assert opts["responsive"] is True
    assert opts["maintainAspectRatio"] is False


def test_options_legend_defaults_to_top_and_visible():
    opts = options()
    assert opts["plugins"]["legend"] == {"display": True, "position": "top"}


def test_options_can_disable_legend_and_move_it():
    opts = options(legend=False, legend_position="right")
    assert opts["plugins"]["legend"]["display"] is False
    assert opts["plugins"]["legend"]["position"] == "right"


def test_options_title_only_present_when_set():
    assert "title" not in options()["plugins"]
    titled = options(title="Sales")
    assert titled["plugins"]["title"] == {"display": True, "text": "Sales"}


def test_options_extra_keys_pass_through():
    # API §3: native options like indexAxis / scales pass through.
    opts = options(indexAxis="y", scales={"y": {"beginAtZero": True}})
    assert opts["indexAxis"] == "y"
    assert opts["scales"]["y"]["beginAtZero"] is True