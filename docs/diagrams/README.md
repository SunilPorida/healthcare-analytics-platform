# Diagrams

Add **Mermaid** (`.mmd`) or exported **PNG/SVG** diagrams here.

## Example (high-level data flow)

```mermaid
flowchart LR
  subgraph Sources
    EHR[EHR / Claims]
  end
  subgraph Platform
    ING[ETL ingestion]
    TR[ETL transformations]
    WH[(Snowflake)]
    ML[ML train / predict]
    API[FastAPI]
  end
  subgraph Consumers
    PBI[Power BI]
  end
  EHR --> ING --> TR --> WH
  TR --> ML --> WH
  WH --> API
  WH --> PBI
```

Keep diagrams next to ADRs or architecture updates in `docs/architecture.md` for traceability.
