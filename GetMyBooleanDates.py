import pandas as pd

def GetMyBooleanDates(BooleanDF, var):
    # Find dates where streak ends and new one begins
    Dates = BooleanDF.index[BooleanDF[var] == 1].tolist()
    Dummy = []
    for i in range(0, len(Dates) - 1):
        diff = (Dates[i+1][0] - Dates[i][0]).days
        if diff != 1:
            Dummy.append([Dates[i][0], Dates[i+1][0]])

    # Add on the missing first date and last date which weren't in iteration
    first = Dates[0][0]
    last = Dates[len(Dates) - 1][0]
    Ranges = []
    for l1 in Dummy:
        for l2 in l1:
            Ranges.append(l2)
    Ranges.insert(0, first)
    Ranges.insert(len(Ranges) - 1, last)

    # Use Odd-Even alogrithm to split array into pairs i.e (start1, end1)
    AllStart = []
    AllEnd = []
    for i in range(0, len(Ranges)):
        if i % 2 == 0:
            AllStart.append(Ranges[i])
        else:
            AllEnd.append(Ranges[i])

    # Bar graph cannot represent single date values so have to add 1
    VarDF = pd.DataFrame({'Start' : AllStart, 'End' : AllEnd})
    VarDF.insert(0, "Variable", var)
    VarDF["End"] = VarDF["End"] + pd.Timedelta(days = 1)
    return VarDF
