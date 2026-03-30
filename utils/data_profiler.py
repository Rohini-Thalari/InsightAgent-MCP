import logging
import pandas as pd
from sqlalchemy import text
from utils.cache_manager import cache
from database.schema_loader import get_schema

logger = logging.getLogger(__name__)

MAX_SAMPLE_ROWS = 1000


def _sql_profile_table(table, columns, engine):
    """Try profiling using SQL queries directly. Raises on failure."""

    col_profiles = {}
    total = 0

    with engine.connect() as conn:
        for col_info in columns:
            col_name = col_info["name"]
            if not col_name.isidentifier():
                logger.warning(f"Skipping invalid column name: {col_name}")
                continue
            col_type = col_info["type"].upper()

            # Basic stats via SQL
            basic_query = text(
                f"SELECT COUNT(*) AS total, "
                f"COUNT({col_name}) AS non_null, "
                f"COUNT(DISTINCT {col_name}) AS unique_vals "
                f"FROM {table}"
            )

            row = conn.execute(basic_query).fetchone()

            total = row[0]
            non_null = row[1]
            unique_vals = row[2]
            null_pct = (total - non_null) / total if total > 0 else 0.0

            col_profile = {
                "type": col_info["type"],
                "null_pct": float(null_pct),
                "unique_values": int(unique_vals)
            }

            is_numeric = any(kw in col_type for kw in [
                "INT", "FLOAT", "DOUBLE", "DECIMAL", "NUMERIC", "REAL", "BIGINT", "SMALLINT", "TINYINT"
            ])
            is_date = any(kw in col_type for kw in ["DATE", "TIME", "TIMESTAMP"])

            if is_numeric:
                stats_query = text(
                    f"SELECT MIN({col_name}), MAX({col_name}), AVG({col_name}) "
                    f"FROM {table}"
                )
                stats_row = conn.execute(stats_query).fetchone()

                col_profile.update({
                    "min": float(stats_row[0]) if stats_row[0] is not None else None,
                    "max": float(stats_row[1]) if stats_row[1] is not None else None,
                    "mean": float(stats_row[2]) if stats_row[2] is not None else None,
                })

            elif is_date:
                date_query = text(
                    f"SELECT MIN({col_name}), MAX({col_name}) "
                    f"FROM {table}"
                )
                date_row = conn.execute(date_query).fetchone()

                col_profile.update({
                    "min_date": str(date_row[0]) if date_row[0] is not None else None,
                    "max_date": str(date_row[1]) if date_row[1] is not None else None,
                })

            else:
                top_query = text(
                    f"SELECT {col_name}, COUNT(*) AS cnt "
                    f"FROM {table} "
                    f"WHERE {col_name} IS NOT NULL "
                    f"GROUP BY {col_name} "
                    f"ORDER BY cnt DESC "
                    f"LIMIT 5"
                )
                top_rows = conn.execute(top_query).fetchall()

                col_profile["top_values"] = [str(r[0]) for r in top_rows]

            col_profiles[col_name] = col_profile

    return {
        "table": table,
        "sample_size": total,
        "columns": col_profiles,
    }


def _pandas_profile_table(table, engine):
    """Fallback: profile using pandas on a sampled subset."""

    query = text(f"SELECT * FROM {table} LIMIT {MAX_SAMPLE_ROWS}")
    df = pd.read_sql(query, engine)

    if df.empty:
        return {
            "table": table,
            "message": "No data found"
        }

    profile = {
        "table": table,
        "sample_size": len(df),
        "columns": {}
    }

    for col in df.columns:

        series = df[col]

        col_profile = {
            "type": str(series.dtype),
            "null_pct": float(series.isnull().mean()),
            "unique_values": int(series.nunique())
        }

        if pd.api.types.is_numeric_dtype(series):

            col_profile.update({
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std())
            })

        elif pd.api.types.is_datetime64_any_dtype(series):

            col_profile.update({
                "min_date": str(series.min()),
                "max_date": str(series.max())
            })

        else:

            top_vals = series.value_counts().head(5).index.tolist()

            col_profile["top_values"] = top_vals

        profile["columns"][col] = col_profile

    return profile


def profile_table(table: str, engine):
    """
    Profile a table. Tries SQL-based profiling first (faster, no data transfer).
    Falls back to pandas profiling if any SQL query fails.
    """
    cache_key = f"profile_{table}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    schema = get_schema(engine)

    if table not in schema:
        raise ValueError(f"Invalid table: {table}")

    columns = schema[table]

    try:
        logger.info(f"Attempting SQL-based profiling for table: {table}")
        result = _sql_profile_table(table, columns, engine)
        logger.info(f"SQL-based profiling succeeded for table: {table}")
        cache.set(cache_key, result)
        return result
    except Exception as e:
        logger.warning(f"SQL profiling failed for table {table}: {e}. Falling back to pandas.")
        return _pandas_profile_table(table, engine)
