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

```

## Data Ingestion & Extraction (Python)

The ingestion script (`scripts/ingest_data.py`) extracts raw operational records and loads them into BigQuery:
* **API Integration:** Connects to REST endpoints (`dummyjson.com/products` and `dummyjson.com/carts`) via `requests` and `pandas`.
* **Pipeline Resilience:** Features an automated fallback data generator (`try-except`) that generates synthetic records if the public API service experiences outages or rate limits.
* **Pre-Ingestion Quality Gate:** Validates datasets for missing values (`nulls == 0`) and duplicate records (`duplicates == 0`) before executing loads.
* **Automated DWH Loading:** Pushes staging DataFrames directly into Google BigQuery's `raw_layer` dataset using the BigQuery Python SDK with `WRITE_TRUNCATE` disposition.

---

## Data Warehouse Modeling (Star Schema)

To optimize query performance for analytical reporting, raw records are transformed into a **Star Schema** using **dbt (data build tool)** in Google BigQuery.

### Lineage Graph & Model Structure:

![Data Warehouse Star Schema](assets/er_diagram.png)

### Model Architecture:
* **Staging Layer (`stg_orders`, `stg_products`):** Standardizes column naming conventions, casts data types, and normalizes raw JSON payloads.
* **Fact Table (`fct_orders`):** Order-level grain containing numeric measures (`quantity`, `price`, `total_amount`) and surrogate foreign keys connecting to dimensions.
* **Dimension Tables:**
  * `dim_products`: Catalog dimensional details (title, category, unit price).
  * `dim_customers`: Customer identifiers and operational metadata.
  * `dim_date`: Date dimension facilitating continuous time-series trend analysis.

---

## Data Quality & Testing

Data integrity is enforced at both the ingestion layer and the warehouse model level:
* **dbt Assertions (`schema.yml`):**
  * **Primary Key Constraints:** `unique` and `not_null` assertions on all surrogate keys across dimension and fact tables.
  * **Referential Integrity:** Validated foreign key relationships between `fct_orders` and all surrounding dimension models.
* **Python Pre-Check:** Automated validation gate preventing corrupted raw payloads from reaching the DWH.

---

## Executive BI Dashboard (Tableau)

An interactive analytics dashboard built in **Tableau Public** connected to the BigQuery data marts.

![Tableau Dashboard](assets/dashboard.png)

🔗 **[View Live Interactive Dashboard on Tableau Public]( https://public.tableau.com/app/profile/olenka.olen/viz/E-CommerceSalesAnalyticsDashboarddbtBigQuery/E-CommerceSalesAnalyticsDashboarddbtBigQuery)** 

### Key Business Metrics Defined:
* **Total Revenue:** Sum of net revenue generated across all completed orders.
* **Total Orders:** Volume of fulfilled customer transactions.
* **Average Order Value (AOV):** Calculated as $\frac{\text{Total Revenue}}{\text{Total Orders}}$ to measure basket size and evaluate pricing efficiency.

### Core Business Features:
* **Category Breakdown:** Horizontal bar chart illustrating sales distribution across categories (e.g., Furniture, Fragrances, Beauty, Groceries).
* **Sales Trend Analysis:** Time-series tracking revenue fluctuations across transaction dates.
* **Dynamic Interactivity:** Integrated `Use as Filter` actions allowing stakeholders to select specific product categories to dynamically recalculate KPIs and line-chart trends.

---

## Tech Stack & Tools

* **Language:** Python 3.x (`pandas`, `requests`, `google-cloud-bigquery`)
* **Cloud Data Warehouse:** Google BigQuery
* **Data Transformation & Modeling:** dbt (data build tool)
* **BI Visualization:** Tableau Public
* **Version Control:** Git & GitHub

---

## Project Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Elen12344321/analytics-project.git](https://github.com/Elen12344321/analytics-project.git)
   cd analytics-project
   ```

2. **Environment Configuration:**
   Place your GCP Service Account credentials as `key.json` in the root directory and set environment variables:
   ```bash
   export GCP_PROJECT_ID="your-gcp-project-id"
   export GOOGLE_APPLICATION_CREDENTIALS="key.json"
   ```

3. **Run Data Ingestion:**
   ```bash
   python scripts/ingest_data.py
   ```

4. **Run dbt Transformations & Tests:**
   ```bash
   dbt run
   dbt test
   ```

   
   
