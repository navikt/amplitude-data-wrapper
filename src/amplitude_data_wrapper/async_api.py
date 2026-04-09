# %%
import asyncio
import base64
import json
from typing import Any
from pathlib import Path
import logging

import aiohttp

# %%
API_DOMAINS = {
    "eu": "https://analytics.eu.amplitude.com/api/3/chart",
    "us": "https://analytics.amplitude.com/api/3/chart",
}

logging.basicConfig(level=logging.INFO)


# %%
def build_headers(api_key: str, api_secret: str) -> dict:
    """
    Builds headers for API requests to amplitude servers

    Parameters
    -----------
    api_key: str, required
        API key for amplitude project
    api_secret: str, required
        API secret for amplitude project

    Returns
    --------
    headers: dict
        A dictionary containing basic authentication token
    """
    token = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


async def fetch_chart_json(
    session: aiohttp.ClientSession,
    chart_id: str,
    headers: dict,
    region: str = "eu",
    concurrency: int = 4,
    retries: int = 5,
    timeout: int = 20,
) -> Any | None:
    """
    Fetch chart data as json from amplitude

    Parameters
    ---------
    session:
        session for requests
    chart_id: str, required
        chart ID
    headers: dict, required
        headers for requests, see build_headers
    region: str, required
        select 'eu' or 'us' amplitude data centre
    concurrency: int, optional
        how many concurrent processes to spawn. Default is 4
    retries: int, optional
        how many times to retry a request. Default is 5
    timeout: int, optional
        how long to wait before timing out a request attempt. Default is 20

    Returns
    -------
    Chart data as Json or None
    """
    url = f"{API_DOMAINS[region]}/{chart_id}/query"
    sem = asyncio.Semaphore(concurrency)
    for attempt in range(1, retries + 1):
        async with sem:
            try:
                async with session.get(url, headers=headers, timeout=timeout) as resp:
                    if resp.status in (500, 502, 503, 504):
                        wait = 2**attempt
                        logging.warning(
                            f"[{chart_id}] Retry {attempt}/{retries} — HTTP {resp.status} — waiting {wait}s"
                        )
                        await asyncio.sleep(wait)
                        continue

                    if resp.status == 429:
                        wait = 300
                        txt = await resp.text()
                        logging.warning(
                            f"Chart {chart_id} - HTTP {resp.status} -> {txt[:429]} - now waiting {wait / 60} minutes"
                        )
                        await asyncio.sleep(wait)
                        continue

                    if resp.status == 404:
                        logging.error(f"[404] Chart not found: {chart_id}")
                        return None

                    if resp.status != 200:
                        txt = await resp.text()
                        logging.error(
                            f"[ERROR] Chart {chart_id} — HTTP {resp.status} → {txt[:200]}"
                        )
                        return None

                    return await resp.json()

            except asyncio.TimeoutError:
                logging.warning(f"[TIMEOUT] {chart_id} attempt {attempt}")
                await asyncio.sleep(2**attempt)

    logging.error(f"[FAILED] {chart_id} after all retries")
    return None


async def save_json(path: Path, data: dict) -> None:
    """
    Save chart dictionary as a json file at a given path

    Parameters
    ----------
    path: Path, required
        saves json as a file at a given path
    data: dict, require
        the chart data
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


async def download_one_chart(
    session: aiohttp.ClientSession,
    chart_id: str,
    headers: dict,
    out_path: Path,
    region: str = "eu",
    concurrency: int = 4,
    retries: int = 5,
    timeout: int = 20,
) -> None:
    """
    Downloads data for a specific chart

    Parameters
    -----------
    session: aiohttp.ClientSession, required
        session for making the request
    chart_id: str, required
        Chart ID at amplitude
    headers: dict, required
        headers for API requests to amplitude
    out_path: Path, required
        a Path for saving chart data as a json file

    region: str, required
        select 'eu' or 'us' amplitude data centre
    concurrency: int, optional
        how many concurrent processes to spawn. Default is 4
    retries: int, optional
        how many times to retry a request. Default is 5
    timeout: int, optional
        how long to wait before timing out a request attempt. Default is 20
    """
    data = await fetch_chart_json(
        session=session,
        chart_id=chart_id,
        headers=headers,
        region=region,
        concurrency=concurrency,
        retries=retries,
        timeout=timeout,
    )
    if data is None:
        return

    await save_json(out_path, data)
    logging.info(f"Saved {out_path}")
