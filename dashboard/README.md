# Power BI dashboard (external)

Power BI lives outside this repository. Use this folder for **instructions**, data contracts, and links to published workspaces.

## Recommended connectivity

1. **Import mode** — Scheduled refresh from Snowflake tables or Parquet exports in S3 (via gateway or dataflow, depending on governance).
2. **DirectQuery** — For near-real-time operational dashboards; enforce aggregations and use certified datasets.
3. **Composite / hybrid** — Large historical facts in import, hot metrics in DirectQuery.

## Dataset design

- Define a **single certified dataset** per subject area (e.g. population health, utilization).
- Document grain, keys, and measure definitions here or in `docs/architecture.md`.
- Align column names with `sql/schema` and `sql/queries` for analyst discoverability.

## Security

- Use **Power BI row-level security (RLS)** mapped to roles from your identity provider.
- Avoid embedding warehouse passwords in PBIX files; use organizational gateways and service principals where approved.

## Refresh and operations

- Document refresh windows, dependencies on ETL completion, and owner contacts.
- Link to runbooks in `docs/` for incident response.

## Local analytics

For analyst sandboxes, prefer **Power BI Desktop** against dev Snowflake or CSV extracts from `data/processed` (never commit PHI to git).
