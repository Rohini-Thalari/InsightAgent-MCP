from sqlalchemy import inspect
from utils.cache_manager import cache


SYSTEM_TABLE_PREFIXES = ["pg_", "sqlite_", "information_schema"]


def analyze_schema(engine):
    """
    Analyze database schema including tables, columns, keys and relationships.
    """

    cache_key = "schema_analysis"
    cached = cache.get(cache_key)
    if cached:
        return cached
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    schema_info = {}
    relationships = []

    for table in tables:

        if any(table.startswith(prefix) for prefix in SYSTEM_TABLE_PREFIXES):
            continue

        columns = inspector.get_columns(table)
        pk = inspector.get_pk_constraint(table)
        fks = inspector.get_foreign_keys(table)
        indexes = inspector.get_indexes(table)

        schema_info[table] = {
            "columns": [
                {
                    "name": c["name"],
                    "type": str(c["type"])
                }
                for c in columns
            ],
            "primary_keys": pk.get("constrained_columns", []),
            "foreign_keys": [],
            "indexes": [idx["column_names"] for idx in indexes]
        }

        for fk in fks:

            constrained = fk.get("constrained_columns", [])
            referred_cols = fk.get("referred_columns", [])

            if not constrained or not referred_cols:
                continue

            fk_info = {
                "column": constrained[0],
                "references_table": fk.get("referred_table"),
                "references_column": referred_cols[0]
            }

            schema_info[table]["foreign_keys"].append(fk_info)

            relationships.append({
                "left_table": table,
                "left_column": constrained[0],
                "right_table": fk.get("referred_table"),
                "right_column": referred_cols[0]
            })
    
    cache.set(cache_key, {
        "tables": schema_info,
        "relationships": relationships
    })
    return {
        "tables": schema_info,
        "relationships": relationships
    }
