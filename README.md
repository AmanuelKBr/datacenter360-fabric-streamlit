# DataCenter360 Intelligence Platform
### Enterprise Data Engineering Portfolio Project
**Built on Microsoft Fabric | Streamlit | Python | PySpark | Power BI**

---

## 🔗 Live Demo
👉 **[DataCenter360 Streamlit App](https://datacenter360-intelligence-platform.streamlit.app/)**

---

## 📌 Project Overview
DataCenter360 is an end-to-end enterprise data platform simulating real-world **data center operations analytics** for a multi-site facility in Ashburn, VA — the world's largest data center hub.

The platform ingests, transforms, and serves operational data across a full **Medallion Architecture** (Bronze → Silver → Gold) built entirely on **Microsoft Fabric**, with automated daily pipelines, interactive dashboards, and a machine learning anomaly detection model.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                          │
│  Google Sheets (DCIM Simulation)  │  Open-Meteo REST API    │
│  server_inventory                 │  Daily weather forecast  │
│  incident_log                     │  Ashburn, VA coords      │
│  capacity_utilization             │  Temp, precipitation,    │
│                                   │  windspeed, weathercode  │
└──────────────────┬────────────────────────────┬─────────────┘
                   ↓                            ↓
┌─────────────────────────────────────────────────────────────┐
│              INGESTION LAYER (Microsoft Fabric)              │
│  Data Factory Pipeline          │  PySpark Notebook          │
│  HTTP Connector → CSV parsing   │  REST API → JSON flatten   │
│  3 tables → lh_bronze           │  1 table → lh_bronze       │
└──────────────────────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│              BRONZE LAYER  (lh_bronze)                       │
│  Raw Delta Tables — append only, never modified              │
│  server_inventory │ incident_log │ capacity_utilization      │
│  weather_ashburn                                             │
└──────────────────────────────────────────────────────────────┘
                   ↓  PySpark Notebook (nb_transform_silver)
┌─────────────────────────────────────────────────────────────┐
│              SILVER LAYER  (lh_silver)                       │
│  Cleansed, typed, validated, deduplicated Delta Tables       │
│  • String → correct data types (Float, Int, Date, Timestamp) │
│  • Range validation (0-100% utilization checks)              │
│  • Referential integrity (incidents → valid server_ids)      │
│  • Deduplication on primary keys                             │
└──────────────────────────────────────────────────────────────┘
                   ↓  PySpark Notebook (nb_transform_gold)
┌─────────────────────────────────────────────────────────────┐
│              GOLD LAYER  (lh_gold)                           │
│  Business-ready aggregates for BI and ML consumption         │
│  server_health_scores          │  incident_summary           │
│  pue_metrics                   │  weather_performance_       │
│  server_anomaly_scores (ML)    │  correlation                │
└──────────────────────────────────────────────────────────────┘
                   ↓                            ↓
┌──────────────────────┐        ┌───────────────────────────────┐
│  Power BI (DirectLake)│        │  Streamlit App (Public)       │
│  5-page Report        │        │  6-page interactive dashboard │
│  Executive Dashboard  │        │  Hosted on Streamlit Cloud    │
└──────────────────────┘        └───────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| **Cloud Platform** | Microsoft Fabric (Trial) |
| **Storage** | OneLake — Delta Tables |
| **Ingestion** | Data Factory HTTP Connector |
| **Transformation** | PySpark Notebooks |
| **Orchestration** | Fabric Data Pipeline (Scheduled Daily 6AM ET) |
| **BI & Dashboards** | Power BI DirectLake |
| **ML Model** | Scikit-learn Isolation Forest |
| **ML Tracking** | MLflow (Fabric Native Experiment) |
| **Web App** | Streamlit + Plotly |
| **Hosting** | Streamlit Cloud (Free) |
| **Version Control** | GitHub |
| **Language** | Python, PySpark, SQL |

---

## 📊 Data Model

### Source 1 — Google Sheets (DCIM Simulation)
| Table | Rows | Description |
|-------|------|-------------|
| `server_inventory` | 25 | Server specs across 3 locations |
| `incident_log` | 55 | Operational incidents Oct 2024 → Jan 2025 |
| `capacity_utilization` | 151 | CPU, RAM, storage, power readings |

### Source 2 — Open-Meteo REST API
| Table | Rows | Description |
|-------|------|-------------|
| `weather_ashburn` | 19 | Daily weather — Ashburn, VA (39.04°N, 77.49°W) |

### Gold Layer Business Tables
| Table | Description |
|-------|-------------|
| `server_health_scores` | Composite health score per server (0-100) |
| `incident_summary` | MTTR, severity breakdown by location |
| `pue_metrics` | PUE proxy metric by location and timestamp |
| `weather_performance_correlation` | Weather vs server performance join |
| `server_anomaly_scores` | ML anomaly predictions with risk levels |

---

## 🤖 ML Model — Anomaly Detection

**Algorithm:** Isolation Forest (Unsupervised)
**Features:** CPU %, RAM %, Storage %, Network Mbps, Power Watts
**Training Data:** 151 server utilization records
**Contamination Rate:** 10% (based on historical incident frequency)

| Risk Level | Count | Action |
|------------|-------|--------|
| High Risk | 3 readings | Immediate investigation |
| Medium Risk | 13 readings | Monitor closely |
| Low Risk | 135 readings | Normal operations |

> Isolation Forest was chosen because it requires no labeled failure data — ideal for anomaly detection in operational systems where failures are rare and unlabeled.

---

## 📈 Power BI Report Pages

| Page | Key Visuals |
|------|-------------|
| **Server Health** | Health scores, CPU vs RAM scatter, status breakdown |
| **Incident Analysis** | MTTR by type, severity heatmap, open incidents |
| **PUE & Power** | PUE proxy vs industry threshold, power by location |
| **Weather & Performance** | Temp vs power correlation, heat stress distribution |
| **Predictive Alerts** | ML risk levels, anomaly distribution by location |

---

## 🌐 Streamlit App Pages

| Page | Description |
|------|-------------|
| **Executive Summary** | KPI overview including ML anomaly alerts |
| **Server Health** | Interactive filters, health scores, utilization scatter |
| **Incident Analysis** | Resolution times, severity breakdown, incident table |
| **PUE & Power** | PUE distribution, power vs CPU scatter |
| **Weather & Performance** | Temperature correlation, heat stress analysis |
| **Predictive Alerts** | ML anomaly scores, risk table, location breakdown |

---

## ⚙️ Pipeline Orchestration

```
pl_master_datacenter360 (Runs Daily at 6:00 AM ET)
│
├── pl_ingest_gsheets_bronze     ← Google Sheets → lh_bronze
├── nb_ingest_weather_bronze     ← Open-Meteo API → lh_bronze
├── wait (120s)
├── nb_transform_silver          ← Bronze → Silver transformations
├── wait (180s)
└── nb_transform_gold            ← Silver → Gold aggregations
                                    + CSV export for Streamlit
├── sm_refresh                   ← Semantic Model Refresh 
                                    To ensure the report refreshes only after the Lakehouse Gold data is updated
```

---

## 🚧 Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Fivetran ADLS auth blocked on Trial | Switched to Data Factory HTTP connector |
| Open-Meteo nested JSON fails in Copy Activity | Built PySpark notebook for API ingestion |
| Spark session capacity limits on Trial | Added Wait activities between pipeline steps |
| Delta schema conflicts on table overwrites | DROP TABLE before overwrite pattern |
| Date gaps between weather and capacity data | Fetched historical archive from Open-Meteo |
| MLflow `start_run` incompatibility on Fabric Trial | Used `mlflow.set_experiment()` direct logging |

> These challenges and their resolutions represent real-world data engineering problem-solving — documented here intentionally as portfolio evidence.

---

## 📁 Repository Structure

```
datacenter360-fabric-streamlit/
├── app.py                          # Streamlit application
├── requirements.txt                # Python dependencies
├── data/
│   ├── server_health_scores.csv
│   ├── incident_summary.csv
│   ├── pue_metrics.csv
│   ├── weather_performance_correlation.csv
│   └── server_anomaly_scores.csv
└── README.md
```

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/AmanuelKBr/datacenter360-fabric-streamlit.git
cd datacenter360-fabric-streamlit

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 👤 Author
**Amanuel Birri**
📧 amanuelkbirri@gmailc.om
💼 [LinkedIn] www.linkedin.com/in/amanuel-birri

---

## 📄 License
MIT License — free to use and reference with attribution.