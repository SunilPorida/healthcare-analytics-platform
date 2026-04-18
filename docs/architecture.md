# Architecture

## Goals

- Ingest healthcare source data with auditability and repeatable batches.
- Transform into conformed dimensions and facts suitable for analytics and ML features.
- Serve curated data through Snowflake and a controlled **FastAPI** surface.
- Visualize in **Power BI** using governed datasets.

## Logical components

1. **Landing (S3 raw / `data/raw`)** — immutable or versioned source files.
2. **Processing** — Pandas for smaller volumes; PySpark for distributed workloads.
3. **Curated warehouse (Snowflake)** — schema in `sql/schema`; analytical SQL in `sql/queries`.
4. **ML** — `ml_model/training` produces artifacts; `ml_model/prediction` writes scores.
5. **API** — operational endpoints, feature lookup, or thin read models (policy-dependent).
6. **BI** — Power BI datasets documented under `dashboard/`.

## Non-functional expectations

- Secrets only via environment variables or a managed secret store (never in git).
- Separate dev/stage/prod databases or accounts in Snowflake.
- Tests: `tests/data_validation` in CI; `tests/uat` for release governance.

## Diagrams

Source diagrams (Mermaid, draw.io exports, etc.) live in `docs/diagrams/`.
