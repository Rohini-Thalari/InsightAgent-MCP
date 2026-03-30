from utils.schema_analyzer import analyze_schema
from utils.session_manager import session_manager


def analyze_schema_tool(session_id: str):

    try:
        engine = session_manager.get_engine(session_id)
        schema = analyze_schema(engine)

        return {
            "status": "success",
            "schema_analysis": schema
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }