"""Ergonomic builders for Chart.js ``data`` and ``options`` dictionaries.

Chart.js is configured entirely through nested dictionaries. Writing them by
hand is verbose and error-prone, so these helpers assemble correct structures
while still letting power users drop down to raw dicts whenever they want. None
of them are required — every chart component also accepts plain Chart.js dicts.
"""

from __future__ import annotations

from typing import Any, Iterable, Sequence

from .constants import PALETTE, PALETTE_ALPHA


def _color(index: int, alpha: bool = False) -> str:
    """Return a palette colour, cycling when the index exceeds the palette size."""
    pool = PALETTE_ALPHA if alpha else PALETTE
    return pool[index % len(pool)]


def dataset(
    label: str,
    data: Sequence[Any],
    *,
    color: str | None = None,
    background_color: str | list[str] | None = None,
    border_color: str | list[str] | None = None,
    fill: bool | str | None = None,
    tension: float | None = None,
    index: int = 0,
    **extra: Any,
) -> dict[str, Any]:
    """Build a single Chart.js dataset dictionary.

    Args:
        label: Legend label for the series.
        data: The numeric values (or ``{x, y[, r]}`` points for scatter/bubble).
        color: Convenience that sets both border and background from one colour.
        background_color: Explicit fill colour(s).
        border_color: Explicit line/border colour(s).
        fill: Area-fill behaviour for line charts.
        tension: Bezier curve tension for line charts (0 = straight).
        index: Palette index used when no colours are supplied.
        **extra: Any other native dataset key (e.g. ``borderWidth``, ``stack``).

    Returns:
        A dataset dict ready to be placed in ``data["datasets"]``.
    """
    ds: dict[str, Any] = {"label": label, "data": list(data)}

    base = color or _color(index)
    ds["borderColor"] = border_color if border_color is not None else base
    ds["backgroundColor"] = (
        background_color if background_color is not None else (color or _color(index, alpha=True))
    )

    if fill is not None:
        ds["fill"] = fill
    if tension is not None:
        ds["tension"] = tension

    ds.update(extra)
    return ds


def categorical_dataset(
    label: str,
    data: Sequence[Any],
    **extra: Any,
) -> dict[str, Any]:
    """Build a dataset where each slice/bar gets its own palette colour.

    Ideal for pie, doughnut and polar-area charts, where colours map to
    categories rather than to a single series.
    """
    n = len(list(data))
    ds: dict[str, Any] = {
        "label": label,
        "data": list(data),
        "backgroundColor": [_color(i, alpha=True) for i in range(n)],
        "borderColor": [_color(i) for i in range(n)],
        "borderWidth": 1,
    }
    ds.update(extra)
    return ds


def chart_data(
    labels: Iterable[Any] | None,
    datasets: list[dict[str, Any]],
) -> dict[str, Any]:
    """Assemble the top-level Chart.js ``data`` object.

    Args:
        labels: Category labels (omit/None for scatter & bubble charts).
        datasets: A list of dataset dicts, e.g. from :func:`dataset`.

    Returns:
        ``{"labels": [...], "datasets": [...]}``.
    """
    data: dict[str, Any] = {"datasets": datasets}
    if labels is not None:
        data["labels"] = list(labels)
    return data


def options(
    *,
    title: str | None = None,
    legend: bool = True,
    legend_position: str = "top",
    responsive: bool = True,
    maintain_aspect_ratio: bool = False,
    **extra: Any,
) -> dict[str, Any]:
    """Assemble a common Chart.js ``options`` object.

    Sensible defaults are applied for responsive layout (the chart fills its
    container) while still exposing every native option through ``extra``.

    Args:
        title: Optional chart title.
        legend: Whether to show the legend.
        legend_position: ``top`` | ``bottom`` | ``left`` | ``right``.
        responsive: Resize with the container.
        maintain_aspect_ratio: Keep width/height ratio (usually False so the
            chart fills a fixed-height box).
        **extra: Any other native option (e.g. ``scales``, ``animation``).

    Returns:
        A Chart.js options dict.
    """
    plugins: dict[str, Any] = {"legend": {"display": legend, "position": legend_position}}
    if title is not None:
        plugins["title"] = {"display": True, "text": title}

    opts: dict[str, Any] = {
        "responsive": responsive,
        "maintainAspectRatio": maintain_aspect_ratio,
        "plugins": plugins,
    }
    opts.update(extra)
    return opts
