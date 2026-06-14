# Specification / PRD — reflex-charts

**Status:** Draft v1 · **Owner:** Ernesto Crespo · **Last updated:** 2026-06-14

## 1. Problem statement

[Reflex](https://reflex.dev) lets developers build full-stack web apps in pure
Python; the framework compiles to React on the frontend. Reflex ships a Recharts
wrapper, but teams that have standardized on **Chart.js** — the most widely used
canvas charting library — have no first-class, idiomatic way to use it from
Python. They are forced to drop into custom JavaScript or hand-roll a wrapper.

`reflex-charts` closes that gap: a reusable Reflex custom component that exposes
the **full Chart.js feature set** through a small, Pythonic API, requiring no
JavaScript from the end user.

## 2. Goals

1. **Complete coverage.** Support all eight Chart.js chart types (line, bar,
   radar, doughnut, pie, polarArea, bubble, scatter) plus common variants
   (area, horizontal bar, mixed) through a single versatile component.
2. **Pure Python.** Charts are configured with Python dicts mirroring Chart.js
   `data`/`options`; no `.js`/`.tsx` authoring required by users.
3. **Idiomatic Reflex.** Data may be static or bound to `rx.State`, so charts
   update reactively. Native interactions (e.g. click) surface as Reflex events.
4. **Batteries included but optional.** Ergonomic builders for datasets, colours
   and options, while raw Chart.js dicts always remain accepted.
5. **Shippable package.** Standard Reflex custom-component layout, installable
   from PyPI, with a runnable demo gallery.

## 3. Non-goals (v0.1)

- Re-implementing Chart.js plugins in Python (users pass plugin options through).
- Server-side/static image rendering of charts (Chart.js is client-side canvas).
- Bundling third-party chart plugins (e.g. zoom, datalabels) — future phase.
- TypeScript-level typing of every nested Chart.js option (we type at dict level).

## 4. Target users

- **Reflex app developers** who need charts and prefer/standardize on Chart.js.
- **Data/ML engineers** building Python-only dashboards without a JS toolchain.
- **Teams migrating** existing Chart.js configs into a Reflex app (configs paste
  in almost verbatim as Python dicts).

## 5. Functional requirements

| ID | Requirement |
|----|-------------|
| FR-1 | Render any Chart.js `type` from one generic component. |
| FR-2 | Accept `data` and `options` as Python dicts (or state `Var`s). |
| FR-3 | Provide named factory helpers per chart type. |
| FR-4 | Register all Chart.js controllers/elements/scales/plugins automatically. |
| FR-5 | Provide builders: `dataset`, `categorical_dataset`, `chart_data`, `options`. |
| FR-6 | Provide a default categorical colour palette with cycling. |
| FR-7 | Surface the canvas `on_click` event with the active elements payload. |
| FR-8 | Support reactive updates when bound to `rx.State` computed vars. |
| FR-9 | Ship a demo app showcasing every chart type + an interactive example. |
| FR-10 | Pin npm dependency versions for reproducible builds. |

## 6. Non-functional requirements

- **Reproducibility:** npm versions pinned (`chart.js@4.5.0`, `react-chartjs-2@5.3.0`).
- **Compatibility:** Reflex ≥ 0.8.6, Python ≥ 3.11.
- **Footprint:** no Python runtime deps beyond Reflex.
- **License:** Apache-2.0 for this repo; upstream JS libs are MIT (see `NOTICE`).
- **Docs:** README quick-start + `specs/` SDD set + per-type examples.

## 7. Success criteria

- A developer renders a working line chart in < 10 lines of Python.
- All 11 gallery examples render in the demo without manual JS registration.
- A state-bound chart re-renders when its computed data var changes.
- `pip install reflex-charts` exposes the documented public API.

## 8. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Chart.js requires component registration | Auto-register `...registerables` in `add_custom_code`. |
| `data`/`options` are deeply nested | Accept raw dicts; provide builders for the common 80%. |
| SSR/hydration issues with canvas | Wrap via react-chartjs-2 which is client-rendered; document fixed-height containers. |
| npm version drift | Pin versions centrally in `constants.py`. |
| Reflex API evolution | Use stable `add_imports`/`add_custom_code` hooks; track in CHANGELOG. |
