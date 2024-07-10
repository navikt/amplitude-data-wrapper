# Amplitude data wrapper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a wrapper for [Amplitude](https://amplitude.com/) APIs. You can use it to query and export data from your account and use the taxonomy API.

Built with [requests](https://requests.readthedocs.io/en/latest/) and [tqdm](https://github.com/tqdm/tqdm)

**Why use this package instead of other wrappers?**

This package supports regions and so you can use it with Amplitude accounts in the EU and USA.

This package also supports using a proxy so you can keep your project API keys and API secrets confidential.

## Supported Amplitude APIs and docs

- [Amplitude data wrapper](#amplitude-data-wrapper)
  - [Supported Amplitude APIs and docs](#supported-amplitude-apis-and-docs)
    - [Dashboard Rest API](#dashboard-rest-api)
    - [Privacy API](#privacy-api)
    - [Cohort API](#cohort-api)
    - [Export API](#export-api)
    - [Taxonomy API](#taxonomy-api)

See examples below and in [example.py](example.py)

Install with

```
pip install amplitude-data-wrapper
```

### Dashboard Rest API

[Results from an existing chart](https://developers.amplitude.com/docs/dashboard-rest-api#results-from-an-existing-chart)

Get data from EU account by setting `region=1`.

```python
import amplitude_data_wrapper.analytics_api as amp

# without proxy
r = amp.get_chart(
    api_key=api_key, secret=api_secret, chart_id=chart_id_eu, region=1
)  # region 1 is EU
r.status_code
r.json() # returns data as json
```

Get data from US account by setting `region=2`.

```python
r = amp.get_chart(
    api_key=api_key, secret=api_secret, chart_id=chart_id_eu, region=2
)  # region 2 is USA
r.json() # returns data as json
```

Get data from EU account with a proxy by setting region and proxy using a dictionary.

```python

# with proxy
proxies = {"http": "http://myproxy.example.org/method"}
r = amp.get_chart(api_key, api_secret, chart_id_eu, region=1, proxy=proxies)
r.status_code  # print status code
```

[Event segmentation](https://developers.amplitude.com/docs/dashboard-rest-api#event-segmentation) lets you export events with segments and filters.

```python
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
```

[User search](https://developers.amplitude.com/docs/dashboard-rest-api#user-search) lets you search for a user with a specific Amplitude ID, Device ID, User ID, or User ID prefix.

```python
user = amp.find_user(
    user=example_id_eu, 
    api_key=api_key, 
    secret=api_secret,
    region=1)
```

### Privacy API

Delete user data with a [deletion job](https://developers.amplitude.com/docs/user-deletion#deletion-job)

```python
deleteme = amp.delete_user_data(
    user["matches"][0]["amplitude_id"],
    email=email,
    api_key=api_key,
    secret=api_secret,
    region=1,
    ignore_invalid_id=True,
    delete_from_org=False,
)
```

[Get a list of deletion jobs](https://developers.amplitude.com/docs/user-deletion#get)

```python
tobe_deleted = amp.get_deletion_jobs(
    start="2022-06-01",
    end="2022-07-01",
    api_key=api_key,
    secret=api_secret,
    region=1,
)
```

### Cohort API

[Getting one cohort](https://developers.amplitude.com/docs/behavioral-cohorts-api#getting-one-cohort)

```python
proxies = {"http": "http://myproxy.domain.org/path"}
file_path = "path-to/cohortdata.csv"
kull = amp.get_cohort(
    api_key,
    api_secret,
    cohort_id,
    filename=file_path,
    props=1,
    region=1,
    proxy=proxies,
)
```

### Export API

[Export API - Export your project's event data](https://developers.amplitude.com/docs/export-api#export-api---export-your-projects-event-data)

```python
start = "20220601T00"
end = "20220601T01"
data = amp.export_project_data(
    start=start,
    end=end,
    api_key=api_key,
    secret=api_secret,
    filename="path-to/projectdata_eu.zip",
    region=1,
)
```

### Taxonomy API

[Get all event types](https://developers.amplitude.com/docs/taxonomy-api#get-all-event-types)

```python
types = amp.get_all_event_types(
    api_key=api_key, 
    secret=api_secret, 
    region=1)
```