# %%
import json
import os

from dotenv import load_dotenv

import src.amplitude_data_wrapper.analytics_api as amp

# %%
load_dotenv()
api_key = os.getenv("AMPLITUDE_EU_PROD_KEY")
api_secret = os.getenv("AMPLITUDE_EU_PROD_SECRET")
test_api_key = os.getenv("AMPLITUDE_EU_TEST_KEY")
test_api_secret = os.getenv("AMPLITUDE_EU_TEST_SECRET")
email = os.getenv("email")
chart_id_eu = os.getenv("chart_id_eu")
example_id_eu = os.getenv("example_id_eu")
cohort_id_eu = os.getenv("cohort_id_eu")
# %%
# without proxy
r = amp.get_chart(
    api_key=api_key, secret=api_secret, chart_id=chart_id_eu, region=1
)  # region 1 is EU
r.status_code
# %%
r.json()  # returns data as json
# %%
r = amp.get_chart(
    secret=api_secret, api_key=api_key, chart_id=chart_id_eu, region=1
)  # region 1 is EU
r.status_code
# %%
# with proxy
proxies = {"http": "http://myproxy.example.org/method"}
r = amp.get_chart(api_key, api_secret, chart_id_eu, region=1, proxy=proxies)
r.status_code  # print status code
# %%
r.json()  # print data as json
# %%
user = amp.find_user(user=example_id_eu, api_key=api_key, secret=api_secret, region=1)
user.text  # print data
# %%
proxies = {"http": "http://myproxy.example.org/method"}
path = "data/cohortdata.csv"
url = ""
cohort = amp.get_cohort(
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
deleteme = amp.delete_user_data(
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
tobe_deleted = amp.get_deletion_jobs(
    start="2022-06-01",
    end="2022-07-01",
    api_key=api_key,
    secret=api_secret,
    region=1,
)
tobe_deleted.text
# %%
start = "20220501T09"
end = "20220501T11"
data = amp.export_project_data(
    start=start,
    end=end,
    api_key=api_key,
    secret=api_secret,
    filename="data/projectdata.zip",
    region=1,
)
# %%
types = amp.get_all_event_types(api_key=test_api_key, secret=test_api_secret, region=1)
types.status_code  # 200
types.text  # prints data
# %%
# write as json file
with open("data/test_types.json", "w") as f:
    json.dump(types.json(), f, ensure_ascii=False)
# %%
with open("data/test_types.json") as f:
    _ = f.read()
_ = json.loads(_)
dd = _["data"]
# %%
event_types = []
for i in dd:
    event_types.append(i["event_type"])
with open("data/test_event_names.json", "w") as f:
    json.dump(event_types, f, ensure_ascii=False)

# %%
# slett event_type med api
dtype = amp.delete_event_type(
    api_key=test_api_key, secret=test_api_secret, event_type="atque maxime ducimus"
)
dtype.status_code
# %%
# get an event with segments
our_event_dict = {
    "event_type": "pageview",
    "group_by": [{"type": "event", "value": "app"}, {"type": "event", "value": "team"}],
}
data = amp.get_event_segmentation(
    api_key=api_key,
    secret=api_secret,
    start="20220601",
    end="20220602",
    event=our_event_dict,
    metrics="uniques",
    interval=1,
    limit=1000,
)
# %%
data.json()  # print data as json
