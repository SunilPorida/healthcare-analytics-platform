# Transformations

Implement cleansing, standardization (e.g. code systems), and aggregations.

**Conventions**

- Prefer pure functions for Pandas steps; isolate Spark session creation for PySpark jobs.
- Emit to `data/processed` or curated Snowflake tables via `sql/schema` contracts.
- Document grain and refresh cadence at the top of each pipeline module.
