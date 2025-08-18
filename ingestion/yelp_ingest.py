import os, sys, json, time, argparse, logging
from datetime import datetime, timezone
import requests                    # HTTP client
from google.cloud import storage   # GCS client
from google.cloud import bigquery  # BigQuery client

log = logging.getLogger("yelp_ingest")
log.setLevel(logging.INFO)
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
log.addHandler(_handler)

def make_timestamps():
    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d")     # folder partition
    ingested_at = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")  # row lineage
    return dt, ingested_at
# print(make_timestamps())

def resolve_env():
    env = os.getenv("ENV", "dev").lower()
    if env not in ("dev", "prod"):
        raise ValueError("ENV must be 'dev' or 'prod'")

    if env == "dev":
        cfg = {
            "env": env,
            "project": os.getenv("GCP_PROJECT_ID_DEV"),
            "bucket":  os.getenv("GCS_BUCKET_NAME_DEV"),
            "keyfile": os.getenv("GOOGLE_APPLICATION_CREDENTIALS_DEV"),
        }
    else:
        cfg = {
            "env": env,
            "project": os.getenv("GCP_PROJECT_ID_PROD"),
            "bucket":  os.getenv("GCS_BUCKET_NAME_PROD"),
            "keyfile": os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PROD"),
        }

    # Fail early if anything is missing
    for k, v in cfg.items():
        if not v:
            raise EnvironmentError(f"Missing {k} for ENV={env}")
    return cfg

# print("Configuration:", resolve_env())


def parse_args():
    p = argparse.ArgumentParser(description="Ingest Yelp businesses to GCS bronze (optional BQ).")
    p.add_argument("--term", type=str, help="search term, e.g. 'korean bbq'")
    p.add_argument("--location", type=str, help="e.g. 'Los Angeles, CA'")
    p.add_argument("--latitude", type=float, help="latitude if no location")
    p.add_argument("--longitude", type=float, help="longitude if no location")
    p.add_argument("--categories", type=str, help="e.g. 'korean,bbq'")
    p.add_argument("--per-page", type=int, default=50, help="Yelp max is 50")
    p.add_argument("--max-records", type=int, default=150, help="cap total fetch")
    p.add_argument("--dt", type=str, help="override partition date YYYY-MM-DD")
    p.add_argument("--write-bq", action="store_true", help="also load a raw BQ table")
    return p.parse_args()


print("Command line arguments:", parse_args())
