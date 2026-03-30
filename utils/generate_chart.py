from utils.chart_utils import create_chart


def generate_chart(
    data,
    x_column,
    y_columns,
    chart_type="auto",
    question=None,
    group_by=None
):
    """
    Generate chart from query result
    """

    try:

        if not data:
            return {
                "status": "error",
                "message": "No data provided for chart generation"
            }
        if isinstance(y_columns, str):
            y_columns = [y_columns]

        chart_result = create_chart(
            data=data,
            x_column=x_column,
            y_columns=y_columns,
            question=question,
            chart_type=chart_type,
            group_by=group_by
        )

        return {
            "status": "success",
            "chart": chart_result["chart"],  # ✅ fixed key
            "insight": chart_result.get("insight"),
            "chart_type": chart_type
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
