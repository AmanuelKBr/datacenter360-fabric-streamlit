# Pipeline: pl_master_datacenter360

> Screenshot of the full pipeline canvas: `screenshots/pl_master_datacenter360_canvas.png`

## Trigger

- Type: Scheduled
- Schedule: Daily at 6:00 AM ET
- Time zone: <!-- confirm exact timezone configured -->

## Activity Flow

```
pl_master_datacenter360 (Daily 6:00 AM ET)
│
├── pl_ingest_gsheets_bronze     ← Google Sheets → lh_bronze
├── nb_ingest_weather_bronze     ← Open-Meteo API → lh_bronze
├── Wait (120s)
├── nb_transform_silver          ← Bronze → Silver transformations
├── Wait (180s)
├── nb_transform_gold            ← Silver → Gold aggregations + CSV export
└── sm_refresh                   ← Semantic model refresh
```

## Activity Details

| # | Activity Name | Type | Settings / Notes |
|---|----------------|------|-------------------|
| 1 | | Invoke Pipeline / ExecutePipeline | Calls `pl_ingest_gsheets_bronze` |
| 2 | | Notebook | Runs `nb_ingest_weather_bronze`, params: <!-- fill in --> |
| 3 | | Wait | 120 seconds — allows Spark session to free up |
| 4 | | Notebook | Runs `nb_transform_silver`, params: <!-- fill in --> |
| 5 | | Wait | 180 seconds |
| 6 | | Notebook | Runs `nb_transform_gold`, params: <!-- fill in --> |
| 7 | | Semantic Model Refresh | Refreshes `sm_datacenter360` after gold tables update |

## Dependency / Success Conditions

<!-- Note any "On Success" / "On Failure" branch conditions between activities -->

## Notebook Run Parameters

<!-- If notebooks are invoked with base parameters (e.g. environment, date), document them here -->
