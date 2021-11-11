# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
#
# + [DateTime in Pandas](#DateTime-in-Pandas) 
# + [Create DatetimeIndex](#Create-DatetimeIndex) 
# + [Convert from other types](#Convert-from-other-types) 
# + [Indexing with DatetimeIndex](#Indexing-with-DatetimeIndex) 
# + [Date/time components in the DatetimeIndex](#Date/time-components-in-the-DatetimeIndex) 
# + [Operations on Datetime](#Operations-on-Datetime) 

# ## DateTime in Pandas
#
# *Qi, Bingnan*
# bingnanq@umich.edu
#
# - Pandas contains a collection of functions and features to deal with time series data. A most commonly used class is `DatetimeIndex`.
#

# ## Create DatetimeIndex
#
# - A `DatetimeIndex` array can be created using `pd.date_range()` function. The `start` and `end` parameter can control the start and end of the range and `freq` can be `D` (day), `M` (month), `H` (hour) and other common frequencies.

pd.date_range(start='2020-01-01', end='2020-01-05', freq='D')

pd.date_range(start='2020-01-01', end='2021-01-01', freq='2M')

# ## Convert from other types
#
# - Other list-like objects like strings can also be easily converted to a pandas `DatetimeIndex` using `to_datetime` function. This function can infer the format of the string and convert automatically.

pd.to_datetime(["2020-01-01", "2020-01-03", "2020-01-05"])

# - A `format` keyword argument can be passed to ensure specific parsing.

pd.to_datetime(["2020/01/01", "2020/01/03", "2020/01/05"], format="%Y/%m/%d")

# ## Indexing with DatetimeIndex
#
# - One of the main advantage of using the `DatetimeIndex` is to make index a time series a lot easier. For example, we can use common date string to directly index a part of the time series.

# +
idx = pd.date_range('2000-01-01', '2021-12-31', freq="M")
ts = pd.Series(np.random.randn(len(idx)), index=idx)

ts['2018-09':'2019-04']
# -

ts['2021-6':]

# ## Date/time components in the DatetimeIndex
#
# - The properties of a date, e.g. `year`, `month`, `day_of_week`, `is_month_end` can be easily obtained from the `DatetimeIndex`.

idx.isocalendar()

# ## Operations on Datetime
#
# - We can shift a DatetimeIndex by adding or substracting a `DateOffset`

idx[:5] + pd.offsets.Day(2)

idx[:5] + pd.offsets.Minute(1)
