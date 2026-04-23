import requests
import os

def get_latest_run():
    url = f"{os.getenv('DATABRICKS_HOST')}/api/2.1/jobs/runs/list"

    headers = {
        "Authorization": f"Bearer {os.getenv('DATABRICKS_TOKEN')}"
    }

    params = {
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "runs" in data and len(data["runs"]) > 0:
        return data["runs"][0]

    return None