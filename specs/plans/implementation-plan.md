# Implementation plan — reflex-charts

**Status:** v1 · **Last updated:** 2026-06-14

This plan turns the [architecture](../technical/architecture.md) into an ordered
build sequence. Steps marked ✅ are complete in v0.1.0.

## Sequence

1. **Pin dependencies & constants** ✅
   `constants.py`: `CHARTJS_NPM`, `REACT_CHARTJS_2_NPM`, `CHART_TYPES`, palettes.

2. **Base wrapper** ✅
   `base.py`: `ChartJSBase(rx.Component)` with `library`, `lib_dependencies`,
   `add_imports` (Chart.js registry symbols) and `add_custom_code`
   (`ChartJS.register(...registerables)`).

3. **Generic component + factories** ✅
   `chart.py`: `ChartCanvas` (props `type/data/options/plugins/width/height/on_click`)
   and factories `chart`, `line`, `bar`, `radar`, `doughnut`, `pie`,
   `polar_area`, `bubble`, `scatter`.

4. **Builders** ✅
   `helpers.py`: `dataset`, `categorical_dataset`, `chart_data`, `options`,
   palette cycling via `_color`.

5. **Public API** ✅
   `__init__.py`: re-export components, factories, builders, constants; set
   `__version__`.

6. **Examples & demo** ✅
   `examples/data.py` (11 canonical figures + `GALLERY`) and `reflex_charts.py`
   (gallery grid + interactive `DemoState` with `randomize` and `on_point_click`).

7. **Tests** ✅
   `tests/test_imports.py`: public surface present, constants, builder shapes.

8. **Packaging & meta** ✅
   `pyproject.toml` (setuptools), `rxconfig.py`, `LICENSE` (Apache-2.0), `NOTICE`,
   `.gitignore`, `.python-version`, `CHANGELOG.md`, `README.md`.

9. **Version control** 🔄
   `git init`, default branch `main`, initial commit of the base.

10. **GitHub** 🔄
    Create the public repository and push `main`
    (via the GitHub connector, or `scripts/create_github_repo.sh` with `gh`).

## Verification strategy

- **Static:** `python -m py_compile` across all modules (syntax).
- **Unit:** `pytest` on dependency-free builders/constants/examples.
- **Integration (on Python 3.13 with Reflex):** `reflex run` renders the gallery;
  the interactive chart updates on *Randomize* and reports clicks.
- **Packaging:** `pip install -e .` then `import reflex_charts` exposes the API.

## Rollback / change management

Specs are the source of truth: change the relevant `specs/` document first, then
the code, then `CHANGELOG.md`. Dependency upgrades are isolated to `constants.py`.

## Open questions (tracked for P5)

- Which third-party Chart.js plugins to bundle vs. document as passthrough?
- Should `on_click` resolve to a structured `{datasetIndex, index, value}` payload
  rather than the raw active-elements array?
- Add a `time` scale recipe using a date adapter (e.g. `chartjs-adapter-date-fns`)?
