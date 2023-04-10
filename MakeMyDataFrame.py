import pandas as pd
import datetime as dt


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
