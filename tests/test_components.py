"""Tests for the component layer (``chart.py`` factories + ``base.py`` wiring).

These exercise the Reflex components in pure Python (no ``reflex run`` needed):
Reflex builds the component objects eagerly, so props and the dependency /
registration wiring are all introspectable.

Traceability:
- FR-1: render any Chart.js ``type`` from one generic component.
- FR-3: named factory helpers per chart type.
- FR-4: register all Chart.js controllers/elements/scales/plugins automatically.
- FR-7: surface the canvas ``on_click`` event.
- FR-10: pin npm dependency versions.
- architecture §2/§3/§4/§7 and ADR-001..003.
"""

from __future__ import annotations

import json

import pytest

import reflex_charts as rxc
from reflex_charts.base import ChartJSBase
from reflex_charts.chart import ChartCanvas
from reflex_charts.constants import CHARTJS_NPM, REACT_CHARTJS_2_NPM


def _type_of(component) -> str:
    """Read the literal value of the component's ``type`` Var."""
    var = component.type
    value = getattr(var, "_var_value", None)
    if value is not None:
        return value
    return json.loads(var._js_expr)


# --- factories set the right controller type ------------------------------ #
FACTORY_TYPE = [
    (rxc.line, "line"),
    (rxc.bar, "bar"),
    (rxc.radar, "radar"),
    (rxc.doughnut, "doughnut"),
    (rxc.pie, "pie"),
    (rxc.polar_area, "polarArea"),
    (rxc.bubble, "bubble"),
    (rxc.scatter, "scatter"),
]


@pytest.mark.parametrize("factory, expected_type", FACTORY_TYPE)
def test_named_factory_sets_its_chart_type(factory, expected_type):
    # FR-3: each helper pre-fills ``type``.
    component = factory(data={"datasets": []}, options={})
    assert isinstance(component, ChartCanvas)
    assert _type_of(component) == expected_type


def test_generic_chart_factory_honours_requested_type():
    # FR-1: one generic component renders any type.
    component = rxc.chart(type="polarArea", data={"datasets": []}, options={})
    assert _type_of(component) == "polarArea"


def test_factory_passes_data_and_options_through():
    data = {"labels": ["a"], "datasets": [{"data": [1]}]}
    component = rxc.bar(data=data, options={"responsive": True})
    assert component.data is not None
    assert component.options is not None


# --- base wiring (ADR-001 / ADR-003) -------------------------------------- #
def test_charts_wrap_the_generic_react_chartjs_2_component():
    # architecture §3: we wrap the single generic ``Chart`` export.
    assert ChartCanvas.tag == "Chart"


def test_base_declares_pinned_npm_dependencies():
    # ADR-001 + FR-10: react-chartjs-2 is the library, chart.js a peer dep,
    # both pinned.
    component = rxc.line(data={"datasets": []}, options={})
    assert component.library == REACT_CHARTJS_2_NPM
    assert CHARTJS_NPM in component.lib_dependencies


def test_base_imports_chartjs_registry_symbols():
    # architecture §4: import Chart + registerables on the frontend.
    component = rxc.line(data={"datasets": []}, options={})
    imports = component.add_imports()
    assert "chart.js" in imports
    assert "Chart as ChartJS" in imports["chart.js"]
    assert "registerables" in imports["chart.js"]


def test_base_registers_all_registerables_once():
    # ADR-003 / FR-4: auto-register everything so any type works zero-config.
    component = rxc.line(data={"datasets": []}, options={})
    code = component.add_custom_code()
    assert any("register(...registerables)" in line for line in code)


def test_chartcanvas_inherits_from_chartjs_base():
    assert issubclass(ChartCanvas, ChartJSBase)


# --- events (FR-7) -------------------------------------------------------- #
def test_on_click_is_an_exposed_event_trigger():
    # FR-7 / architecture §7: surface the canvas click.
    component = rxc.bar(data={"datasets": []}, options={})
    assert "on_click" in component.get_event_triggers()
