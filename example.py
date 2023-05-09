# %%
import json
import os

from dotenv import load_dotenv

from amplitude_data_wrapper import (
    get_chart,
    find_user,
    get_cohort,
    delete_user_data,
    get_deletion_jobs,
    export_project_data,
    get_all_event_types,
    get_event_segmentation,
)
# %%
load_dotenv()
api_key = os.getenv('AMPLITUDE_EU_PROD_KEY')
api_secret = os.getenv("AMPLITUDE_EU_PROD_SECRET")
email = os.getenv("email")
chart_id_eu = os.getenv("chart_id_eu")
example_id_eu = os.getenv("example_id_eu")
cohort_id_eu = os.getenv("cohort_id_eu")
# %%
# without proxy
r = get_chart(api_key, api_secret, chart_id_eu, region=1)  # region 1 is EU
r.status_code
# %%
# with proxy
proxies = {"http": "http://myproxy.example.org/method"}
r = get_chart(api_key, api_secret, chart_id_eu, region=1, proxy=proxies)
r.status_code  # print status code
# %%
user = find_user(user=example_id_eu, api_key=api_key, secret=api_secret, region=1)
user.text  # print data
# %%
proxies = {"http": "http://myproxy.example.org/method"}
path = "data/cohortdata.csv"
url = ""
cohort = get_cohort(
    api_key,
    api_secret,
    cohort_id_eu,
    filename=path,
    props=1,
    region=1,
    proxy=proxies,
)
# %%
user_data = json.loads(user.text)
deleteme = delete_user_data(
    user["matches"][0]["amplitude_id"],
    email=email,
    api_key=api_key,
    secret=api_secret,
    region=1,
    ignore_invalid_id=True,
    delete_from_org=False,
)
deleteme.text
# %%
tobe_deleted = get_deletion_jobs(
    start="2022-06-01",
    end="2022-07-01",
    api_key=api_key,
    secret=api_secret,
    region=1,
)
tobe_deleted.text
# %%
start = "20220601T00"
end = "20220601T01"
data = export_project_data(
    start=start,
    end=end,
    api_key=api_key,
    secret=api_secret,
    filename="data/projectdata.zip",
    region=1,
)
# %%
types = get_all_event_types(api_key=api_key, secret=api_secret, region=1)
types.status_code  # 200
types.text  # prints data
# %%
# get an event with segments
our_event_dict = {
    "event_type": "pageview",
    "group_by": [{"type": "event", "value": "app"}, {"type": "event", "value": "team"}],
}
data = get_event_segmentation(
    api_key=api_key,
    secret=api_secret,
    start="20220601",
    end="20220602",
    event=our_event_dict,
    metrics="uniques",
    interval=1,
    limit=1000,
)
