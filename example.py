# %%
import json

from decouple import config

from amplitude_data_wrapper import (
    get_chart,
    find_user,
    get_cohort,
    delete_user_data,
    get_deletion_jobs,
    export_project_data,
    get_all_event_types,
)

api_key = config("AMPLITUDE_EU_PROD_KEY")
api_secret = config("AMPLITUDE_EU_PROD_SECRET")
email = config("email")
chart_id_eu = config("chart_id_eu")
example_id_eu = config("example_id_eu")
cohort_id_eu = config("cohort_id_eu")
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
user = find_user(user=example_id_eu, api_key=api_key, secret=api_secret)
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
