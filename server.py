from fastmcp import FastMCP
from tools.connect_database import connect_database
from tools.get_schema import get_schema_tool
from tools.sample_rows import sample_rows
from tools.run_query import run_query
from tools.profile_table import profile_table_tool
from tools.analyze_schema import analyze_schema_tool
from tools.dataset_tools import (
    upload_dataset_tool,
    list_datasets_tool,
    query_dataset_tool
)
from tools.session_tools import create_session_tool
from datetime import datetime
from tools.generate_chart import generate_chart
from typing import List, Union
import logging
from pathlib import Path

# Get project root based on server file location
BASE_DIR = Path(__file__).resolve().parent

# Logs directory
logs_dir = BASE_DIR / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")


class LazyFileHandler(logging.Handler):
    """Only creates the log file when the first log message is emitted."""

    def __init__(self, logs_dir: Path):
        super().__init__()
        self._logs_dir = logs_dir
        self._real_handler = None

    def emit(self, record):
        if self._real_handler is None:
            log_filename = self._logs_dir / (datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log")
            self._real_handler = logging.FileHandler(str(log_filename))
            self._real_handler.setFormatter(self.formatter)
        self._real_handler.emit(record)


# Force logging config even if a root logger was already set up by imports
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
root_logger.addHandler(stream_handler)

lazy_file_handler = LazyFileHandler(logs_dir)
lazy_file_handler.setFormatter(formatter)
root_logger.addHandler(lazy_file_handler)

logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("AI Data Analyst MCP Server")

@mcp.tool()
def connect_database_tool(session_id: str, connection_uri: str):
    """
    Firstly create a session, then connect a user database to it with the specified session ID.
    """
    logger.info(f"Connecting database for session: {session_id}")
    return connect_database(session_id, connection_uri)

@mcp.tool()
def get_schema(session_id: str):
    """
    Fetches the database schema: tables and their columns.
    """
    logger.info("Fetching database schema...")
    return get_schema_tool(session_id)

@mcp.tool()
def sample_rows_tool(session_id: str, table_name: str, limit: int = 10):
    """
    Sample rows from a specified table.
    """
    logger.info(f"Sampling rows from table: {table_name}")
    return sample_rows(session_id, table_name, limit)

@mcp.tool()
def run_query_tool(session_id: str, sql: str):
    """
    Run a SQL query against the connected database and return results.
    """
    logger.info(f"Running SQL query: {sql}")
    return run_query(session_id, sql)

@mcp.tool()
def generate_chart_tool(
    data: List[dict],
    x_column: str,
    y_columns: Union[str, List[str]],
    chart_type: str = "auto",
    question: str = None,
    group_by: str = None
):
    """
    Generate a visualization from query results.

    Parameters
    ----------
    data : list of dict
        Query result rows returned from run_query.
    x_column : str
        Column to use for the X axis.
    y_columns : str or list
        Metric column(s) to visualize.
    chart_type : str
        Chart type (auto, bar, line, scatter, pie).
    question : str
        Optional user question used for smarter aggregation detection.
    group_by : str
        Optional column used to aggregate results before plotting.

    Returns
    -------
    dict
        {
            "status": "success",
            "chart": "<plotly html>",
            "insight": "optional generated insight"
        }
    """

    try:
        if not isinstance(data, list):
            raise ValueError("data must be a list of records")

        result = generate_chart(
            data=data,
            x_column=x_column,
            y_columns=y_columns,
            chart_type=chart_type,
            question=question,
            group_by=group_by
        )
        logger.info("Chart generated successfully")
        return result
    
    except Exception as e:
        logger.error("Chart generation failed")
        return {
            "status": "error",
            "message": str(e)
        }
    
@mcp.tool()
def profile_table(session_id: str, table: str):
    """
    Profile a database table to understand data distribution.
    """
    logger.info(f"Profiling table: {table}")
    return profile_table_tool(session_id, table)

@mcp.tool()
def analyze_schema(session_id: str):
    """
    Analyze database schema and detect relationships between tables
    """
    logger.info("Analyzing database schema...")
    return analyze_schema_tool(session_id)

@mcp.tool()
def upload_dataset(file_path: str, table_name: str = None):
    """
    Upload CSV/Excel/JSON dataset for analysis
    """
    return upload_dataset_tool(file_path, table_name)


@mcp.tool()
def list_datasets():
    """
    List uploaded datasets
    """
    return list_datasets_tool()


@mcp.tool()
def query_dataset(sql: str):
    """
    Run SQL queries on uploaded datasets
    """
    return query_dataset_tool(sql)

@mcp.tool()
def create_session() -> dict:
    """
    Create a new analysis session.

    Sessions allow the AI agent to store:
    - database connections
    - cached query results
    - temporary datasets

    Returns
    -------
    dict
        {
            "status": "success",
            "data": {
                "session_id": "..."
            }
        }
    """

    try:
        return create_session_tool()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@mcp.tool()
def hello():
    """
    Simple test tool to verify the server works.
    """
    logger.info("Hello tool called")
    return "MCP Server is running!"




if __name__ == "__main__":
    logger.info("Starting MCP server...")
    mcp.run()