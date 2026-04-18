# Ingestion

Place scheduled or event-driven jobs that land data into `data/raw` or S3 raw prefixes.

**Conventions**

- One module per source system (e.g. `ehr_batch.py`, `claims_api.py`).
- Read configuration from environment variables (see repository `.env.example`).
- Write idempotent loads where possible (partition keys, file naming with run IDs).
