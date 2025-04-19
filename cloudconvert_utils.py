import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
CLOUDCONVERT_API_KEY = os.getenv("CLOUDCONVERT_API_KEY")

def convert_file_to_csv(filename, file_bytes):
    if not CLOUDCONVERT_API_KEY:
        raise Exception("Missing CLOUDCONVERT_API_KEY in .env")

    headers = {
        "Authorization": f"Bearer {CLOUDCONVERT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Step 1: Create the job
    try:
        response = requests.post("https://api.cloudconvert.com/v2/jobs", json={
            "tasks": {
                "import-1": {"operation": "import/upload"},
                "convert-1": {
                    "operation": "convert",
                    "input": "import-1",
                    "output_format": "csv"
                },
                "export-1": {"operation": "export/url", "input": "convert-1"}
            }
        }, headers=headers)

        if response.status_code != 201:
            raise Exception(f"CloudConvert job creation failed: {response.text}")

        job = response.json()
        job_id = job["data"]["id"]
        
        # Get the first upload task (import-1)
        upload_task = next(t for t in job["data"]["tasks"] if t["name"] == "import-1")
        upload_url = upload_task["result"]["form"]["url"]
        upload_params = upload_task["result"]["form"]["parameters"]

        # Step 2: Upload the file
        upload_response = requests.post(
            upload_url, 
            data=upload_params, 
            files={'file': (filename, file_bytes)}
        )

        if upload_response.status_code != 204:
            raise Exception(f"CloudConvert file upload failed: {upload_response.text}")

        # Step 3: Poll job status until finished
        while True:
            status_response = requests.get(
                f"https://api.cloudconvert.com/v2/jobs/{job_id}", 
                headers=headers
            )
            if status_response.status_code != 200:
                raise Exception(f"Failed to check job status: {status_response.text}")

            job_status = status_response.json()
            status = job_status["data"]["status"]
            
            if status == "finished":
                break
            if status == "error":
                raise Exception(f"CloudConvert job failed: {job_status}")
            time.sleep(2)

        # Step 4: Get the download link
        export_task = next(t for t in job_status["data"]["tasks"] if t["name"] == "export-1")
        file_url = export_task["result"]["files"][0]["url"]

        # Step 5: Download the converted CSV
        download_response = requests.get(file_url)
        download_response.raise_for_status()
        return download_response.content

    except Exception as e:
        raise Exception(f"CloudConvert conversion failed: {str(e)}")