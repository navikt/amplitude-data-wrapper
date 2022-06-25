# Amplitude data wrapper

This is a wrapper for [Amplitude](https://amplitude.com/) APIs. You can use it to query and export data from your account and use the taxonomy API.

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

### Dashboard Rest API

[Results from an existing chart](https://developers.amplitude.com/docs/dashboard-rest-api#results-from-an-existing-chart)

Get data from EU account

```python
from amplitude_data_wrapper import get_chart

r = get_chart(chart_id, api_key, api_secret, region=1)
r.status_code  # 200
r.text # print data
```

Get data from US account

```python
from amplitude_data_wrapper import get_chart

r = get_chart(chart_id, api_key, api_secret, region=2)
r.status_code  # 200
r.text # print data
```

Get data from EU account with a proxy

```python
from amplitude_data_wrapper import get_chart

proxies = {"http": "http://myproxy.domain.org/path"}
r = get_chart(chart_id, api_key, api_secret, region=1, proxy=proxies)
r.status_code  # 200
r.text # print data
```

[Event segmentation](https://developers.amplitude.com/docs/dashboard-rest-api#event-segmentation)



### Privacy API

Delete user data with a [deletion job](https://developers.amplitude.com/docs/user-deletion#deletion-job)

```python
deleteme = delete_user_data(
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
tobe_deleted = get_deletion_jobs(
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
kull = get_cohort(
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
data = export_project_data(
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
types = get_all_event_types(
    api_key=api_key, 
    secret=api_secret, 
    region=1)
```