-- Example healthcare-oriented objects (adapt types and constraints to your standards).
-- Run against Snowflake or your dev warehouse after review.

CREATE TABLE IF NOT EXISTS dim_patient (
    patient_sk           VARCHAR(36) NOT NULL,
    source_patient_id    VARCHAR(256) NOT NULL,
    birth_date           DATE,
    sex_at_birth_code    VARCHAR(16),
    effective_from_ts    TIMESTAMP_NTZ NOT NULL,
    effective_to_ts      TIMESTAMP_NTZ,
    is_current             BOOLEAN NOT NULL DEFAULT TRUE,
    etl_batch_id           VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_encounter (
    encounter_sk           VARCHAR(36) NOT NULL,
    patient_sk             VARCHAR(36) NOT NULL,
    encounter_start_ts     TIMESTAMP_NTZ NOT NULL,
    encounter_end_ts       TIMESTAMP_NTZ,
    encounter_type_code    VARCHAR(64),
    etl_batch_id           VARCHAR(64) NOT NULL
);
