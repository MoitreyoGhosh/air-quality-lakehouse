# Computational Environmental Intelligence Framework (CEIF)

> **A Research-Oriented Environmental Intelligence Lakehouse for Near Real-Time Air Quality Analytics, Explainable Forecasting, and Decision Support**

---

## Overview

The **Computational Environmental Intelligence Framework (CEIF)** is an end-to-end environmental analytics platform designed to integrate heterogeneous air quality and weather datasets into a unified **Lakehouse Architecture**. The framework provides a scalable pipeline for historical data ingestion, validation, preprocessing, analytics, forecasting, explainable AI, and environmental decision support.

The primary objective of the framework is to bridge multiple environmental data sources into a standardized, analytics-ready repository that supports real-time monitoring, scientific analysis, machine learning, and policy-driven decision making.

The framework currently integrates **17 monitoring stations across Kolkata, India**, combining historical observations from the **West Bengal Pollution Control Board (WBPCB)** with weather observations and forecasts from **Open-Meteo APIs**.

---

## Project Objectives

- Build a scalable Environmental Lakehouse Architecture.
- Standardize heterogeneous environmental datasets.
- Integrate multi-source air quality and weather observations.
- Generate analytics-ready curated datasets.
- Support near real-time monitoring.
- Enable explainable air quality forecasting.
- Provide environmental insights for decision support systems.

---

## Data Sources

### Air Quality

- West Bengal Pollution Control Board (WBPCB)
- Historical Air Quality Monitoring Data
- 17 Monitoring Stations

### Weather

- Open-Meteo Historical Weather API
- Open-Meteo Forecast API
- Open-Meteo Air Quality API

### Metadata

- Station Metadata
- Geographic Coordinates
- Administrative Information
- Dataset Lineage Information

---

# System Architecture

The framework follows a modern **Environmental Data Lakehouse** architecture.

```
Data Sources
      │
      ▼
Historical Ingestion
      │
      ▼
Schema Discovery
      │
      ▼
Column Normalization
      │
      ▼
Alias Resolution
      │
      ▼
Schema Mapping
      │
      ▼
Bronze Layer
      │
      ▼
Station Metadata
      │
      ▼
Silver Layer
      │
      ▼
Silver Validation
      │
      ▼
Gold Layer (Feature Engineering)
      │
      ▼
Analytics
      │
      ▼
Forecasting
      │
      ▼
Decision Support
```

---

# Current Implementation Status

## ✅ Data Engineering

- Historical data ingestion
- Schema discovery
- Automatic schema inference
- Column normalization
- Alias resolution
- Canonical schema mapping
- Dataset validation
- Metadata generation

---

## ✅ Bronze Layer

Raw canonical datasets are stored without modification.

Features include:

- Dataset lineage preservation
- Metadata registration
- DuckDB persistence
- Parquet storage
- Ingestion logging
- Validation logging

Outputs:

- Bronze DuckDB tables
- Bronze Parquet datasets
- Dataset registry
- Ingestion reports

---

## ✅ Station Metadata

Automatically generated metadata including:

- Station IDs
- Station names
- Geographic coordinates
- Administrative regions
- Source dataset mapping

---

## ✅ Silver Layer

Curated master datasets are generated for downstream analytics.

### WBPCB Master

- Duplicate removal
- Empty column removal
- Datetime generation
- Station mapping
- Metadata integration

### Weather Master

- Historical weather consolidation
- Station mapping
- Timestamp validation
- Duplicate removal

### Environment Master

Unified environmental dataset created by merging:

- Air Quality
- Weather
- Station Metadata

using

- Station ID
- Datetime

This produces a clean, analytics-ready environmental dataset.

---

## ✅ Silver Validation

Automated validation framework including:

- Dataset integrity validation
- Duplicate detection
- Missing value analysis
- Station coverage validation
- Datetime coverage validation
- Weather coverage analysis
- Source agreement validation

Validation metrics include:

- MAE
- RMSE
- Bias
- Pearson Correlation
- Circular Wind Direction Error

Reports are automatically generated after each pipeline execution.

---

# Lakehouse Layers

## Bronze

Purpose:

- Immutable raw canonical datasets
- Dataset lineage
- Metadata preservation

---

## Silver

Purpose:

- Cleaned datasets
- Standardized schema
- Integrated master datasets
- Analytics-ready data

---

## Gold *(Planned)*

Will contain:

- Feature Engineering
- AQI Categories
- Lag Features
- Rolling Statistics
- Daily Aggregations
- Monthly Aggregations
- Forecast-ready datasets
- ML-ready datasets
- Dashboard datasets

---

# Technology Stack

## Programming

- Python

## Storage

- DuckDB
- Apache Parquet

## Data Processing

- Pandas
- NumPy

## APIs

- WBPCB
- Open-Meteo Weather API
- Open-Meteo Air Quality API

## Machine Learning *(Planned)*

- XGBoost
- Random Forest
- Prophet
- LSTM
- GRU
- Temporal Fusion Transformer

## Explainable AI *(Planned)*

- SHAP
- Feature Importance
- Temporal Contribution Analysis

---

# Project Structure

```
data/
├── raw/
├── bronze/
├── silver/
├── gold/
└── metadata/

reports/
├── validation/
├── silver_validation/
└── analytics/

src/
├── connectors/
├── ingestion/
├── preprocessing/
├── lakehouse/
├── analytics/
├── forecasting/
├── visualization/
└── database/
```

---

# Pipeline Workflow

```
Historical Data
        │
        ▼
Validation
        │
        ▼
Bronze Layer
        │
        ▼
Station Metadata
        │
        ▼
Silver Layer
        │
        ▼
Silver Validation
        │
        ▼
Gold Layer
        │
        ▼
Analytics
        │
        ▼
Forecasting
        │
        ▼
Decision Support
```

---

# Future Roadmap

The next development stages include:

- Gold Layer implementation
- Advanced Feature Engineering
- Environmental Analytics
- Exploratory Data Analysis (EDA)
- Explainable Forecasting Models
- Near Real-Time Prediction Pipeline
- Interactive Dashboard
- Decision Support System
- Automated Scheduling
- Continuous Model Retraining
- API Services
- Research Publication Support

---

# Research Vision

The framework aims to provide a reproducible and extensible platform for computational environmental intelligence by combining data engineering, analytics, machine learning, and explainable AI within a unified Lakehouse architecture. The long-term goal is to support environmental monitoring agencies, researchers, policymakers, and urban planners through reliable, transparent, and scalable environmental intelligence.