import pandas as pd

def MakeMyBooleanDF(DataFrame, boolValues):
    columns = DataFrame.columns
    for col, val in zip(columns, boolValues):
        DataFrame.loc[DataFrame[col] >= val, col] = int(1)
        DataFrame.loc[DataFrame[col] != int(1), col] = 0
    return DataFrame
