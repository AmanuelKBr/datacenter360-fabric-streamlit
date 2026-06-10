# Pipeline: pl_ingest_gsheets_bronze

Full ARM template definition exported from Fabric: [`pl_ingest_gsheets_bronze.json`](pl_ingest_gsheets_bronze.json)

- **Workspace ID:** `adbcfe0d-bf1c-4d80-b926-e339a4faca0e`
- **Last published:** 2026-04-22T06:13:13Z

## Purpose
Ingests the three Google Sheets sources (DCIM simulation data) into the `lh_bronze` lakehouse via the Data Factory HTTP connector.

## Activities (sequential, `Completed` dependency chain)

| Order | Activity | Type | Source | Sink (lh_bronze, schema `dbo`) |
|-------|----------|------|--------|----------------------------------|
| 1 | `copy_server_inventory` | Copy | Google Sheets (HTTP GET, CSV export) | Table `server_inventory` |
| 2 | `copy_incident_log` | Copy | Google Sheets (HTTP GET, CSV export) | Table `incident_log` |
| 3 | `copy_capacity_utilization` | Copy | Google Sheets (HTTP GET, CSV export) | Table `capacity_utilization` |

All three activities use:
- **Source:** `DelimitedTextSource` / `HttpReadSettings` (GET), comma-delimited, `firstRowAsHeader: true`, quote char `"`, escape char `\`
- **Sink:** `LakehouseTableSink`, `tableActionOption: "Append"`, `partitionOption: "None"`, `applyVOrder: false`
- **Translator:** `TabularTranslator` with explicit column mappings, `typeConversion: true`, `allowDataTruncation: true`

## Column Mappings (source → sink, all string→string with type conversion)

**server_inventory**: server_id, rack_id, data_center_location, server_type, cpu_cores, ram_gb, install_date, status

**incident_log**: incident_id, server_id, incident_date, incident_type, severity, resolution_time_hrs, resolved

**capacity_utilization**: record_id, server_id, timestamp, cpu_pct, ram_pct, storage_pct, network_mbps, power_watts

## Notes
- This pipeline is also embedded (with identical activity definitions) inside `pl_master_datacenter360` rather than being invoked via `ExecutePipeline`.
- The pipeline canvas/diagram metadata (`manifest.json`, including the linked-service connection names pointing at the Google Sheets export URLs and `lh_bronze`) was provided during export but omitted here as low-value (purely visual layout data) — the JSON above contains all functional configuration.
