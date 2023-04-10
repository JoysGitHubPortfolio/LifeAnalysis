import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
import os
import math
import warnings
from itertools import islice
from MakeMyDataFrame import MakeMyDataFrame
from MakeMyBooleanDF import MakeMyBooleanDF
from GetMyBooleanDates import GetMyBooleanDates

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
pd.set_option('display.max_rows', None)

# Read the directory and get filenames; then read data for each filename
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\ExcelFiles"
filenamesList = []
for file in os.listdir(data_path):
    filename = data_path + "\\" + file
    filenamesList.append(filename)

# Concatenate dataframes using files from different months
frames = []
for file in filenamesList:
    df = MakeMyDataFrame(file)
    frames.append(df)
result = pd.concat(frames)

# Set the threshold values for achieving a target activity
boolValues = [0.33, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1]
BooleanDF = MakeMyBooleanDF(result, boolValues)
print(BooleanDF)

# Plot a Gantt chart with dates where a streak is true
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


# Can see these 4 variables are redundant information so can reduce dimensions
BooleanDF = BooleanDF.drop(["Brush", "Night Brush", "Spanish", "Hindi"], axis = 1)
FloatDF = result.drop(["Brush", "Night Brush", "Spanish", "Hindi"], axis = 1)
variables = BooleanDF.columns

# Get the average achievement rate for all given variables
Sums = []
for var in variables:
    sum = int(BooleanDF[var].sum())
    Sums.append([var, sum])
duration = len(BooleanDF)
for sum in Sums:
    print(sum[0], sum[1],  sum[1]/duration * 100, "% \n")

# Create Conditional Probability Matrix for all pairwise combination of variables
conditionalProbabilities = []
for var1 in variables:
    VarDF = BooleanDF.loc[BooleanDF[var1] == 1]
    for var2 in variables:
        p = VarDF[var2].sum()/len(VarDF)
        conditionalProbabilities.append(round(p, 2))
        print(var1, var2 , p)
# Make empty square matrix then fill with values of conditional probabilities
size = [len(BooleanDF.columns)] * len(BooleanDF.columns)
input = iter(conditionalProbabilities)
output = [list(islice(input, elem)) for elem in size]
fig1 = px.imshow(output, text_auto = True, x = variables, y = variables)
fig1.show()

# Create Pearson Correlation Matrix for all pairwise combinations of variables
values = FloatDF.values.transpose()
corrValues = []
for i in range(0, len(values)):
    for j in range(0, len(values)):
        r = np.corrcoef(list(values[i]), list(values[j]))[0,1]
        # PEARSON R NOT ALWAYS DEFINED IF BOOLEAN == TRUE FOR EVERY ELEM IN LIST
        if math.isnan(r):
            r = 0
        corrValues.append(round(r, 2))
input = iter(corrValues)
output = [list(islice(input, elem)) for elem in size]
fig2 = px.imshow(output, text_auto = True, x = variables, y = variables)
fig2.show()
