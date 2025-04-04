# %%
import json
import logging
import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from tqdm.auto import tqdm
from urllib3.util import Retry

logging.basicConfig(level=logging.INFO)
# %%
api_domains = {1: "https://analytics.eu.amplitude.com", 2: "https://amplitude.com"}


# %%
def get_chart(
    api_key: str, secret: str, chart_id: str, proxy: dict | None = None, region: int = 1
) -> requests.Response:
    """
    Get data for an existing chart in Amplitude

    See https://developers.amplitude.com/docs/dashboard-rest-api#results-from-an-existing-chart

    Parameters
    ---------
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    chart_id: str, required
        The ID of the chart. For example  https://analytics.amplitude.com/demo/chart/abc123
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.

    Returns
    ----------
    r: requests object with results
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = api_domains
    r = requests.get(
        f"{url[region]}/api/3/chart/{chart_id}/query",
        params={},
        headers=headers,
        auth=(api_key, secret),
        proxies=proxy,
    )
    logging.info("Success. Retrieved data for chart_id %s", chart_id)
    return r


# %%
def find_user(
    user: str, api_key: str, secret: str, proxy: dict | None = None, region: int = 1
) -> requests.Response:
    """
    Find the Amplitude ID for a user based on a type of ID, for example Device ID or User ID.

    See https://developers.amplitude.com/docs/dashboard-rest-api#user-search

    Parameters
    ---------
    user: str, required
      The user you want to identify. Can use Device ID or User ID.
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.

    Returns
    ----------
    user_id: requests object with results
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = api_domains
    r = requests.get(
        f"{url[region]}/api/2/usersearch?user={user}",
        params={},
        headers=headers,
        auth=(api_key, secret),
        proxies=proxy,
    )
    logging.info("Success. Found user %s", user)
    return r


# %%
def get_cohort(
    api_key: str,
    api_secret: str,
    cohort_id: str,
    filename: str,
    proxy: dict | None = None,
    props: int = 0,
    region: int = 1,
) -> str:
    """
    Downloads a cohort of users from Amplitude

    See https://developers.amplitude.com/docs/behavioral-cohorts-api#getting-one-cohort

    Parameters
    ---------
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    cohort_id: str, required
        ID for the cohort
    props: int, required
        Set to 0 if you only want Amplitude IDs, or 1 if you want more user data
    filename: str, required
        Path and filename to store the results. Example: "data/cohortdata.csv"
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.

    Returns
    ---------
    filename: path filename as a string to a csv containing data for the cohort
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    url = api_domains
    response = s.get(
        f"{url[region]}/api/5/cohorts/request/{cohort_id}",
        params={"props": props},
        headers=headers,
        auth=(api_key, api_secret),
        stream=True,
        timeout=600,
        proxies=proxy,
    )
    response.raise_for_status()
    json_response = response.json()
    for key, value in json_response.items():
        logging.info("%s : %s", key, value)
    header_status = 0
    request_id = json_response["request_id"]
    while header_status != 200:
        status_response = s.get(
            f"{url[region]}/api/5/cohorts/request-status/{request_id}",
            headers=headers,
            auth=(api_key, api_secret),
            stream=True,
            timeout=600,
            proxies=proxy,
        )
        status_response.raise_for_status()

        if status_response.status_code == 202:
            logging.info("Waiting for request_id %s to be completed", request_id)
            time.sleep(5)
        elif status_response.status_code == 200:
            download_url = f"{url[region]}/api/5/cohorts/request/{request_id}/file"
            logging.info("Downloading from %s", download_url)
            file_download = s.get(
                download_url,
                headers=headers,
                auth=(api_key, api_secret),
                stream=True,
                timeout=600,
                proxies=proxy,
            )
            file_download.raise_for_status()
            with tqdm.wrapattr(
                open(filename, "wb"),
                "write",
                miniters=1,
                total=int(file_download.headers.get("content-length", 0)),
                desc=filename,
            ) as fout:
                for chunk in file_download.iter_content(chunk_size=8192):
                    fout.write(chunk)
            header_status = 200
        else:
            logging.error(
                f"An error occurred, retrying to reach request ID {request_id} and request URL {download_url} in 10 seconds"
            )
            time.sleep(10)

    return filename


# %%
def delete_user_data(
    deletion_list: list,
    user_ids: list,
    email: str,
    api_key: str,
    secret: str,
    proxy: dict | None = None,
    region: int = 1,
    ignore_invalid_id: bool = False,
    delete_from_org: bool = False,
) -> requests.Response:
    """
    Delete user data for one or more users

    See https://developers.amplitude.com/docs/user-deletion#post

    Parameters
    ---------
    deletion_list: required
      One or more Amplitude IDs you want to delete user data for
    email: required
      email for the user in Amplitude requesting the data be deleted
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    ignored_invalid_id: bool, required
        Ignore any invalid user IDs(users that do no exist in the project) that were passed in
    delete_from_org: bool, required
        delete from the entire org rather than just this project. Can only be used with portfolio orgs (have the Portfolio feature enabled) and with user ids only. Values can be either 'True' or 'False' and by default it is set to False
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.

    Returns
    ----------
    r: requests object with results
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = api_domains
    r = requests.post(
        f"{url[region]}/api/2/deletions/users",
        data={
            "amplitude_ids": deletion_list,
            "user_ids": user_ids,
            "requester": email,
            "ignore_invalid_id": ignore_invalid_id,
            "delete_from_org": delete_from_org,
        },
        headers=headers,
        auth=(api_key, secret),
        proxies=proxy,
    )
    logging.info("Sletter brukere")
    return r


