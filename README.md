# reflex-charts

**Chart.js for [Reflex](https://reflex.dev) — every chart type, from pure Python.**

`reflex-charts` is a Reflex custom component that wraps
[Chart.js](https://www.chartjs.org) (via its React bindings,
[react-chartjs-2](https://react-chartjs-2.js.org)). It exposes the full Chart.js
feature set through a small, Pythonic API so you can build interactive,
reactive charts in a Reflex app without writing any JavaScript.

> Status: **v0.1.0 — foundation.** Base wrapper, generic component, typed
> factories, data builders, and a demo gallery covering every chart type.

## Features

- **All eight Chart.js types** from one versatile component: line, bar, radar,
  doughnut, pie, polar area, bubble, scatter — plus area, horizontal bar and
  mixed variants.
- **Pure Python.** Configure charts with `data`/`options` dicts that mirror the
  Chart.js docs one-to-one. Any chartjs.org example pastes straight in.
- **Reactive.** Bind chart data to `rx.State` computed vars; charts update when
  state changes.
- **Interactive.** Surface the canvas `on_click` event (with the clicked
  elements) as a Reflex event handler.
- **Zero setup.** All Chart.js controllers, scales and plugins are registered
  automatically — no manual `Chart.register(...)`.
- **Optional builders** for datasets, palettes and options; raw dicts always work.

## Install

```bash
pip install reflex-charts        # once published to PyPI
# or from a clone:
pip install -e .
```

Requires Reflex ≥ 0.8.6 and Python ≥ 3.11.

## Quick start

```python
import reflex as rx
import reflex_charts as rxc

data = rxc.chart_data(
    labels=["Jan", "Feb", "Mar", "Apr"],
    datasets=[rxc.dataset("Sales", [10, 25, 18, 30], tension=0.3)],
)

def index() -> rx.Component:
    return rx.box(
        rxc.line(data=data, options=rxc.options(title="Monthly sales")),
        height="320px",
        width="100%",
    )

app = rx.App()
app.add_page(index)
```

Put charts in a **fixed-height box** — the `options()` builder sets
`maintainAspectRatio=False` so the chart fills its container.

## Chart types

| Factory | Type | Notes |
|---------|------|-------|
| `rxc.line(...)` | `line` | area via dataset `fill` |
| `rxc.bar(...)` | `bar` | horizontal via `options(indexAxis="y")` |
| `rxc.radar(...)` | `radar` | |
| `rxc.doughnut(...)` | `doughnut` | |
| `rxc.pie(...)` | `pie` | |
| `rxc.polar_area(...)` | `polarArea` | |
| `rxc.bubble(...)` | `bubble` | points `{x, y, r}` |
| `rxc.scatter(...)` | `scatter` | points `{x, y}` |
| `rxc.chart(type=..., ...)` | any | generic / mixed / runtime-chosen |

See [`docs/usage.md`](docs/usage.md) for an example of each.

## Run the demo

The package ships a demo app with a gallery of every chart type plus a
state-driven, click-aware interactive example.

```bash
reflex run     # open http://localhost:3000
```

## Project layout

```
reflex-charts/
├── reflex_charts/          # the component package + demo app
│   ├── base.py             # ChartJSBase: deps + Chart.js registration
│   ├── chart.py            # ChartCanvas + typed factories
│   ├── helpers.py          # dataset / chart_data / options builders
│   ├── constants.py        # npm pins, chart types, palette
│   ├── examples/data.py    # canonical sample figures
│   └── reflex_charts.py    # demo app
├── specs/                  # Spec-Driven Design artifacts (see below)
├── docs/usage.md           # usage guide
├── tests/                  # smoke tests
└── scripts/                # GitHub bootstrap helper
```

## Design docs (Spec-Driven Design)

This repository is built spec-first. The full SDD set lives in
[`specs/`](specs/README.md):

- [Specification / PRD](specs/prd/reflex-charts-prd.md)
- [Architecture](specs/technical/architecture.md) (incl. ADRs)
- [Component API v1](specs/api/component-api-v1.md)
- [Data model](specs/data-model/chart-data-schemas.md)
- [Phases](specs/phases/phases.md)
- [Implementation plan](specs/plans/implementation-plan.md)
- [Task breakdown](specs/tasks/task-breakdown.md)

## How it works

Reflex compiles Python components to React. `reflex-charts` declares a component
whose generated JSX is the generic `<Chart>` from `react-chartjs-2`, with
Chart.js registered globally (`Chart.register(...registerables)`) so any `type`
renders. Your `data`/`options` dicts are serialized to props; on interaction,
Chart.js events are forwarded back to your Reflex state. See the
[architecture doc](specs/technical/architecture.md) for the details and the
decision records.

## Acknowledgements

Built on the excellent [Chart.js](https://www.chartjs.org) and
[react-chartjs-2](https://react-chartjs-2.js.org) projects (both MIT licensed —
see [`NOTICE`](NOTICE)) and the [Reflex](https://reflex.dev) framework.

## License

[Apache-2.0](LICENSE) © 2026 Ernesto Crespo.
