import json
from utils.data_profiler import profile_table
from database.schema_loader import get_schema
from utils.session_manager import session_manager


def profile_table_tool(session_id: str, table: str):
    """
    Profile a database table to understand data distribution
    """

    # Handle case where table is passed as JSON string e.g. '{"table": "users"}'
    if isinstance(table, str) and table.strip().startswith("{"):
        try:
            parsed = json.loads(table)
            if isinstance(parsed, dict) and "table" in parsed:
                table = parsed["table"]
        except (json.JSONDecodeError, KeyError):
            pass

    try:
        engine = session_manager.get_engine(session_id)
        schema = get_schema(engine)
        if table not in schema:
            raise ValueError(f"Table '{table}' does not exist in database")
        result = profile_table(table, engine)
        return {
            "status": "success",
            "table": table,
            "profile": result
        }
    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
