# Semantic Model: sm_datacenter360 — Tables & Columns

Captured from the Fabric web modeling view (model diagram) before trial expiration.

## Relationships
**No relationships are defined between tables.** All 5 tables appear as standalone entities in the
model diagram with no relationship lines. Each table is queried independently by the Power BI
report visuals (no cross-table joins at the semantic model layer).

## Tables

All 5 tables correspond directly to the gold-layer CSVs in [`/data`](../../data) (DirectLake over
the `lh_gold` lakehouse). Columns marked **Σ** have an implicit/default summarization (Sum or
Average) set in the model, which is what the report visuals use — there are **no DAX measures**
(see [`sm_datacenter360_measures.md`](sm_datacenter360_measures.md)).

### `incident_summary`
- avg_resolution_hrs **(Σ)**
- data_center_location
- incident_type
- open_incidents **(Σ)**
- severity
- total_incidents **(Σ)**

### `pue_metrics`
- avg_cpu_pct **(Σ)**
- avg_ram_pct **(Σ)**
- data_center_location
- pue_proxy **(Σ)**
- pue_status
- timestamp
- total_power_watts **(Σ)**

### `server_health_scores`
- avg_cpu_pct **(Σ)**
- avg_network_mbps **(Σ)**
- avg_power_watts **(Σ)**
- avg_ram_pct **(Σ)**
- avg_storage_pct **(Σ)**
- cpu_cores **(Σ)**
- data_center_location
- health_score **(Σ)**
- health_status
- install_date
- rack_id
- ram_gb **(Σ)**

### `weather_performance_correlation`
- avg_cpu_pct **(Σ)**
- avg_network_mbps **(Σ)**
- avg_power_watts **(Σ)**
- avg_ram_pct **(Σ)**
- date
- heat_stress
- ingested_at
- location
- precipitation_in **(Σ)**
- temp_max_f **(Σ)**
- temp_min_f **(Σ)**
- windspeed_max_mph **(Σ)**

### `server_anomaly_scores`
- anomaly_flag
- anomaly_score
- cpu_pct
- data_center_location
- is_anomaly
- network_mbps
- power_watts
- ram_pct
- risk_level

## Source of truth
Since no separate gold-layer schema export was produced, the column lists above (and the exact
data types/values) should be cross-referenced against the corresponding files in
[`/data`](../../data):

| Semantic model table | CSV file |
|------------------------|----------|
| `incident_summary` | `data/incident_summary.csv` |
| `pue_metrics` | `data/pue_metrics.csv` |
| `server_health_scores` | `data/server_health_scores.csv` |
| `weather_performance_correlation` | `data/weather_performance_correlation.csv` |
| `server_anomaly_scores` | `data/server_anomaly_scores.csv` |