# %%
def get_deletion_jobs(
    start: str,
    end: str,
    api_key: str,
    secret: str,
    proxy: dict | None = None,
    region: int = 1,
) -> requests.Response:
    """
    Get an overview of all deletion jobs in Amplitude

    See https://developers.amplitude.com/docs/user-deletion#get

    Parameters
    ---------
    start: str, required
        Start date for a period of deletion jobs. Formated as YYYY-MM-DD, for example 2021-10-01 for october 1 2021
    end: str, required
        End dat for a period of deletion jobs. Should add 30 days to the start date. Formated as YYYY-MM-DD, for example 2021-10-15 for october 15 2021
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.

    Returns
    ---------
    r: requests object with results
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = api_domains
    r = requests.get(
        f"{url[region]}/api/2/deletions/users",
        params={"start_day": start, "end_day": end},
        headers=headers,
        auth=(api_key, secret),
        proxies=proxy,
    )
    return r


# %%
def export_project_data(
    start: str,
    end: str,
    api_key: str,
    secret: str,
    filename: str,
    proxy: dict | None = None,
    region: int = 1,
) -> str:
    """
    Download all project data from an Amplitude project for a time period, max 365 days per request

    See https://developers.amplitude.com/docs/export-api

    Parameters
    ---------
    start: str, required
        The date for the start of the requested timeperiod. Must be formated as YYYYMMDDTHH, for example 20210101T00 = january 1 2021 at 00:00
    end: str, required
        The dat for the end of the requested timeperiode. Must be formated as YYYYMMDDTHH, for example 20210101T23 = january 1 2021 at 23:00
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    filename: str, required
        filename and path to the project data. Example: "data/projectdata.zip"
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.


    Returns
    ----------
    filename: zip-file containing multiple gzip files, one for each hour
    """
    filename = filename
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    urls = api_domains
    s = requests.Session()
    response = s.get(
        f"{urls[region]}/api/2/export",
        params={"start": start, "end": end},
        headers=headers,
        auth=(api_key, secret),
        stream=True,
        proxies=proxy,
    )
    logging.info("Export request submitted")
    response.raise_for_status()
    header_status = 0
    while header_status != 200:
        logging.info("Waiting for response")
        if response.status_code == 400:
            logging.info(
                "The file size of the exported data is too large. Shorten the time ranges and try again. The limit size is 4GB."
            )
        elif response.status_code == 404:
            logging.info(
                "Request data for a time range during which no data has been collected for the project, then you will receive a 404 response from our server."
            )
        elif response.status_code == 504:
            logging.info(
                "The amount of data is large causing a timeout. For large amounts of data, the Amazon S3 destination is recommended."
            )
        elif response.status_code == 200:
            logging.info("Success. Downloading file as %s", filename)
            with tqdm.wrapattr(
                open(filename, "wb"),
                "write",
                miniters=1,
                total=int(response.headers.get("content-length", 0)),
                desc=filename,
            ) as fout:
                for chunk in response.iter_content(chunk_size=8192):
                    fout.write(chunk)
            header_status = 200
        else:
            logging.error("Some other error occurred. Retrying again in 10 seconds.")
            time.sleep(10)
    return filename


# %%
def get_all_event_types(
    api_key: str, secret: str, proxy: dict | None = None, region: int = 1
) -> requests.Response:
    """
    Get a list of all event-types for a project in Amplitude

    See https://developers.amplitude.com/docs/taxonomy-api#get-all-event-types

    Parameters
    ---------
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.

    Returns
    ----------
    r: requests object with results
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = api_domains
    r = requests.get(
        f"{url[region]}/api/2/taxonomy/event",
        headers=headers,
        auth=(api_key, secret),
        proxies=proxy,
    )
    return r


