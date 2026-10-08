import os
import time
from google.cloud import bigquery
import numpy as np
import pandas as pd
import requests

# ----------------------------------------------------------------------
# 1. SERVICE ACCOUNT AUTHENTICATION
# ----------------------------------------------------------------------
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
KEY_PATH = "key.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

client = bigquery.Client(project=PROJECT_ID)
DATASET_ID = f"{PROJECT_ID}.raw_layer"
print("Successfully authenticated via Service Account Key!")


# ----------------------------------------------------------------------
# 2. DATA EXTRACTION (WITH FALLBACK GENERATOR)
# ----------------------------------------------------------------------
def fetch_products_and_carts():
  """Fetches data from DummyJSON API or generates fallback dataset if API fails."""
  try:
    print("Fetching products from DummyJSON API...")
    res_p = requests.get(
        "https://dummyjson.com/products?limit=30", timeout=10
    )
    res_p.raise_for_status()
    products_data = [
        {
            "product_id": p["id"],
            "product_name": p["title"],
            "price": float(p["price"]),
            "category": p["category"],
        }
        for p in res_p.json()["products"]
    ]

    print("Fetching carts/orders from DummyJSON API...")
    res_c = requests.get("https://dummyjson.com/carts?limit=10", timeout=10)
    res_c.raise_for_status()

    orders_data = []
    np.random.seed(42)
    for cart in res_c.json()["carts"]:
      order_id = f"ORD-{cart['id']:05d}"
      user_id = f"CUST-{cart['userId']:04d}"
      order_date = pd.to_datetime("2026-09-01") + pd.Timedelta(
          days=int(np.random.randint(0, 30))
      )

      for item in cart["products"]:
        orders_data.append({
            "order_id": order_id,
            "customer_id": user_id,
            "product_id": item["id"],
            "quantity": item["quantity"],
            "order_date": order_date.date(),
            "status": np.random.choice(
                ["completed", "cancelled", "returned"], p=[0.85, 0.10, 0.05]
            ),
        })

    print("Successfully fetched online data!")
    return pd.DataFrame(products_data), pd.DataFrame(orders_data)

  except Exception as e:
    print(
        f"Network/API error encountered ({e}). Switching to local fallback"
        " data generator..."
    )
    # Synthetic fallback data generator
    np.random.seed(42)
    products_data = [
        {
            "product_id": i,
            "product_name": f"Product {i}",
            "price": round(np.random.uniform(10, 500), 2),
            "category": np.random.choice(
                ["Electronics", "Clothing", "Home", "Beauty"]
            ),
        }
        for i in range(1, 21)
    ]

    orders_data = []
    for i in range(1, 51):
      orders_data.append({
          "order_id": f"ORD-{i:05d}",
          "customer_id": f"CUST-{np.random.randint(1, 10):04d}",
          "product_id": np.random.randint(1, 21),
          "quantity": np.random.randint(1, 5),
          "order_date": (
              pd.to_datetime("2026-09-01")
              + pd.Timedelta(days=int(np.random.randint(0, 30)))
          ).date(),
          "status": np.random.choice(
              ["completed", "cancelled", "returned"], p=[0.85, 0.10, 0.05]
          ),
      })

    return pd.DataFrame(products_data), pd.DataFrame(orders_data)


df_products, df_orders = fetch_products_and_carts()

# Calculate total order amount
df_orders = df_orders.merge(
    df_products[["product_id", "price"]], on="product_id", how="left"
)
df_orders["total_amount"] = (
    df_orders["quantity"] * df_orders["price"]
).round(2)


# ----------------------------------------------------------------------
# 3. DATA QUALITY GATE
# ----------------------------------------------------------------------
def run_data_quality_checks(df: pd.DataFrame, df_name: str) -> bool:
  print(f"\n🔍 Data Quality Check: {df_name}")
  nulls = df.isnull().sum().sum()
  dups = df.duplicated().sum()
  print(f"   • Nulls: {nulls} | Duplicates: {dups}")
  return nulls == 0 and dups == 0


run_data_quality_checks(df_orders, "Raw Orders")
run_data_quality_checks(df_products, "Raw Products")


# ----------------------------------------------------------------------
# 4. DATA INGESTION TO BIGQUERY
# ----------------------------------------------------------------------
dataset = bigquery.Dataset(DATASET_ID)
dataset.location = "US"
client.create_dataset(dataset, exists_ok=True)


def load_df_to_bigquery(df: pd.DataFrame, table_name: str):
  table_ref = f"{DATASET_ID}.{table_name}"
  job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
  job = client.load_table_from_dataframe(
      df, table_ref, job_config=job_config
  )
  job.result()
  print(
      f" {len(df)} rows successfully loaded into BigQuery table: {table_ref}"
  )


load_df_to_bigquery(df_orders, "raw_orders")
load_df_to_bigquery(df_products, "raw_products")
