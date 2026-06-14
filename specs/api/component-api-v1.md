# Component API — v1

**Status:** Stable for v0.1.0 · **Import root:** `import reflex_charts as rxc`

This is the public Python surface. Anything not listed here is internal and may
change without notice.

## 1. Components

### `ChartCanvas`
The generic Chart.js component. Prefer the factories below; use this directly
only when subclassing.

**Props**

| Prop | Type | Description |
|------|------|-------------|
| `type` | `str` | Chart type; one of `CHART_TYPES`. |
| `data` | `dict` \| `Var[dict]` | Chart.js data object. |
| `options` | `dict` \| `Var[dict]` | Chart.js options object. |
| `plugins` | `list` | Inline Chart.js plugins (advanced). |
| `width` | `int` | Canvas width in px (fallback). |
| `height` | `int` | Canvas height in px (fallback). |
| `on_click` | `EventHandler` | Receives the active elements array of the click. |

## 2. Factories

All factories return an `rx.Component` and accept the same keyword props as
`ChartCanvas` (except `type`, which they set).

```python
rxc.chart(type="bar", data=..., options=...)   # generic
rxc.line(...)        # type="line"   (also area via dataset fill)
rxc.bar(...)         # type="bar"    (horizontal via options indexAxis="y")
rxc.radar(...)       # type="radar"
rxc.doughnut(...)    # type="doughnut"
rxc.pie(...)         # type="pie"
rxc.polar_area(...)  # type="polarArea"
rxc.bubble(...)      # type="bubble"
rxc.scatter(...)     # type="scatter"
```

## 3. Data builders

### `dataset(label, data, *, color=None, background_color=None, border_color=None, fill=None, tension=None, index=0, **extra) -> dict`
Build one Chart.js dataset. Colours default from the palette (cycled by `index`).
`**extra` passes through any native dataset key (`borderWidth`, `stack`, `yAxisID`, …).

### `categorical_dataset(label, data, **extra) -> dict`
Like `dataset`, but assigns a distinct palette colour **per data point** — ideal
for pie/doughnut/polarArea.

### `chart_data(labels, datasets) -> dict`
Assemble `{"labels": [...], "datasets": [...]}`. Pass `labels=None` for scatter
and bubble charts (which use `{x, y[, r]}` points instead of category labels).

### `options(*, title=None, legend=True, legend_position="top", responsive=True, maintain_aspect_ratio=False, **extra) -> dict`
Assemble a Chart.js options object with responsive defaults. `**extra` passes any
native option (`scales`, `animation`, `indexAxis`, `plugins`, …).

## 4. Constants

| Name | Description |
|------|-------------|
| `CHART_TYPES` | Tuple of the 8 supported chart type strings. |
| `PALETTE` | Tuple of default hex colours used by the builders. |

## 5. Usage patterns

### Static chart
```python
import reflex as rx
import reflex_charts as rxc

data = rxc.chart_data(
    labels=["Jan", "Feb", "Mar"],
    datasets=[rxc.dataset("Sales", [10, 25, 18], tension=0.3)],
)

def view() -> rx.Component:
    return rx.box(
        rxc.line(data=data, options=rxc.options(title="Sales")),
        height="320px",
    )
```

### State-bound (reactive) chart
```python
class S(rx.State):
    values: list[int] = [1, 2, 3]

    @rx.var
    def data(self) -> dict:
        return rxc.chart_data(["a", "b", "c"],
                              [rxc.dataset("Live", self.values)])

    @rx.event
    def bump(self):
        self.values = [v + 1 for v in self.values]

def view() -> rx.Component:
    return rx.vstack(
        rx.box(rxc.bar(data=S.data, options=rxc.options()), height="320px"),
        rx.button("Update", on_click=S.bump),
    )
```

### Handling clicks
```python
class S(rx.State):
    msg: str = ""

    @rx.event
    def clicked(self, elements):
        self.msg = f"{len(elements)} element(s) clicked"

rxc.bar(data=..., options=..., on_click=S.clicked)
```

### Raw Chart.js config (no builders)
```python
rxc.chart(
    type="doughnut",
    data={"labels": ["A", "B"], "datasets": [{"data": [1, 2]}]},
    options={"plugins": {"legend": {"position": "right"}}},
)
```

## 6. Stability / versioning

The names in this document are covered by semantic versioning from v0.1.0.
Additive changes (new factories/builders/props) are minor; breaking changes bump
the major version and are recorded in `CHANGELOG.md`.
