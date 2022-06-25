# Amplitude analytics

This is a wrapper for Amplitude APIs. You can use it to query and export data from your account and use the taxonomy API.

**Why use this package instead of other wrappers?**

This package supports regions and so you can use it with Amplitude accounts in the EU and USA.

This package also supports using a proxy so you can keep your project API keys and API secrets confidential.

**Get existing chart**

```python
from amplitude_data_wrapper import get_chart

proxies = {"http": "http://myproxy.domain.org/path"}
r = get_chart(chart_id, api_key, api_secret, region=1, proxy=proxies)
r.status_code  # 200
r.text # print data
```

**Get a cohort**

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

**Export project data**

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