# %%
def delete_event_type(
    api_key: str,
    secret: str,
    event_type: str,
    proxy: dict | None = None,
    region: int = 1,
) -> requests.Response:
    """
    Delete an even type for a project in Amplitude

    See https://www.docs.developers.amplitude.com/analytics/apis/taxonomy-api/#delete-an-event-type

    Parameters
    ----------
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    event_type: str, required
        name of the event type to be deleted from the Amplitude project
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.

    Returns
    ----------
    r: requests object with status result

    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = api_domains
    r = requests.delete(
        f"{url[region]}/api/2/taxonomy/event/{event_type}",
        headers=headers,
        auth=(api_key, secret),
        proxies=proxy,
    )
    return r


# %%
def get_event_segmentation(
    api_key: str,
    secret: str,
    start: str,
    end: str,
    event: dict,
    metrics: Any,
    interval: int = 1,
    segment: Any = None,
    group: Any = None,
    limit: int = 100,
    region: int = 1,
) -> requests.Response:
    """
    Get metrics for an event with segmentation

    See https://developers.amplitude.com/docs/dashboard-rest-api#event-segmentation

    Parameters
    ---------
    api_key: str, required
        API key for the project in Amplitude
    secret: str, required
        API secret for the project in Amplitude
    region: int, optional
        Region of the data centre. Default is 1 for Europe, and 2 for USA.
    start: date, required
        YYYYMMDD
    end, dato, required
        YYYYMMDD
    event: dict, required
        1 or 2 event-types with filter
    metrics: optional
        non-property metrics
    interval: optional
        time interval for the query. -300000, -3600000, 1, 7, or 30 for realtime, per hour, day, week and month. Default is 1.
    segment:
        segment
    group:
        group by
    limit: int
        Number of rows. Default is 100, max is 1000.
    proxy: dict | None = None, optional
        Set proxy with custom domain and path. Example: {"http": "http://myproxy.example.org/path"}

        Default is no proxy.


    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url = api_domains
    r = requests.get(
        f"{url[region]}/api/2/events/segmentation",
        params={
            "e": json.dumps(event),
            "m": metrics,
            "start": start,
            "end": end,
            "i": interval,
            "s": segment,
            "limit": limit,
        },
        headers=headers,
        auth=(api_key, secret),
    )
    return r
