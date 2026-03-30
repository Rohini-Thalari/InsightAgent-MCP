        import os
import pandas as pd
from sqlalchemy import create_engine

DATASET_DB = "datasets/datasets.db"

# create SQLite engine for uploaded datasets
engine = create_engine(f"sqlite:///{DATASET_DB}")

DATASETS = {}


def upload_dataset(file_path: str, table_name: str = None):

    if not os.path.exists(file_path):
        raise ValueError("File not found")

    ext = file_path.split(".")[-1].lower()

    if ext == "csv":
        df = pd.read_csv(file_path)

    elif ext in ["xlsx", "xls"]:
        df = pd.read_excel(file_path)

    elif ext == "json":
        df = pd.read_json(file_path)

    else:
        raise ValueError("Unsupported file type")

    if table_name is None:
        table_name = os.path.basename(file_path).split(".")[0]

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    DATASETS[table_name] = {
        "rows": len(df),
        "columns": list(df.columns)
    }

    return {
        "table_name": table_name,
        "rows": len(df),
        "columns": list(df.columns)
    }


def list_datasets():

    return DATASETS


def query_dataset(sql: str):

    df = pd.read_sql(sql, engine)

    return df.to_dict(orient="records")
