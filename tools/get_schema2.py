from database.schema_loader import get_schema
from utils.session_manager import session_manager

def format_schema_text(schema):

    text = ""

    for table, columns in schema.items():

        text += f"\nTable: {table}\nColumns:\n"

        for col in columns:
            text += f"- {col['name']} ({col['type']})\n"

    return text


def get_schema_tool(session_id: str):

    try:
        engine = session_manager.get_engine(session_id)
        schema = get_schema(engine)
        schema_text = format_schema_text(schema)

        return {
            "status": "success",
            "schema_dict": schema,
            "schema_text": schema_text
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }