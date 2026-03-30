import pandas as pd
import logging

from database.schema_loader import get_schema
from utils.session_manager import session_manager

logger = logging.getLogger(__name__)


def sample_rows(session_id: str, table: str, limit: int = 10):
    """
    Return sample rows from a table
    """
    try:
        engine = session_manager.get_engine(session_id)
        schema = get_schema(engine)
        if table not in schema:
            return {
                "status": "error",
                "message": f"Table '{table}' does not exist"
            }
        limit = min(limit, 50)

        query = f"SELECT * FROM {table} LIMIT {limit}"

        logger.info(f"Sampling rows from {table}")

        df = pd.read_sql(query, engine)

        return {
            "status": "success",
            "table": table,
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records")
        }

    except Exception as e:

        logger.error("Sample rows failed")

        return {
            "status": "error",
            "message": str(e)
        }