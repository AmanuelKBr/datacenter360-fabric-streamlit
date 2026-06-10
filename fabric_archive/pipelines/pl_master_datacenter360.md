# Pipeline: pl_master_datacenter360

Full ARM template definition exported from Fabric: [`pl_master_datacenter360.json`](pl_master_datacenter360.json)

- **Workspace ID:** `adbcfe0d-bf1c-4d80-b926-e339a4faca0e`
- **Last published:** 2026-04-30T03:05:44Z
- **Schedule:** Daily at 6:00 AM ET (per README orchestration diagram)

## Purpose
End-to-end daily orchestration: ingest both data sources into Bronze, then run the Silver and Gold transformation notebooks in sequence, with `Wait` activities to work around Fabric Trial Spark session capacity limits.

## Activity Flow

```
copy_server_inventory (Copy, Succeeded)
   └─→ copy_incident_log (Copy, Succeeded)
          └─→ copy_capacity_utilization (Copy, Succeeded)
                 └─→ run_ingest_weather (TridentNotebook, Succeeded)
                        └─→ wait_after_ingest (Wait 120s, Succeeded)
                               └─→ run_silver (TridentNotebook, Succeeded)
                                      └─→ wait_after_silver (Wait 180s, Succeeded)
                                             └─→ run_gold (TridentNotebook)
```

## Activity Details

| Activity | Type | Notebook ID | Notes |
|----------|------|--------------|-------|
| `copy_server_inventory` | Copy | — | Google Sheets → `lh_bronze.dbo.server_inventory` (same config as `pl_ingest_gsheets_bronze`) |
| `copy_incident_log` | Copy | — | Google Sheets → `lh_bronze.dbo.incident_log` |
| `copy_capacity_utilization` | Copy | — | Google Sheets → `lh_bronze.dbo.capacity_utilization` |
| `run_ingest_weather` | TridentNotebook | `dc0dd780-d249-4830-bcd9-2d8f6e53d6e0` | Corresponds to `nb_ingest_weather_bronze.ipynb` — Open-Meteo API → `lh_bronze.weather_ashburn` |
| `wait_after_ingest` | Wait | — | 120 seconds — allows Spark session to free up before Silver run |
| `run_silver` | TridentNotebook | `204fa27c-7232-45c0-9a37-ade16a4f889e` | Corresponds to `nb_transform_silver.ipynb` — Bronze → Silver |
| `wait_after_silver` | Wait | — | 180 seconds — allows Spark session to free up before Gold run |
| `run_gold` | TridentNotebook | `286ed1e8-108a-4ab8-a896-b3b31e72ef03` | Corresponds to `nb_transform_gold.ipynb` — Silver → Gold + CSV export |

## Notes
- The README orchestration diagram also lists an `sm_refresh` step after `run_gold` (Semantic Model Refresh) — this step is not present in the exported pipeline JSON, so it may have been configured separately (e.g., a scheduled semantic model refresh) or added/removed after this export was taken.
- This pipeline duplicates the three Copy activities from `pl_ingest_gsheets_bronze` inline rather than calling that pipeline via `ExecutePipeline`.
- Pipeline canvas/diagram metadata (`manifest.json`) was provided during export but omitted here as low-value visual layout data.
