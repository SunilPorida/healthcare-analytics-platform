# Schema (DDL)

Store versioned DDL aligned with environments: `dev`, `staging`, `prod`.

**Suggested naming**

- `V001__initial_core.sql` — ordered migrations  
- Or one file per domain: `dim_patient.sql`, `fact_encounter.sql`

Apply changes through your standard migration process (manual runbook, schemachange, Flyway equivalent, or CI).
