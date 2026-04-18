# Healthcare Analytics Platform

End-to-end analytics stack for healthcare data: ingestion, transformation, warehouse-style SQL, machine learning, and API exposure. Business intelligence is delivered via **Power BI** connected to curated datasets (Snowflake tables, API exports, or semantic models you publish).

## Repository layout

| Path | Purpose |
|------|---------|
| `data/raw` | Immutable landing zone for source extracts (not committed). |
| `data/processed` | Cleaned, conformed, or feature-ready datasets (not committed). |
| `etl/ingestion` | Pull/load jobs (files, APIs, streams) into raw or staging. |
| `etl/transformations` | Business rules, joins, aggregations toward processed/analytics layers. |
| `sql/schema` | DDL and incremental migration scripts for warehouse tables. |
| `sql/queries` | Reusable analytical SQL (reports, exports, validation). |
| `ml_model/training` | Training pipelines, hyperparameters, experiment tracking hooks. |
| `ml_model/prediction` | Batch or online scoring, model artifacts loading. |
| `api` | FastAPI service for health checks, metadata, and controlled data access. |
| `dashboard` | Guidance for Power BI datasets, refresh, and row-level security patterns. |
| `tests/data_validation` | Great Expectations-style or custom checks on pipelines and tables. |
| `tests/uat` | User acceptance scenarios and sign-off checklists. |
| `docs` | Architecture decisions, diagrams, and runbooks. |

## Tech stack

- **Python** — orchestration and services  
- **Pandas / PySpark** — single-node and distributed transforms  
- **SQL** — semantic layer in Snowflake (or compatible engines)  
- **Snowflake** — production warehouse; use dev accounts or mocks locally  
- **AWS S3** — object storage; use **LocalStack** or **MinIO** locally if needed  
- **FastAPI** — operational and read APIs  
- **Power BI** — external dashboards and governance (see `dashboard/`)

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/docs` for interactive API documentation.

## Local simulation notes

- **S3**: Point `AWS_ENDPOINT_URL` (if supported by your code) to LocalStack or MinIO; use distinct buckets for `raw` and `processed`.  
- **Snowflake**: Prefer a dedicated dev warehouse and role; avoid production credentials in `.env`. For unit tests, mock connectors or use a lightweight SQLite staging layer where appropriate.

## Testing

```bash
pytest tests -q
```

## Documentation

See `docs/architecture.md` and `docs/diagrams/` for system context and data flow.

## License

Proprietary / internal use unless otherwise specified.
