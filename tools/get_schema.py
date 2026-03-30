from database.schema_loader import get_schema
from utils.session_manager import session_manager
import logging

logger = logging.getLogger(__name__)


def get_schema_tool(session_id: str):
    """
    Tool to fetch database schema : tables and their columns.
    """

    try:
        logger.info("Fetching database schema")
        engine = session_manager.get_engine(session_id)
        schema = get_schema(engine)
        return {
            "status": "success",
            "schema": schema
        }
    except Exception as e:
        logger.error("Schema fetch failed")
        logger.error(str(e))
        return {
            "status": "error",
            "message": "Database not connected",
            "details": str(e)
        }
    

