# Architecture — reflex-charts

**Status:** Draft v1 · **Last updated:** 2026-06-14

## 1. Overview

`reflex-charts` is a thin, well-typed Python facade over the Chart.js React
bindings. Reflex compiles Python components to React; this package declares a
Reflex component whose generated JSX is the `<Chart>` element from
`react-chartjs-2`, with Chart.js registered globally so any chart type works.

```
 Python (author)            Reflex compiler           Browser (runtime)
┌────────────────┐         ┌────────────────┐        ┌─────────────────────┐
│ rxc.bar(       │         │  generates     │        │ react-chartjs-2     │
│   data=...,    │ ──────▶ │  React/JSX +   │ ─────▶ │   <Chart type=.../> │
│   options=...) │         │  package.json  │        │        │            │
└────────────────┘         └────────────────┘        │   Chart.js canvas   │
        ▲                                             └─────────┬───────────┘
        │   on_click(elements)  ◀───────── Reflex event ────────┘
   rx.State handler
```

## 2. Key decision: wrap `react-chartjs-2`, not Chart.js directly

Chart.js is an imperative canvas library (`new Chart(ctx, config)`); Reflex wraps
**declarative React components**. `react-chartjs-2` is the official, maintained
React binding that exposes Chart.js as React components taking `type`, `data`
and `options` props and handling the canvas lifecycle (create/update/destroy).

Wrapping it gives us reactive prop-driven updates for free and keeps the Python
side declarative. See ADR-001 below.

## 3. Key decision: one generic component, not eight

`react-chartjs-2` exposes typed components (`Line`, `Bar`, …) **and** a generic
`Chart` that takes a `type` prop. We wrap the generic `Chart` once
(`ChartCanvas`) and expose Python factory functions per type. This:

- Maximizes versatility (mixed charts, runtime-chosen types).
- Centralizes dependency and registration wiring in one base class.
- Keeps the public API small while reading naturally (`rxc.line(...)`).

See ADR-002.

## 4. Key decision: global registration via `add_custom_code`

Chart.js v3+ is tree-shakeable: controllers, elements, scales and plugins must be
registered before use. Rather than make users register pieces, the base class
emits once per module:

```js
import { Chart as ChartJS, registerables } from "chart.js";
ChartJS.register(...registerables);
```

`registerables` is the full built-in bundle, so every chart type and the common
plugins (legend, tooltip, title, filler) are available with zero user setup.
Registration is idempotent in Chart.js, so emitting it per component is safe.
See ADR-003.

## 5. Module layout

```
reflex_charts/
├── __init__.py        Public API surface (re-exports).
├── constants.py       npm version pins, CHART_TYPES, colour palettes.
├── base.py            ChartJSBase: library/lib_dependencies + registration.
├── chart.py           ChartCanvas (generic) + chart()/line()/bar()/… factories.
├── helpers.py         dataset / categorical_dataset / chart_data / options.
├── examples/
│   ├── __init__.py
│   └── data.py        Canonical sample figures + GALLERY registry.
└── reflex_charts.py   Demo Reflex app (gallery + interactive state example).
```

Dependency direction is strictly inward and acyclic:
`__init__ → chart → base → constants`; `helpers → constants`;
`examples.data → helpers`; `reflex_charts.py → (package public API + examples)`.

## 6. Data flow

1. **Author** builds `data`/`options` dicts (directly or via `helpers`).
2. Dicts are passed as props to a factory → `ChartCanvas.create(type=…, data=…)`.
3. Reflex serializes props to JSON and renders `<Chart>` from react-chartjs-2.
4. Chart.js paints the canvas. On interaction, `onClick(event, elements, chart)`
   fires; the wrapper forwards `elements` to the bound Reflex `EventHandler`.
5. When `data` is an `rx.State` computed `Var`, any state change recomputes the
   prop and react-chartjs-2 diff-updates the existing chart instance.

## 7. Props contract (frontend mapping)

| Python (`ChartCanvas`) | JS prop on `<Chart>` | Type |
|------------------------|----------------------|------|
| `type` | `type` | string (one of `CHART_TYPES`) |
| `data` | `data` | object `{labels?, datasets[]}` |
| `options` | `options` | object (Chart.js options) |
| `plugins` | `plugins` | array (inline plugins) |
| `width` / `height` | `width` / `height` | number (px) |
| `on_click` | `onClick` | `(event, elements, chart) ⇒` forwards `elements` |

## 8. Reliability / rendering notes

- Charts should live in a **fixed-height container** with
  `options.maintainAspectRatio = False` (the `options()` builder defaults to
  this) so they fill responsive layouts predictably.
- react-chartjs-2 is client-rendered; no special SSR handling is required for the
  generic component in current Reflex versions. If a future Reflex/SSR mode
  causes hydration issues, the base can switch to `rx.NoSSRComponent`.

## 9. Architecture Decision Records

### ADR-001 — Wrap react-chartjs-2 rather than Chart.js core
- **Context:** Reflex wraps declarative React components; Chart.js core is imperative.
- **Decision:** Depend on `react-chartjs-2` with `chart.js` as a peer dependency.
- **Consequences:** Free reactive updates and lifecycle handling; one extra npm
  dependency; we follow react-chartjs-2's prop contract.

### ADR-002 — Single generic component + Python factories
- **Decision:** Wrap the generic `Chart` export; expose `chart()` + named helpers.
- **Consequences:** Smaller surface, supports mixed/dynamic types; `type` is a
  prop rather than baked into separate classes.

### ADR-003 — Auto-register all Chart.js registerables
- **Decision:** Emit `ChartJS.register(...registerables)` via `add_custom_code`.
- **Consequences:** Zero-config for users; slightly larger JS bundle than
  hand-registering only used pieces (acceptable for a general-purpose wrapper).

### ADR-004 — Accept raw dicts, builders optional
- **Decision:** Type `data`/`options` as `Var[dict]`; provide optional builders.
- **Consequences:** Any chartjs.org example pastes in as Python; full Chart.js
  power retained; less compile-time validation of nested option keys.
