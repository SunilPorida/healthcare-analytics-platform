# Healthcare Analytics Platform

A structured Python project for healthcare data engineering, analytics, and model-driven insights. The repository separates raw and processed data, ETL logic, warehouse SQL, machine learning components, a service API, automated tests, documentation, and dashboard guidance.

## Tech stack

- **Python** — application runtime and automation  
- **Pandas / PySpark** — tabular and large-scale data processing  
- **SQL** — schemas, transformations, and analytical queries against your warehouse or database  
- **FastAPI** — HTTP APIs for services, integrations, and operational endpoints  

## Repository layout

| Folder | Purpose |
|--------|---------|
| `data/raw` | Source-aligned extracts and landing files (not committed). |
| `data/processed` | Cleaned or feature-ready datasets for downstream use (not committed). |
| `etl` | Ingestion and transformation jobs. |
| `sql` | DDL, migrations, and reusable queries. |
| `ml_model` | Training and inference code and configuration. |
| `api` | FastAPI application. |
| `tests` | Unit and integration tests. |
| `docs` | Architecture notes and diagrams. |
| `dashboard` | Instructions and conventions for BI dashboards (e.g. Power BI). |

## Quick start

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create local data directories if they do not exist yet:

```bash
mkdir data\raw data\processed
```

Run the API (when implemented):

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```
