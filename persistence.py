import os
import json
from pyspark.sql import SparkSession, DataFrame
from dotenv import load_dotenv

load_dotenv()

DATALAKE_PATH = os.environ["DATALAKE_PATH"]
BRONZE_PATH = os.path.join(DATALAKE_PATH, 'bronze')


def get_session(name="persistence"):
    return SparkSession.builder.appName(name).getOrCreate()


def _save_in_bronze(data: dict):
    """Save raw data in datalake/bronze/query/{date}.json"""
    folder = os.path.join(BRONZE_PATH, f"query={data['query']}")
    os.makedirs(folder, exist_ok=True)
    file_name = os.path.join(folder, f"capture_date={data['capture_date']}.json")
    curated_data = json.dumps(data, ensure_ascii=False).encode('utf-8').decode()
    with open(file_name, "a") as f:
        f.write(curated_data+"\n")


def save(json_data: dict):
    _save_in_bronze(json_data)
