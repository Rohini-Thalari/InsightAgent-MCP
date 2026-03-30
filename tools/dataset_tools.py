from datasets.dataset_manager import upload_dataset, list_datasets, query_dataset


def upload_dataset_tool(file_path: str, table_name: str = None):

    try:

        result = upload_dataset(file_path, table_name)

        return {
            "status": "success",
            "dataset": result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


def list_datasets_tool():

    return {
        "status": "success",
        "datasets": list_datasets()
    }


def query_dataset_tool(sql: str):

    try:

        rows = query_dataset(sql)

        return {
            "status": "success",
            "rows": rows
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }