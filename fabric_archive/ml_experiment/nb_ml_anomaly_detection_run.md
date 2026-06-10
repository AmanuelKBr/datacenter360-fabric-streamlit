# MLflow Experiment: nb_ml_anomaly_detection — Run Details

Captured from the Fabric MLflow run view before trial expiration. This documents the trained
Isolation Forest model behind the `server_anomaly_scores` gold table (see
[README — ML Model](../../README.md#-ml-model--anomaly-detection)).

> Note on naming: the Fabric workspace item was originally named `nb_mi_anomaly_detection`
> (notebook + experiment). The notebook source is preserved here as
> [`../notebooks/nb_ml_anomaly_detection.ipynb`](../notebooks/nb_ml_anomaly_detection.ipynb).

## Run Summary

| Field | Value |
|-------|-------|
| Run name | `affable_box_sl8rg0...` |
| Run ID | `9e5b9074-a130-4cac-9ba8-a75aa914ab7e` |
| Operation (Livy) ID | `78b5ee3c-853e-4d43-83e1-546db757fe0a` |
| Experiment | `nb_ml_anomaly_detection1` |
| Status | Completed |
| Created by | Amanuel Birri |
| Start time | 2026-04-24 4:58 PM |
| Duration | 9.91s |

## Run Parameters (model hyperparameters)

| Parameter | Value |
|-----------|-------|
| `bootstrap` | `False` |
| `contamination` | `0.1` |
| `max_features` | `1.0` |
| `max_samples` | `auto` |
| `n_estimators` | `100` |
| `n_jobs` | `None` |
| `random_state` | `42` |
| `verbose` | `0` |
| `warm_start` | `False` |

## Run Tags

| Tag | Value |
|-----|-------|
| `estimator_class` | `sklearn.ensemble._iforest.IsolationForest` |
| `estimator_name` | `IsolationForest` |

## Model Schema

| | Type |
|---|------|
| **Input** | `Tensor(dtype=float32, shape=[-1, 5])` — 5 features: CPU %, RAM %, Storage %, Network Mbps, Power Watts |
| **Output** | `Tensor(dtype=int64, shape=[-1])` — Isolation Forest anomaly label (`-1` = anomaly, `1` = normal), mapped to `is_anomaly` / `risk_level` in `server_anomaly_scores` |

## Result Summary (per README)

| Risk Level | Count |
|------------|-------|
| High Risk | 3 readings |
| Medium Risk | 13 readings |
| Low Risk | 135 readings |
