# Project Assessment and Improvement Plan

## Current Level

This project is currently at a **beginner-to-intermediate prototype (MVP) level**:

- It has a working end-to-end ELT flow (JSON -> SQLite -> KPI queries -> Flask dashboard).
- It demonstrates core KPI reporting with readable logic in a single file.
- It is well-suited for learning and demonstration.

## What Is Working Well

1. **Complete ELT path is implemented** in simple and understandable code.
2. **KPI coverage is practical** (sales, profit, quantity, discount, margin).
3. **Dashboard output is usable** with table-based summaries and clean basic styling.
4. **Documentation is beginner-friendly**, with quick start and feature explanations.

## Main Gaps

1. **Monolithic app structure**: data loading, transformations, web rendering, and startup are tightly coupled in `app.py`.
2. **No dependency lock file** (`requirements.txt`/`pyproject.toml`) for reproducible setup.
3. **No automated tests** for KPI logic, SQL correctness, or route rendering.
4. **No error handling/data quality checks** for missing columns, invalid types, or divide-by-zero scenarios.
5. **Performance/scalability limits** from full reload and repeated ad-hoc aggregation queries.
6. **Documentation drift** (e.g., references to files/paths that do not exist in the repo).

## Recommended Improvement Roadmap

### Phase 1: Reliability and Maintainability (High Priority)

- Split code into modules:
  - `etl.py` (extract/load)
  - `metrics.py` (KPI queries + business logic)
  - `web.py` or Flask blueprints (routes/templates)
- Add configuration via environment variables (`DATA_PATH`, `DB_PATH`, `FLASK_ENV`).
- Add robust validation:
  - verify required columns
  - handle nulls and numeric casting
  - safe profit margin calculation when sales is zero
- Add `requirements.txt` and pin core dependencies.

### Phase 2: Testability and CI

- Add tests using `pytest`:
  - unit tests for KPI calculations
  - integration test for `/` route
  - fixtures for a small sample dataset
- Add a lightweight CI workflow (e.g., GitHub Actions):
  - install dependencies
  - run lint + tests

### Phase 3: UX and Analytics Depth

- Move inline HTML to template files (`templates/`).
- Add filters (date range, region, category) and drill-down views.
- Add charts (Plotly/Chart.js) for trends and category/product comparisons.
- Add data freshness indicator and “last updated” timestamp.

### Phase 4: Production Readiness

- Introduce logging and structured error messages.
- Add caching/materialized aggregates to reduce repeated query cost.
- Containerize with Docker and add deployment guidance.
- Consider migration path to Postgres for larger datasets.

## Suggested Success Metrics

- **Code quality**: test coverage > 70% for KPI and route logic.
- **Reliability**: zero startup failures from malformed data.
- **Performance**: dashboard render under 1 second on baseline dataset.
- **Maintainability**: clear module boundaries and reproducible setup.
