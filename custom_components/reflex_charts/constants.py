"""Pinned dependency versions, chart-type registry and default palettes.

Centralising these values keeps the rest of the package free of magic strings
and makes dependency upgrades a one-line change.
"""

from __future__ import annotations

# --- npm dependency pins -------------------------------------------------- #
# Bump these to upgrade the underlying JavaScript libraries. They are injected
# into the generated package.json by Reflex.
CHARTJS_NPM = "chart.js@4.5.0"
REACT_CHARTJS_2_NPM = "react-chartjs-2@5.3.0"

# --- supported chart types ------------------------------------------------ #
# These are the eight controller types Chart.js ships with. Every one is usable
# through the generic ``chart()`` factory or its named helper.
CHART_TYPES: tuple[str, ...] = (
    "line",
    "bar",
    "radar",
    "doughnut",
    "pie",
    "polarArea",
    "bubble",
    "scatter",
)

# --- default colour palette ----------------------------------------------- #
# A categorical palette inspired by the Chart.js documentation examples. The
# helpers in :mod:`reflex_charts.helpers` cycle through these for datasets that
# do not specify their own colours.
PALETTE: tuple[str, ...] = (
    "#36a2eb",  # blue
    "#ff6384",  # red
    "#ff9f40",  # orange
    "#ffcd56",  # yellow
    "#4bc0c0",  # teal
    "#9966ff",  # purple
    "#c9cbcf",  # grey
    "#2ecc71",  # green
)

# Translucent variants (RGBA) used for fills/backgrounds.
PALETTE_ALPHA: tuple[str, ...] = (
    "rgba(54, 162, 235, 0.5)",
    "rgba(255, 99, 132, 0.5)",
    "rgba(255, 159, 64, 0.5)",
    "rgba(255, 205, 86, 0.5)",
    "rgba(75, 192, 192, 0.5)",
    "rgba(153, 102, 255, 0.5)",
    "rgba(201, 203, 207, 0.5)",
    "rgba(46, 204, 113, 0.5)",
)
