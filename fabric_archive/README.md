# Fabric Artifacts Archive

This folder preserves the source artifacts of the **DataCenter360** Microsoft Fabric workspace
before the trial capacity expires. The Fabric trial does not support Git integration, Power BI
embedding, or offline `.pbix` export, so each item below is preserved manually through the
Fabric UI and committed here as plain files (notebooks, schema scripts, DAX, PDFs, screenshots).

Combined with `app.py` and the gold-layer CSVs already in `/data`, this archive is enough to:
- Rebuild the Fabric workspace from scratch (notebooks, pipeline logic, schemas, semantic model)
- Demonstrate the full implementation to portfolio reviewers without a live Fabric workspace

## Checklist

- [ ] Notebooks (4) → `notebooks/`
- [ ] Pipelines (2) → `pipelines/`
- [ ] Semantic model → `semantic_model/`
- [ ] Reports & Dashboard → `reports/`
- [ ] Lakehouse schemas → `lakehouse_schemas/`
- [ ] Lakehouse bronze/silver data samples → `lakehouse_data/`
- [ ] ML experiment results → `ml_experiment/`

---

## 1. Notebooks (do this first — quickest win)

For each of these notebooks:
- `nb_ingest_weather_bronze`
- `nb_transform_silver`
- `nb_transform_gold`
- `nb_mi_anomaly_detection`

1. Open the notebook in Fabric
2. **File → Export this notebook → Download as `.ipynb`** (or `.py`)
3. Save the file into `fabric_archive/notebooks/`

> Skip `sm_datacenter360_memory analyzer_2134` — this is an auto-generated Fabric utility
> notebook, not part of the project.

---

## 2. Pipelines

Pipelines can't be exported to a file on the trial, so document them with screenshots + notes.

For `pl_ingest_gsheets_bronze` and `pl_master_datacenter360`:

1. Open the pipeline canvas and take a full screenshot of the whole canvas
   → save to `pipelines/screenshots/`
2. Click each activity → screenshot its **General / Source / Destination / Settings** tabs
   → save to `pipelines/screenshots/`
3. For any dynamic content / expressions (the `fx` icon), copy the expression text
4. Fill in the matching template:
   - `pipelines/pl_ingest_gsheets_bronze.md`
   - `pipelines/pl_master_datacenter360.md`

---

## 3. Semantic Model (`sm_datacenter360`)

Open `sm_datacenter360` — it opens in the web modeling view.

1. **Model view**: screenshot the relationship diagram → `semantic_model/relationships.png`
2. Click each **measure** — the formula bar shows the full DAX expression. Copy each one into
   `semantic_model/sm_datacenter360_measures.md`
3. For each table, note its columns/types into `semantic_model/sm_datacenter360_tables.md`
   (the gold layer tables are already documented in the main README's Data Model section,
   so you mainly need to confirm and add any calculated columns/measures)

---

## 4. Reports & Dashboard

For **DataCenter360 Operations Report** and **DataCenter360 Executive Dashboard**:

1. Open the item
2. **File → Export to PDF** (captures every page with current data, works without offline pbix)
   → save to `reports/`
3. Optionally also **File → Export → PowerPoint**
4. Take a few high-resolution screenshots of key pages for the main project README
   → save to `reports/screenshots/`

---

## 5. Lakehouse Schemas & Data

The **gold layer is already preserved** as CSVs in `/data` — no action needed for `lh_gold`.

For `lh_bronze` and `lh_silver`:

1. Open the Lakehouse's **SQL analytics endpoint**
2. For each table: right-click → **"Script table as" → CREATE** → paste the DDL into
   `lakehouse_schemas/lh_bronze_schema.sql` or `lh_silver_schema.sql`
3. Run `SELECT TOP 100 * FROM <table>` for each table, then use **"Download as CSV"** on the
   results grid → save into `lakehouse_data/bronze/` or `lakehouse_data/silver/`

---

## 6. ML Experiment

For `DataCenter360_AnomalyDetection` (and the `nb_mi_anomaly_detection` experiment):

1. Open the experiment, screenshot the runs list (parameters & metrics columns)
2. Click into the best run, screenshot the metrics/parameters detail panel
3. Save screenshots into `ml_experiment/`

> The training code itself is preserved in `notebooks/nb_mi_anomaly_detection.ipynb`,
> and the model output is preserved in `/data/server_anomaly_scores.csv`.

---

## Folder structure

```
fabric_archive/
├── README.md
├── notebooks/
│   ├── nb_ingest_weather_bronze.ipynb
│   ├── nb_transform_silver.ipynb
│   ├── nb_transform_gold.ipynb
│   └── nb_mi_anomaly_detection.ipynb
├── pipelines/
│   ├── pl_ingest_gsheets_bronze.md
│   ├── pl_master_datacenter360.md
│   └── screenshots/
├── semantic_model/
│   ├── sm_datacenter360_measures.md
│   ├── sm_datacenter360_tables.md
│   └── relationships.png
├── reports/
│   └── screenshots/
├── lakehouse_schemas/
│   ├── lh_bronze_schema.sql
│   └── lh_silver_schema.sql
├── lakehouse_data/
│   ├── bronze/
│   └── silver/
└── ml_experiment/
```
