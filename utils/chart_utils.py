import pandas as pd
import plotly.express as px

def detect_aggregation(question: str, column: str, df: pd.DataFrame):
    """ Detect the best aggregation function dynamically """ 
    column_lower = column.lower()
    # 1️⃣ Detect from question intent 
    if question:
        q = question.lower()
        if any(w in q for w in ["average", "avg", "mean"]):
            return "mean"
        if any(w in q for w in ["count", "number", "how many"]):
            return "count"
        if any(w in q for w in ["max", "highest", "top"]):
            return "max"
        if any(w in q for w in ["min", "lowest"]):
            return "min"
        if any(w in q for w in ["total", "sum"]):
            return "sum"
    # 2️⃣ Detect from column name
    if any(k in column_lower for k in ["revenue", "sales", "amount", "profit", "quantity"]):
        return "sum"
    if any(k in column_lower for k in ["count", "num", "orders", "users"]):
        return "count"
    if any(k in column_lower for k in ["rating", "score", "price", "age"]):
        return "mean"
    # 3️⃣ Detect from datatype
    if pd.api.types.is_numeric_dtype(df[column]):
        return "sum"
    # fallback
    return None

def detect_chart_type(df, x_column, y_columns):
    if pd.api.types.is_datetime64_any_dtype(df[x_column]):
        return "line"
    if len(y_columns) > 1:
        return "line"
    if pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_columns[0]]):
        return "scatter"
    if df[x_column].nunique() <= 10:
        return "pie"
    return "bar"

def create_chart(
    data,
    x_column,
    y_columns,
    question=None,
    chart_type="auto",
    group_by=None
):
    """
    Advanced chart creation utility
    """
    df = pd.DataFrame(data)

    if df.empty:
        return {
            "chart": "<p>No data available</p>",
            "insight": "No data returned from query"
        }
    if isinstance(y_columns, str):
        y_columns = [y_columns]

    if group_by:
        agg_dict = {}
        
        for col in y_columns:
            agg = detect_aggregation(question, col, df) or "sum"
            if agg:
                agg_dict[col] = agg
        df = df.groupby(group_by)[y_columns].agg(agg_dict).reset_index()
        x_column = group_by

    #detect chart type if auto
    if chart_type == "auto":
        chart_type = detect_chart_type(df, x_column, y_columns)

    if chart_type == "line":
        fig = px.line(df, x=x_column, y=y_columns)

    elif chart_type == "bar":
        fig = px.bar(df, x=x_column, y=y_columns)

    elif chart_type == "scatter":
        fig = px.scatter(df, x=x_column, y=y_columns[0])

    elif chart_type == "pie":
        fig = px.pie(df, names=x_column, values=y_columns[0])

    else:
        raise ValueError("Unsupported chart type")

    fig.update_layout(
        template="plotly_white",
        height=500,
        hovermode="x unified"
    )

    insight = None

    if len(y_columns) == 1:
        y = y_columns[0]
        if df[y].iloc[-1] > df[y].iloc[0]:
            insight = f"{y} shows an increasing trend."
        else:
            insight = f"{y} shows a decreasing trend."

    return {
        "chart": fig.to_html(full_html=False, include_plotlyjs=False),
        "insight": insight
    }