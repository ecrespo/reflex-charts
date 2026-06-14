"""Base wrapper around Chart.js / react-chartjs-2 for Reflex.

This module defines the low-level bridge between Reflex (pure Python) and the
``react-chartjs-2`` React bindings for Chart.js. Every public chart component in
:mod:`reflex_charts` ultimately inherits from :class:`ChartJSBase`.

The base class is responsible for three things:

1. Declaring the npm dependencies (``react-chartjs-2`` and ``chart.js``).
2. Importing the Chart.js registry symbols on the generated frontend.
3. Registering **all** Chart.js controllers, elements, scales and plugins via
   ``ChartJS.register(...registerables)`` so that any chart ``type`` works out
   of the box without the user having to register pieces manually.

Pinning the npm versions keeps generated apps reproducible. Bump the constants
in :mod:`reflex_charts.constants` to upgrade.
"""

from __future__ import annotations

import reflex as rx

from .constants import CHARTJS_NPM, REACT_CHARTJS_2_NPM


class ChartJSBase(rx.Component):
    """Common base for every Chart.js powered Reflex component.

    Subclasses only need to set ``tag`` (the export name from
    ``react-chartjs-2``) and declare the props they accept. The dependency
    wiring and global registration handled here are inherited automatically.
    """

    # The npm package that provides the React bindings.
    library = REACT_CHARTJS_2_NPM

    # Chart.js itself is a peer dependency of react-chartjs-2.
    lib_dependencies: list[str] = [CHARTJS_NPM]

    def add_imports(self) -> dict[str, list[str]]:
        """Import the Chart.js registry helpers on the frontend.

        ``registerables`` is the bundle of all built-in controllers, elements,
        scales and plugins shipped with Chart.js.
        """
        return {"chart.js": ["Chart as ChartJS", "registerables"]}

    def add_custom_code(self) -> list[str]:
        """Register every Chart.js building block exactly once per module.

        Chart.js de-duplicates repeated registrations, so emitting this for each
        component class is safe. It is what lets a single generic ``Chart``
        component render line, bar, radar, doughnut, pie, polar-area, bubble and
        scatter charts interchangeably.
        """
        return ["ChartJS.register(...registerables);"]
