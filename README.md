# E-Commerce End-to-End Analytics Pipeline & DWH Model

An end-to-end data engineering and analytics solution designed to transform raw e-commerce operational data into actionable business intelligence using **Python, Google BigQuery, dbt, and Tableau Public**.

---

## Business Case & Problem Statement

An e-commerce business faced operational challenges due to fragmented data sources, missing product metadata, and a lack of real-time visibility into executive financial metrics. Decision-makers were unable to track revenue fluctuations, analyze basket sizes, or evaluate sales across distinct product categories in a centralized place.
To simulate a real-world e-commerce analytics challenge using public API data, this project addresses the common operational issue of fragmented data sources, missing product metadata, and a lack of centralized financial visibility...

**Project Goal:** Design and deploy a modern data pipeline that extracts operational data via API, ingests it into a cloud data warehouse, transforms raw tables into a star schema using dbt, enforces automated data quality checks, and publishes an interactive dashboard for executive decision-making.

---

## Pipeline Architecture

```text
               [ External API / DummyJSON ]
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Python Ingestion Script (ingest_data.py)                │
│ • Requests & Pandas Extraction                          │
│ • Fault-Tolerant Fallback Synthetic Data Generator      │
│ • Pre-ingestion Data Quality Gate (Nulls & Duplicates)  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Google BigQuery (Raw Layer)                             │
│ • raw_orders & raw_products                             │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ dbt Transformations (Star Schema Modeling)              │
│ • Staging: stg_orders, stg_products                     │
│ • Marts: fct_orders, dim_products, dim_customers, date  │
│ • Automated Data Quality Tests & Referential Integrity  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Tableau Public Interactive Dashboard                    │
│ • Executive Financial KPIs (Total Revenue, Orders, AOV) │
│ • Category Breakdown & Dynamic Time-Series Filtering    │
└─────────────────────────────────────────────────────────┘
