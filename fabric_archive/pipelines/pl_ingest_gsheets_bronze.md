# Pipeline: pl_ingest_gsheets_bronze

> Screenshot of the full pipeline canvas: `screenshots/pl_ingest_gsheets_bronze_canvas.png`

## Trigger

- Type: <!-- Manual / Scheduled -->
- Schedule: <!-- e.g. none — invoked by pl_master_datacenter360 -->

## Activities

| # | Activity Name | Type | Source | Destination | Notes |
|---|----------------|------|--------|-------------|-------|
| 1 | | Copy Data (HTTP connector) | Google Sheets export URL: `server_inventory` | `lh_bronze.server_inventory` | |
| 2 | | Copy Data (HTTP connector) | Google Sheets export URL: `incident_log` | `lh_bronze.incident_log` | |
| 3 | | Copy Data (HTTP connector) | Google Sheets export URL: `capacity_utilization` | `lh_bronze.capacity_utilization` | |

## Activity Details

### Activity 1 — server_inventory

- Source dataset / linked service: <!-- screenshot ref -->
- Source settings (HTTP connector base URL, relative URL, format): <!-- fill in -->
- Sink settings (table name, write behavior — overwrite/append): <!-- fill in -->
- Mapping: <!-- fill in if custom mapping used -->

### Activity 2 — incident_log

- Source settings: <!-- fill in -->
- Sink settings: <!-- fill in -->

### Activity 3 — capacity_utilization

- Source settings: <!-- fill in -->
- Sink settings: <!-- fill in -->

## Dynamic Content / Expressions

<!-- Paste any pipeline expressions (fx) used, e.g. for parameterized URLs or table names -->

```
<expression text here>
```
