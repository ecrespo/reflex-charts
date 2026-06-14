"""Demo application for reflex-charts.

Run it from the repository root with::

    reflex run

It renders one card per chart type from :data:`reflex_charts.examples.data.GALLERY`
plus an interactive section that mutates chart data from Reflex state to show
that updates flow from Python to Chart.js reactively.
"""

from __future__ import annotations

import random

import reflex as rx

import reflex_charts as rxc
from reflex_charts.examples.data import GALLERY, MONTHS


class DemoState(rx.State):
    """Drives the interactive, state-bound chart."""

    values: list[int] = [65, 59, 80, 81, 56, 55, 40]
    last_clicked: str = "Click a bar to inspect it."

    @rx.var
    def live_data(self) -> dict:
        """Chart.js data object recomputed whenever ``values`` changes."""
        return rxc.chart_data(
            labels=MONTHS,
            datasets=[rxc.dataset("Live series", self.values, index=0)],
        )

    @rx.event
    def randomize(self):
        """Replace the series with fresh random values."""
        self.values = [random.randint(10, 100) for _ in MONTHS]

    @rx.event
    def on_point_click(self, elements):
        """Handle a click on a bar and report the active element count."""
        count = len(elements) if elements else 0
        self.last_clicked = (
            f"Clicked {count} element(s)." if count else "Clicked empty canvas area."
        )


def chart_card(slug: str) -> rx.Component:
    """Render one gallery example inside a titled card."""
    title, chart_type, builder = GALLERY[slug]
    data, options = builder()
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.box(
                rxc.chart(type=chart_type, data=data, options=options),
                height="280px",
                width="100%",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def gallery() -> rx.Component:
    """A responsive grid of every example chart."""
    return rx.grid(
        *[chart_card(slug) for slug in GALLERY],
        columns=rx.breakpoints(initial="1", sm="2", lg="3"),
        spacing="4",
        width="100%",
    )


def interactive_section() -> rx.Component:
    """A chart wired to Reflex state with randomize + click handling."""
    return rx.card(
        rx.vstack(
            rx.heading("Interactive (state-driven)", size="5"),
            rx.text(DemoState.last_clicked, color_scheme="gray"),
            rx.box(
                rxc.bar(
                    data=DemoState.live_data,
                    options=rxc.options(title="Randomizable bar chart"),
                    on_click=DemoState.on_point_click,
                ),
                height="320px",
                width="100%",
            ),
            rx.button("Randomize data", on_click=DemoState.randomize),
            spacing="3",
            width="100%",
        ),
        width="100%",
    )


def index() -> rx.Component:
    """The single demo page."""
    return rx.container(
        rx.vstack(
            rx.heading("reflex-charts", size="8"),
            rx.text(
                "Chart.js for Reflex — every chart type from pure Python.",
                color_scheme="gray",
                size="4",
            ),
            rx.divider(),
            interactive_section(),
            rx.heading("Gallery", size="6", margin_top="1em"),
            gallery(),
            rx.divider(),
            rx.text(
                "Built with reflex-charts, a wrapper around Chart.js via react-chartjs-2.",
                size="2",
                color_scheme="gray",
            ),
            spacing="5",
            width="100%",
            padding_y="2em",
        ),
        size="4",
    )


app = rx.App()
app.add_page(index, title="reflex-charts demo")
