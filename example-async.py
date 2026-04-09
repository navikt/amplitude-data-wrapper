# %%
import asyncio
import os
import json
from pathlib import Path
import logging

import aiohttp
from dotenv import load_dotenv

from src.amplitude_data_wrapper.async_api import (
    build_headers,
    download_one_chart,
)

# %%
"""
Download amplitude charts asynchronously 

Steps
1. set global variables in CONFIG section
2. prepare list of chart IDs as json
3. set required environment variables for API key and secret
4. run program:
    python example_async.py
"""
# %%
"""
CONFIG
"""
load_dotenv()
API_KEY = os.getenv("AMPLITUDE_TEST_KEY")
API_SECRET = os.getenv("AMPLITUDE_TEST_SECRET")
PROJECT_ID = os.getenv("AMPLITUE_TEST_PROJECT_ID")
SAVE_DIR = "data/charts"

"""
Chart IDs list
"""
with open("data/test_chart_ids.json") as b:
    data = json.load(b)

if type(data) is dict:
    chart_ids = data["chart_ids"]

"""
Project credentials
"""
PROJECT_CREDENTIALS: dict[str, dict] = {
    PROJECT_ID: {"key": API_KEY, "secret": API_SECRET, "charts": chart_ids}
}

logging.basicConfig(level=logging.INFO)

# %%


async def download_all() -> None:
    """
    Download all charts from a list

    Checks which charts are already downloaded in the download directory, and which are missing. Downloads missing charts.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []

        for project_id, cfg in PROJECT_CREDENTIALS.items():
            headers = build_headers(cfg["key"], cfg["secret"])

            project_dir = Path(SAVE_DIR) / project_id
            project_dir.mkdir(parents=True, exist_ok=True)

            # Determine which charts are already downloaded
            existing = {f.stem for f in project_dir.glob("*.json")}
            all_charts = set(cfg["charts"])
            missing = sorted(all_charts - existing)
            _ = list(missing)
            with open(f"{SAVE_DIR}/missing.json", "w", encoding="utf-8") as f:
                json.dump(_, f, indent=2)

            logging.info(
                f"Project {project_id}: {len(existing)} already downloaded, {len(missing)} missing"
            )

            for chart_id in missing:
                tasks.append(
                    download_one_chart(
                        session=session,
                        chart_id=chart_id,
                        headers=headers,
                        out_path=Path(f"{SAVE_DIR}/{project_id}/{chart_id}.json"),
                        region="us",
                    )
                )
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(download_all())
