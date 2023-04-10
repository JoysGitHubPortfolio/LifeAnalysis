import numpy as np
import pandas as pd
import datetime as dt
import os
import math

# Read the directory and get filenames; then read data for each filename
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\ExcelFiles"
for file in os.listdir(data_path):
    date = file.strip("WellLog_").strip(".xlsx")[:-7]
# df = pd.read_excel(data_path + "\\" + file, engine = "openpyxl")
df = pd.read_excel(r"C:\Users\joyco\OneDrive\Desktop\Dev\Py\Life Analysis\ExcelFiles\WellLog_2023_03_01  11_18.xlsx")

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
    column_names.append(dt.date(2023, 3, day))
df = df.set_axis([column_names], axis = 1, inplace = False)
df = df.drop(df.index[0:2])

# Fill in the NaN values for classes and swap empty values for 0
classes = []
for classType in df["Class"].iterrows():
    test = classType[1][0]
    if type(test) == str:
        newClass = test
    classes.append(newClass)
df["Class"] = classes
df = df.fillna(0)

# Convert string and Boolean into consistent numeric values
def TranslateValueType(colIndex):
    testCol = df.iloc[:, colIndex: colIndex + 1]
    newCol = []
    for row in testCol.iterrows():
        val = row[1][0]
        if (type(val) == str):
            if "mins" in val:
                val = float(val.strip("mins"))/60
            elif "hours" in val:
                val = float(val.strip("hours"))
        val = float(val)
        newCol.append(val)
    df.iloc[:, colIndex: colIndex + 1] = newCol

# Iterate through each date
for i in range(2, len(df.columns)):
    TranslateValueType(i)
df = df.transpose()
# Drop the empty rows
df = df.loc[(df!=0).any(axis=1)]

variables = df.loc["Variable"].values[0]
df.columns = variables
df = df.iloc[2:, :]
values = df.values
values = values.transpose()


print(df)
print(values)
print(len(values))

# PEARSON R NOT ALWAYS DEFINED IF BOOLEAN == TRUE FOR EVERY ELEM IN LIST
corrValues = []
for i in range(0, len(values)):
    for j in range(0, len(values)):
        r = np.corrcoef(list(values[i]), list(values[j]))[0,1]
        if math.isnan(r):
            r = 0
        # corrValues.append([i, j, r])
        corrValues.append(r)

from itertools import islice

length = [14, 14, 14, 14,
          14, 14, 14, 14,
          14, 14, 14, 14,
          14, 14]
input = iter(corrValues)
output = [list(islice(input, elem)) for elem in length]

for l in output:
    print(l)

import plotly.express as px

fig = px.imshow(output, text_auto = True, x = variables, y = variables)
fig.show()
