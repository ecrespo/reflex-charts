# Data model — Chart.js schemas as used by reflex-charts

**Status:** v1 · **Last updated:** 2026-06-14

`reflex-charts` does not invent a data model; it passes Chart.js `data` and
`options` objects straight through. This document captures the **subset and
conventions** the package relies on so the builders and examples stay consistent.

## 1. `data` object

```
data = {
    "labels":   [str | number, ...],   # optional; omit for scatter/bubble
    "datasets": [ <dataset>, ... ],     # required, 1..n
}
```

### Dataset (category charts: line, bar, radar, pie, doughnut, polarArea)
```
dataset = {
    "label":           str,
    "data":            [number, ...],         # aligned with labels
    "borderColor":     str | [str, ...],
    "backgroundColor": str | [str, ...],
    # optional, per chart type:
    "fill":            bool | str,            # line/area
    "tension":         number,                # line curve (0..1)
    "borderWidth":     number,
    "stack":           str,                   # grouped/stacked bar
    "type":            str,                    # per-dataset type (mixed charts)
}
```

### Dataset (scatter)
```
dataset = { "label": str, "data": [ {"x": number, "y": number}, ... ] }
```

### Dataset (bubble)
```
dataset = { "label": str, "data": [ {"x": number, "y": number, "r": number}, ... ] }
```
`r` is the bubble radius in pixels (not scaled by the axes).

## 2. `options` object (commonly used keys)

```
options = {
    "responsive":          bool,     # default True
    "maintainAspectRatio": bool,     # default False here (fill container)
    "indexAxis":           "x"|"y",  # "y" => horizontal bar
    "plugins": {
        "legend": { "display": bool, "position": "top"|"bottom"|"left"|"right" },
        "title":  { "display": bool, "text": str },
        "tooltip": { ... },
    },
    "scales": {
        "x": { "type": "linear"|"category"|"time"|..., "position": "bottom", ... },
        "y": { "beginAtZero": bool, "min": number, "max": number, ... },
        "r": { ... },                # radial scale: radar, polarArea
    },
    "animation": { ... },
}
```

## 3. Chart-type → required shape matrix

| Type | `labels` | dataset `data` shape | colours map to |
|------|:--------:|----------------------|----------------|
| line | yes | `[number]` | series |
| area | yes | `[number]` + `fill` | series |
| bar | yes | `[number]` | series |
| horizontal bar | yes | `[number]` + `indexAxis:"y"` | series |
| radar | yes | `[number]` | series |
| doughnut | yes | `[number]` | categories |
| pie | yes | `[number]` | categories |
| polarArea | yes | `[number]` | categories |
| bubble | no | `[{x,y,r}]` | series |
| scatter | no | `[{x,y}]` | series |
| mixed | yes | per-dataset `type` | series |

## 4. Builder ↔ schema mapping

| Builder | Produces |
|---------|----------|
| `dataset(...)` | one *series* dataset (single colour from palette). |
| `categorical_dataset(...)` | one dataset with **per-point** colours (pie/doughnut/polarArea). |
| `chart_data(labels, datasets)` | the top-level `data` object. |
| `options(...)` | the top-level `options` object with responsive defaults. |

## 5. Validation philosophy

Validation is intentionally light (dict-level typing). Chart.js tolerates extra
keys and reports misconfiguration at runtime in the browser console. The builders
guarantee the **structure** of the common cases; raw dicts remain fully supported
for the long tail of Chart.js options.
