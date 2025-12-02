# sync_gist.py

# Import the requests library to handle HTTP requests
import requests

# Import json to serialize/deserialize JSON data
import json

# Import asyncio for asynchronous support and scheduling
import asyncio

# Import aiofiles for asynchronous file read/write
import aiofiles

# Import os in case you need to use file path manipulation later
import os

# Import datetime to add timestamps to logs
from datetime import datetime

from dotenv import load_dotenv

# Create headers for authentication and API versioning
load_dotenv()

GIST_FILENAME = "longterm_lists.json"
LOCAL_FILE = "longterm_lists.json"
GIST_URL = f"https://api.github.com/gists/{os.getenv("GIST_ID")}"
HEADERS = {
    "Authorization": f"token {os.getenv("GITHUB_TOKEN")}",
    "Accept": "application/vnd.github.v3+json"
}


# -------------------------------
# Function: pull_gist
# Purpose: Downloads the Gist file and saves it locally
# -------------------------------
async def pull_gist():
    
    # Log that a pull is starting
    print(f"[{datetime.now()}] Pulling Gist...")

    # Make a GET request to fetch the Gist content
    response = requests.get(GIST_URL, headers=HEADERS)

    # If request was successful
    if response.status_code == 200:

        # Parse JSON from response
        data = response.json()

        # Extract the actual file content by filename
        content = data["files"][GIST_FILENAME]["content"]

        # Open the local file asynchronously for writing (overwrite mode)
        async with aiofiles.open(LOCAL_FILE, "w", encoding="utf-8") as f:
            await f.write(content)  # Save content to disk

        # Confirm successful save
        print(f"[{datetime.now()}] Pulled and saved to {LOCAL_FILE}")

    # If request failed, log the error
    else:
        print(f"[ERROR] Failed to pull Gist: {response.status_code} - {response.text}")


# -------------------------------
# Function: push_gist
# Purpose: Reads the local file and updates the Gist with it
# -------------------------------
async def push_gist():

    # Log that a push is starting
    print(f"[{datetime.now()}] Pushing Gist...")

    # Open the local file asynchronously for reading
    async with aiofiles.open(LOCAL_FILE, "r", encoding="utf-8") as f:
        content = await f.read()  # Read file contents

    # Create a JSON payload in the Gist update format
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": content  # New content to replace the old file
            }
        }
    }

    # Send a PATCH request to update the Gist
    response = requests.patch(GIST_URL, headers=HEADERS, data=json.dumps(payload))

    # If update succeeded
    if response.status_code == 200:
        print(f"[{datetime.now()}] Pushed successfully.")

    # If update failed, log error
    else:
        print(f"[ERROR] Failed to push Gist: {response.status_code} - {response.text}")


# -------------------------------
# Function: start_sync_loop
# Purpose: Sync loop that pulls at startup and pushes every 30 minutes
# -------------------------------
async def start_sync_loop():

    # Run an initial pull on startup to ensure local file is up to date
    await pull_gist()

    # Start an infinite loop to continue pushing periodically
    while True:

        # Sleep for 1800 seconds (30 minutes) between each push
        await asyncio.sleep(1800)

        # Push the latest local file to Gist
        await push_gist()
