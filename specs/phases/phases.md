# Delivery phases — reflex-charts

**Status:** v1 · **Last updated:** 2026-06-14

Delivery is split into milestones. Each phase has an exit criterion; a phase is
"done" only when its criterion is demonstrably met.

## P0 — Research & specification ✅ (this milestone)
- Study Chart.js (types, config model, registration) and Reflex custom-component
  wrapping.
- Produce the SDD set (PRD, architecture, API, data model, plan, tasks).
- **Exit:** specs reviewed and the public API shape agreed.

## P1 — Core wrapper foundation ✅
- `constants.py` (pins, types, palette), `base.py` (dependencies + registration),
  `chart.py` (`ChartCanvas` + factories), `__init__.py` public API.
- **Exit:** all 8 types instantiate; Chart.js auto-registers.

## P2 — Ergonomic builders ✅
- `helpers.py`: `dataset`, `categorical_dataset`, `chart_data`, `options` + palette cycling.
- **Exit:** builders produce valid Chart.js dicts; covered by unit tests.

## P3 — Demo gallery & interactivity ✅
- `examples/data.py` (canonical figures + GALLERY) and `reflex_charts.py` demo
  with a responsive gallery + a state-bound, click-aware interactive chart.
- **Exit:** `reflex run` renders every chart type and the interactive example.

## P4 — Packaging & repository 🔄 (current)
- `pyproject.toml`, `LICENSE`, `NOTICE`, `.gitignore`, `README.md`, tests,
  `scripts/create_github_repo.sh`; git `main` branch; publish to GitHub.
- **Exit:** repo on GitHub with green `main`; `pip install` works locally.

## P5 — Hardening & ecosystem ⏳ (future)
- Optional plugin passthrough recipes (zoom, datalabels, annotation).
- Typed option helpers for scales/animations; richer event payloads
  (clicked dataset/index, hover).
- CI (lint + tests), PyPI release, expanded docs site.
- **Exit:** v0.2 published to PyPI with CI and plugin recipes.

## Phase ↔ requirement traceability

| Phase | Requirements covered (see PRD §5) |
|-------|-----------------------------------|
| P1 | FR-1, FR-2, FR-3, FR-4, FR-10 |
| P2 | FR-5, FR-6 |
| P3 | FR-7, FR-8, FR-9 |
| P4 | NFRs: packaging, license, docs |
| P5 | Extensibility, CI/CD, distribution |
