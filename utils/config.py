import os
from dotenv import load_dotenv

load_dotenv()

def load_cfg():
    env = os.getenv("ENV", "dev").lower()
    if env not in ("dev", "prod"):
        raise ValueError("ENV must be 'dev' or 'prod'")

    if env == "dev":
        return {
            "project": os.getenv("GCP_PROJECT_ID_DEV"),
            "bucket": os.getenv("GCS_BUCKET_NAME_DEV"),
            "bq_datasets": {
                "bronze": os.getenv("BQ_DATASET_BRONZE_DEV"),
                "silver": os.getenv("BQ_DATASET_SILVER_DEV"),
                "gold": os.getenv("BQ_DATASET_GOLD_DEV"),
            },
            "sa": os.getenv("GOOGLE_APPLICATION_CREDENTIALS_DEV"),
        }
    else:
        return {
            "project": os.getenv("GCP_PROJECT_ID_PROD"),
            "bucket": os.getenv("GCS_BUCKET_NAME_PROD"),
            "bq_datasets": {
                "bronze": os.getenv("BQ_DATASET_BRONZE_PROD"),
                "silver": os.getenv("BQ_DATASET_SILVER_PROD"),
                "gold": os.getenv("BQ_DATASET_GOLD_PROD"),
            },
            "sa": os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PROD"),
        }
