# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-10-24

### Added
- Release workflow (`.github/workflows/publish.yml`): pushing a `vX.Y.Z` tag
  that matches `pyproject.toml` runs the tests, builds the distribution and
  publishes it to PyPI via Trusted Publishing (no API token).

## [0.2.0] - 2026-10-24

### Changed
- **Require Reflex ≥ 0.10.0** (was ≥ 0.8.6). Stay on `reflex-charts==0.1.0`
  for Reflex 0.8/0.9.
- Build/publish docs: Reflex 0.10 removed the `reflex component` CLI, so the
  package is built with `uv build` and uploaded with `twine` / `uv publish`.
  Stub regeneration now uses `python -m reflex_base.utils.pyi_generator`.
- Build backend requires `setuptools>=78.1.1`.
- Demo `requirements.txt` installs the published `reflex-charts` from PyPI
  (so Reflex Cloud deploys work) instead of `-e ..`.
- Adopt the standard Reflex custom-component layout: the importable package now
  lives under `custom_components/reflex_charts/`, and the demo is a standalone
  app in `reflex_charts_demo/`. `pyproject.toml` uses
  `packages.find where=["custom_components"]`. Import path (`import reflex_charts`)
  and public API are unchanged.

### Added
- GitHub Actions CI: pytest on Python 3.11–3.13, wheel build with a stub check,
  and a `reflex compile` of the demo app.
- Spec-traceable unit-test suite (constants, helpers, examples, components,
  public API) — 90 tests covering the documented surface.
- `publish` optional-dependency group (`build`, `twine`) for building and
  uploading the distribution; `build`/`twine` also added to the dev group.
- Generated type stubs (`base.pyi`, `chart.pyi`) and a PEP 561 `py.typed`
  marker, packaged so editors get typed autocomplete for the components.

### Fixed
- Remove the unregistered `Framework :: Reflex` trove classifier that PyPI
  rejected (400) on upload.

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
