import re
import pandas as pd
import datetime as dt
from TranslateValueType import TranslateValueType

def MakeMyDataFrame(file_location):
    print(file_location)
    df = pd.read_excel(file_location)
    match = re.search(r"\d{4}_\d{2}_\d{2}", file_location)
    date = match.group()
    year, month = date[0:4], date[5:7]
    if month[0] == "0":
        month = month[-1]
    year, month = int(year), int(month)
    days = []
    for key in df.keys():
        if "Unnamed" in key:
            key = int(key.strip("Unnamed: ")) - 1
        if key == "WELL LOG":
            key = 14
        if key >= 1:
            days.append(key)

    # Reformat the dateframe so has datetime format
    column_names = ["Class", "Variable"]
    for day in days:
        column_names.append(dt.date(year, month, day))
    df = df.set_axis([column_names], axis = 1, inplace = False)
    df = df.drop(df.index[0:2])

    # Fill in the NaN values for classes and swap empty values for 0
    classes = []
    for class_type in df["Class"].iterrows():
        test = class_type[1][0]
        if type(test) == str:
            new_class = test
        classes.append(new_class)
    df["Class"] = classes
    df = df.fillna(0)

    # Iterate through dates of 'df' & convert "mins"/"hours" to standard format
    for i in range(2, len(df.columns)):
        TranslateValueType(df, i)
    df = df.transpose()
    # Delete unnecessary row information
    variables = df.loc["Variable"].values[0]
    df.columns = variables
    df = df.iloc[2:, :]
    values = df.values
    values = values.transpose()
    # Drop the empty rows
    df = df.loc[(df!=0).any(axis=1)]
    return df

# Strictly convert all floats to BOOLEAN
def MakeMyBooleanDF(df, bool_values):
    columns = df.columns
    for col, val in zip(columns, bool_values):
        df.loc[df[col] >= val, col] = int(1)
        df.loc[df[col] == 1.0, col] = int(1)
        df.loc[df[col] != int(1), col] = 0
    return df
