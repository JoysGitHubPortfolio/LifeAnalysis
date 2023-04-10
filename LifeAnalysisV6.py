import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
import os
import math
import warnings
from itertools import islice

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
pd.set_option('display.max_rows', None)


# Read the directory and get filenames; then read data for each filename
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\ExcelFiles"
filenamesList = []
for file in os.listdir(data_path):
    filename = data_path + "\\" + file
    filenamesList.append(filename)


def MakeMyDataFrame(fileLocation):
    print(fileLocation, "\n")
    df = pd.read_excel(fileLocation)

    date = fileLocation.strip(".xlsx")
    date = date[len(date) - 17: len(date) - 6]
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

    # Delete unnecessary row information
    variables = df.loc["Variable"].values[0]
    df.columns = variables
    df = df.iloc[2:, :]
    values = df.values
    values = values.transpose()

    # Drop the empty rows
    df = df.loc[(df!=0).any(axis=1)]
    return df

frames = []
for file in filenamesList:
    df = MakeMyDataFrame(file)
    frames.append(df)
result = pd.concat(frames)


def MakeMyBooleanDF(DataFrame, boolValues):
    columns = DataFrame.columns
    for col, val in zip(columns, boolValues):
        DataFrame.loc[DataFrame[col] >= val, col] = int(1)
        DataFrame.loc[DataFrame[col] != int(1), col] = 0
    return DataFrame

boolValues = [0.33, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1]
BooleanDF = MakeMyBooleanDF(result, boolValues)
print(BooleanDF)

def GetMyBooleanDates(BooleanDF, var):

    Dates = BooleanDF.index[BooleanDF[var] == 1].tolist()
    Dummy = []
    for i in range(0, len(Dates) - 1):
        diff = (Dates[i+1][0] - Dates[i][0]).days
        if diff != 1:
            Dummy.append([Dates[i][0], Dates[i+1][0]])

    first = Dates[0][0]
    last = Dates[len(Dates) - 1][0]
    Ranges = []
    for l1 in Dummy:
        for l2 in l1:
            Ranges.append(l2)
    Ranges.insert(0, first)
    Ranges.insert(len(Ranges) - 1, last)

    AllStart = []
    AllEnd = []
    for i in range(0, len(Ranges)):
        if i % 2 == 0:
            AllStart.append(Ranges[i])
        else:
            AllEnd.append(Ranges[i])

    VarDF = pd.DataFrame({'Start' : AllStart, 'End' : AllEnd})
    VarDF.insert(0, "Variable", var)

    # Bar graph cannot represent single date values so have to add 1
    VarDF["End"] = VarDF["End"] + pd.Timedelta(days = 1)
    return VarDF


variables = BooleanDF.columns
system = []
for var in variables:
    df = GetMyBooleanDates(BooleanDF, var)
    system.append(df)
df = pd.concat(system, axis = 0)

fig0 = px.timeline(df, x_start = "Start", x_end = "End", y = "Variable",
    color = df["Variable"],
    color_discrete_sequence = ["#922B21", "#E74C3C", "#F0B27A", "#FDEBD0",
                               "#F4D03F", "#F9E79F", "#ABEBC6", "#2ECC71",
                               "#A3E4D7", "#85C1E9", "#5499C7", "#8E44AD",
                               "#D2B4D3", "#979A9A"])
fig0.show()


# Can see that brush, night brush, Spanish and Hindi are redundant information so can reduce dimensions
BooleanDF = BooleanDF.drop(["Brush", "Night Brush", "Spanish", "Hindi"], axis = 1)
variables = BooleanDF.columns

Sums = []
for var in variables:
    sum = int(BooleanDF[var].sum())
    Sums.append([var, sum])
duration = len(BooleanDF)
for sum in Sums:
    print(sum[0], sum[1],  sum[1]/duration * 100, "% \n")

conditionalProbabilities = []
for var1 in variables:
    VarDF = BooleanDF.loc[BooleanDF[var1] == 1]
    for var2 in variables:
        p = VarDF[var2].sum()/len(VarDF)
        conditionalProbabilities.append(round(p, 2))
        print(var1, var2 , p)

# Make empty square matrix then fill with values of conditionalProbabilities
size = [len(BooleanDF.columns)] * len(BooleanDF.columns)
input = iter(conditionalProbabilities)
output = [list(islice(input, elem)) for elem in size]
fig1 = px.imshow(output, text_auto = True, x = variables, y = variables)
fig1.show()

# PEARSON R NOT ALWAYS DEFINED IF BOOLEAN == TRUE FOR EVERY ELEM IN LIST
values = BooleanDF.values
values = values.transpose()
corrValues = []
for i in range(0, len(values)):
    for j in range(0, len(values)):
        r = np.corrcoef(list(values[i]), list(values[j]))[0,1]
        if math.isnan(r):
            r = 0
        corrValues.append(round(r, 2))

input = iter(corrValues)
output = [list(islice(input, elem)) for elem in size]

fig2 = px.imshow(output, text_auto = True, x = variables, y = variables)
fig2.show()
