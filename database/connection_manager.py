from sqlalchemy import create_engine,text
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.engine = None

    def connect(self, connection_uri: str):
        """Initialize database engine and test connection"""
        if self.engine is not None:
            logger.info("Database engine already initialized")
            return

        try:
            self.engine = create_engine(connection_uri)

            # test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info("Database connection successful")

        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

    def get_engine(self):
        if self.engine is None:
            raise RuntimeError("Database not connected")
        return self.engine

    def get_connection(self):
        if self.engine is None:
            raise RuntimeError("Database not connected")

        return self.engine.connect()


# global singleton
connection_manager = ConnectionManager()
