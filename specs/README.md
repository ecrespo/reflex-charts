# Spec-Driven Design (SDD) — reflex-charts

This directory holds the **specifications that drive the implementation** of
`reflex-charts`. In Spec-Driven Design the documents here are the primary
artifact: code is written to satisfy the spec, and the spec is updated first
when requirements change.

## Reading order

| # | Document | Purpose |
|---|----------|---------|
| 1 | [`prd/reflex-charts-prd.md`](prd/reflex-charts-prd.md) | **Specification** — problem, goals, users, functional & non-functional requirements, scope. |
| 2 | [`technical/architecture.md`](technical/architecture.md) | **Architecture** — how Reflex wraps Chart.js, module layout, data flow, key decisions. |
| 3 | [`api/component-api-v1.md`](api/component-api-v1.md) | **API spec** — the public Python surface (components, factories, builders). |
| 4 | [`data-model/chart-data-schemas.md`](data-model/chart-data-schemas.md) | **Data model** — the Chart.js `data`/`options` schemas as used here. |
| 5 | [`phases/phases.md`](phases/phases.md) | **Phases** — delivery broken into milestones P0–P5. |
| 6 | [`plans/implementation-plan.md`](plans/implementation-plan.md) | **Plan** — concrete build sequence mapped to the architecture. |
| 7 | [`tasks/task-breakdown.md`](tasks/task-breakdown.md) | **Tasks** — granular, checkable work items per phase. |

## How these were produced

The specs were derived from primary research into two sources:

- **Chart.js** — the charting engine ([chartjs.org](https://www.chartjs.org),
  [github.com/chartjs/Chart.js](https://github.com/chartjs/Chart.js)): chart
  types, the `data`/`options` configuration model, controllers, scales, plugins.
- **Reflex** — the Python web framework ([reflex.dev](https://reflex.dev)) and
  its *wrapping React* and *custom components* guides: `rx.Component`,
  `library`/`tag`/`lib_dependencies`, `Var` props, `EventHandler`,
  `add_imports`, `add_custom_code`, and the `reflex component` packaging layout.

## Status

`v0.1.0` — foundation: base wrapper, generic component, typed factories, data
builders, and a demo gallery covering every chart type. See
[`../CHANGELOG.md`](../CHANGELOG.md).
