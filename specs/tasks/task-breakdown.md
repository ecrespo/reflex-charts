# Task breakdown — reflex-charts

**Status:** v1 · **Last updated:** 2026-06-14 · Legend: `[x]` done · `[ ]` open

Granular, checkable work items grouped by phase (see [phases](../phases/phases.md)).

## P0 — Research & specification
- [x] Study Chart.js types, `data`/`options` model, registration requirements.
- [x] Study Reflex `rx.Component` wrapping (`library`, `tag`, `lib_dependencies`).
- [x] Study Reflex `add_imports` / `add_custom_code` and event triggers.
- [x] Confirm `react-chartjs-2` generic `Chart` component contract.
- [x] Write PRD, architecture, API spec, data-model, phases, plan, tasks.

## P1 — Core wrapper
- [x] `constants.py`: npm pins, `CHART_TYPES` (8), `PALETTE`, `PALETTE_ALPHA`.
- [x] `base.py`: `ChartJSBase` with deps + global registration.
- [x] `chart.py`: `ChartCanvas` props (`type/data/options/plugins/width/height`).
- [x] `chart.py`: `on_click` event handler forwarding active elements.
- [x] `chart.py`: factories for all 8 types + generic `chart()`.
- [x] `__init__.py`: public re-exports + `__version__`.

## P2 — Builders
- [x] `dataset()` with palette defaults and `**extra` passthrough.
- [x] `categorical_dataset()` with per-point colours.
- [x] `chart_data()` supporting label-less (scatter/bubble) data.
- [x] `options()` with responsive defaults + `**extra`.
- [x] Unit tests for builder output shapes.

## P3 — Demo & examples
- [x] `examples/data.py`: line, area, bar, horizontal bar, radar, doughnut, pie,
      polar area, bubble, scatter, mixed (11 figures) + `GALLERY` registry.
- [x] `reflex_charts.py`: responsive gallery grid of all types.
- [x] `reflex_charts.py`: interactive `DemoState` (randomize + click reporting).

## P4 — Packaging & repo
- [x] `pyproject.toml` (setuptools, metadata, package-data).
- [x] `rxconfig.py` (app `reflex_charts`, Tailwind + sitemap plugins).
- [x] `LICENSE` (Apache-2.0), `NOTICE` (MIT upstream attribution).
- [x] `.gitignore`, `.python-version`, `main.py`, `CHANGELOG.md`.
- [x] `README.md` quick-start + feature/API overview.
- [x] `tests/test_imports.py` smoke tests.
- [x] `scripts/create_github_repo.sh`.
- [ ] `git init`, branch `main`, initial commit.
- [ ] Create public GitHub repo and push `main`.

## P5 — Hardening (future)
- [ ] CI workflow (ruff + pytest) on push/PR.
- [ ] PyPI release (`reflex component build` / `publish`).
- [ ] Plugin passthrough recipes (zoom, datalabels, annotation).
- [ ] Structured `on_click` payload `{datasetIndex, index, value}`.
- [ ] `time`-scale recipe with a date adapter.
- [ ] Docs site / expanded examples per chart type.

## Acceptance checklist (v0.1.0)
- [x] All pure-logic modules compile and unit tests pass.
- [x] Public API matches `specs/api/component-api-v1.md`.
- [ ] `reflex run` renders the gallery on a Python 3.13 + Reflex environment.
- [ ] `main` branch pushed to GitHub (public).
