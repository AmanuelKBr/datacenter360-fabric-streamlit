# Semantic Model: sm_datacenter360 — Measures

**No DAX measures are defined in this semantic model.**

All Power BI report visuals (Server Health, Incident Analysis, PUE & Power, Weather & Performance,
Predictive Alerts) use **direct aggregates on gold-layer table columns** — i.e., the columns
themselves have a default summarization (Sum or Average) set in the model, marked with a **Σ**
icon in the modeling view, and the report visuals reference those columns directly with the
desired aggregation (e.g., `Average of avg_cpu_pct`, `Sum of total_incidents`).

See [`sm_datacenter360_tables.md`](sm_datacenter360_tables.md) for the full list of columns and
which ones carry a default aggregation.

## Future enhancement
As noted during the archival process, this is an area for future improvement: introducing
relationships between the gold tables (e.g., on `data_center_location`) and replacing raw column
aggregates with explicit DAX measures (for clearer naming, reusable business logic, and more
advanced calculations such as ratios, time-intelligence, or anomaly-rate metrics) would make the
model more robust and maintainable.
