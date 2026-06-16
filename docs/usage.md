# Usage guide — reflex-charts

A practical, example-first guide. For the formal contract see
[`../specs/api/component-api-v1.md`](../specs/api/component-api-v1.md).

## Install

```bash
pip install reflex-charts        # once published
# or, from a clone:
pip install -e .
```

Requires Reflex ≥ 0.8.6 and Python ≥ 3.11. The first `reflex run` downloads the
pinned npm packages (`chart.js`, `react-chartjs-2`).

## The mental model

You write two Python dicts — `data` and `options` — exactly as the
[Chart.js docs](https://www.chartjs.org/docs/latest/) describe them, then hand
them to a chart factory. Optional builders save you typing.

## One chart, eight types

```python
import reflex as rx
import reflex_charts as rxc

labels = ["Q1", "Q2", "Q3", "Q4"]

def panel() -> rx.Component:
    return rx.grid(
        rx.box(rxc.line(   data=rxc.chart_data(labels, [rxc.dataset("A", [1,3,2,5])]),
                           options=rxc.options(title="Line")), height="260px"),
        rx.box(rxc.bar(    data=rxc.chart_data(labels, [rxc.dataset("A", [1,3,2,5])]),
                           options=rxc.options(title="Bar")), height="260px"),
        rx.box(rxc.pie(    data=rxc.chart_data(labels, [rxc.categorical_dataset("A", [1,3,2,5])]),
                           options=rxc.options(title="Pie")), height="260px"),
        columns="3", spacing="4",
    )
```

## Area chart (filled line)

```python
rxc.line(
    data=rxc.chart_data(labels, [rxc.dataset("Filled", [1,3,2,5], fill="origin", tension=0.4)]),
    options=rxc.options(title="Area"),
)
```

## Horizontal bar

```python
rxc.bar(
    data=rxc.chart_data(labels, [rxc.dataset("A", [1,3,2,5])]),
    options=rxc.options(indexAxis="y"),
)
```

## Scatter & bubble (no labels)

```python
rxc.scatter(
    data=rxc.chart_data(None, [rxc.dataset("pts", [{"x": 1, "y": 2}, {"x": 3, "y": 1}])]),
    options=rxc.options(scales={"x": {"type": "linear", "position": "bottom"}}),
)

rxc.bubble(
    data=rxc.chart_data(None, [rxc.dataset("b", [{"x": 1, "y": 2, "r": 12}])]),
    options=rxc.options(),
)
```

## Reactive data with state

```python
class S(rx.State):
    values: list[int] = [5, 9, 3, 7]

    @rx.var
    def data(self) -> dict:
        return rxc.chart_data(["a","b","c","d"], [rxc.dataset("Live", self.values)])

    @rx.event
    def shuffle(self):
        import random
        self.values = [random.randint(1, 10) for _ in self.values]

def live() -> rx.Component:
    return rx.vstack(
        rx.box(rxc.bar(data=S.data, options=rxc.options()), height="320px"),
        rx.button("Shuffle", on_click=S.shuffle),
    )
```

## Reacting to clicks

```python
class S(rx.State):
    note: str = ""

    @rx.event
    def on_pick(self, elements):
        self.note = f"{len(elements)} element(s) clicked"

rxc.bar(data=..., options=..., on_click=S.on_pick)
```

## Dropping to raw Chart.js

Builders are optional. Any config from chartjs.org works verbatim:

```python
rxc.chart(
    type="radar",
    data={"labels": ["a","b","c"], "datasets": [{"label": "x", "data": [1,2,3]}]},
    options={"scales": {"r": {"beginAtZero": True}}},
)
```

## Layout tip

Always put a chart in a fixed-height box. The `options()` builder sets
`maintainAspectRatio=False`, so the chart fills its container:

```python
rx.box(rxc.line(data=..., options=rxc.options()), height="320px", width="100%")
```

## Run the demo

The demo is a standalone Reflex app under `reflex_charts_demo/`:

```bash
pip install -e .          # install the component
cd reflex_charts_demo
reflex run               # then open http://localhost:3000
```
