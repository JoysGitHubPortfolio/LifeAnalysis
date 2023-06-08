import pandas as pd
import numpy as np
import datetime as dt

def GetMyBooleanDates(boolean_df, var):
    # Find dates where streak ends and new one begins
    dates = boolean_df.index[boolean_df[var] == 1].tolist()
    dummy = []
    for i in range(0, len(dates) - 1):
        diff = (dates[i+1][0] - dates[i][0]).days
        if diff != 1:
            dummy.append([dates[i][0], dates[i+1][0]])

    # Add on the missing first date and last date which weren't in iteration
    first = dates[0][0]
    last = dates[len(dates) - 1][0]
    ranges = []
    for l1 in dummy:
        for l2 in l1:
            ranges.append(l2)
    ranges.insert(0, first)
    ranges.insert(len(ranges) - 1, last)

    # Use Odd-Even alogrithm to split array into pairs i.e (start1, end1)
    all_start = []
    all_end = []
    for i in range(0, len(ranges)):
        if i % 2 == 0:
            all_start.append(ranges[i])
        else:
            all_end.append(ranges[i])

    # Bar graph cannot represent single date values so have to add 1
    var_df = pd.DataFrame({'Start' : all_start, 'End' : all_end})
    var_df.insert(0, "Variable", var)
    var_df["End"] = var_df["End"] + pd.Timedelta(days = 1)
    return var_df

# Flatten the multi-index for df & get dates for overall analysis
def GetDateRange(result):
    dummy = result.copy(deep=True)
    dummy.index = pd.to_datetime(dummy.index.get_level_values(0))
    start_date = dummy.index.min().date()
    end_date = dummy.index.max().date()
    print(start_date, end_date)
    return start_date, end_date

def GetMonthlyRanges(result):
    # Group the analysis by month
    dummy = result.copy(deep = True)
    dummy.index = pd.to_datetime(dummy.index.get_level_values(0))

    df_monthly = pd.DataFrame(index=dummy.index)
    df_monthly['month_start'] = dummy.index
    df_monthly['month_end'] = dummy.index + pd.offsets.MonthEnd(1)
    df_ends = [elem.date() for elem in df_monthly['month_end']]

    df_ends = np.unique(df_ends)

    monthly_ranges = []
    for end in df_ends:
        year, month, day = end.year, end.month, end.day
        start = dt.date(year, month, 1)
        range = [start, end]
        monthly_ranges.append(range)
        print(range)
    return monthly_ranges
