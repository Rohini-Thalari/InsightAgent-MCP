from sqlalchemy import create_engine, text
from utils.session_manager import session_manager
import logging

logger = logging.getLogger(__name__)


def connect_database(session_id: str, connection_uri: str):
    """
    Connect user database to a session.
    """

    if "://" not in connection_uri:
        return {
            "status": "error",
            "message": "Invalid connection URI format"
        }

    try:
        session = session_manager.get_session(session_id)

        engine = create_engine(connection_uri)

        # test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        session["db_engine"] = engine

        logger.info(f"Database connected for session: {session_id}")

        return {
            "status": "success",
            "message": "Database connected"
        }

    except Exception as e:

        logger.error(f"Database connection failed: {str(e)}")

        return {
            "status": "error",
            "message": str(e)
        }