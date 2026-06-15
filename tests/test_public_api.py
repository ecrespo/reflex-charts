"""Tests pinning the public API surface to ``specs/api/component-api-v1.md``.

Traceability:
- API spec §1–§4: the documented public names (component, factories, builders,
  constants).
- API spec §6: names are covered by semantic versioning from v0.1.0, so the
  package ``__version__`` must agree with the packaging metadata.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import reflex_charts as rxc

# The exact public surface documented in component-api-v1.md.
DOCUMENTED_COMPONENTS = {"ChartCanvas"}
DOCUMENTED_FACTORIES = {
    "chart",
    "line",
    "bar",
    "radar",
    "doughnut",
    "pie",
    "polar_area",
    "bubble",
    "scatter",
}
DOCUMENTED_BUILDERS = {"dataset", "categorical_dataset", "chart_data", "options"}
DOCUMENTED_CONSTANTS = {"CHART_TYPES", "PALETTE"}

DOCUMENTED_SURFACE = (
    DOCUMENTED_COMPONENTS
    | DOCUMENTED_FACTORIES
    | DOCUMENTED_BUILDERS
    | DOCUMENTED_CONSTANTS
)


def test_every_documented_name_is_importable():
    for name in DOCUMENTED_SURFACE:
        assert hasattr(rxc, name), f"missing documented public symbol: {name}"


def test_documented_names_are_advertised_in_dunder_all():
    exported = set(rxc.__all__)
    missing = DOCUMENTED_SURFACE - exported
    assert not missing, f"documented but not in __all__: {sorted(missing)}"


def test_factories_and_builders_are_callable():
    for name in DOCUMENTED_FACTORIES | DOCUMENTED_BUILDERS:
        assert callable(getattr(rxc, name)), f"{name} should be callable"


def test_version_is_declared():
    assert rxc.__version__ == "0.1.0"


def test_version_matches_packaging_metadata():
    # API spec §6: semantic versioning from v0.1.0 -> package and pyproject agree.
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    meta = tomllib.loads(pyproject.read_text())
    assert rxc.__version__ == meta["project"]["version"]
