import pandas as pd
import logging
from security.sql_validator import validate_sql
from utils.session_manager import session_manager

logger = logging.getLogger(__name__)

def run_query(session_id: str, sql: str):
    """
    Run a SQL query against the connected database and return results.
    """
    try:
        validate_sql(sql)
        logger.info(f"Executing SQL query: {sql}")

        engine = session_manager.get_engine(session_id)

        df = pd.read_sql(sql, engine)

        return {
            "status": "success",
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records")
        }

    except Exception as e:
        logger.error(f"Error occurred while executing SQL query: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }