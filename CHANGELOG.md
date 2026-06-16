# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Adopt the standard Reflex custom-component layout: the importable package now
  lives under `custom_components/reflex_charts/`, and the demo is a standalone
  app in `reflex_charts_demo/`. `pyproject.toml` uses
  `packages.find where=["custom_components"]`. Import path (`import reflex_charts`)
  and public API are unchanged.

### Added
- Spec-traceable unit-test suite (constants, helpers, examples, components,
  public API) — 90 tests covering the documented surface.
- `publish` optional-dependency group (`build`, `twine`) for
  `reflex component build` / `publish`; `build`/`twine` also added to the dev
  group so `reflex component build` works out of the box.
- Generated type stubs (`base.pyi`, `chart.pyi`) and a PEP 561 `py.typed`
  marker, packaged so editors get typed autocomplete for the components.

## [0.1.0] - 2026-06-14

### Added
- Initial scaffold of the `reflex-charts` custom component.
- `ChartJSBase` wrapper around `react-chartjs-2` + `chart.js` with automatic
  global registration of all Chart.js controllers, elements, scales and plugins.
- Generic `ChartCanvas` component and `chart()` factory.
- Named helpers: `line`, `bar`, `radar`, `doughnut`, `pie`, `polar_area`,
  `bubble`, `scatter`.
- Data/options builders: `dataset`, `categorical_dataset`, `chart_data`, `options`.
- Demo app (`reflex_charts/reflex_charts.py`) with a gallery of all chart types
  and an interactive, state-driven example.
- Spec-Driven Design artifacts under `specs/` (PRD, architecture, API, data
  model, phases, plan, tasks).
