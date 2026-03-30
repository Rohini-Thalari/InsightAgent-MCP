import re

def validate_sql(sql: str):
    """
    Prevent dangerous SQL queries
    """

    forbidden = [
        "DROP",
        "DELETE",
        "UPDATE",
        "ALTER",
        "INSERT",
        "TRUNCATE",
        "MERGE",
        "GRANT",
        "REVOKE"
    ]

    sql_clean = sql.strip().upper()
    if ";" in sql:
        raise Exception("Multiple SQL statements are not allowed")

    for word in forbidden:
        if re.search(rf"\b{word}\b", sql_clean):
            raise Exception(f"Forbidden SQL operation detected: {word}")

    if not (sql_clean.strip().startswith("SELECT") or sql_clean.strip().startswith("WITH")):
        raise Exception("Only SELECT and WITH queries are allowed")

    return True
