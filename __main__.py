from LifeAnalysis import *

# Read the directory and get filenames; then read data for each filename
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path.replace("\Code", "")
data_path = dir_path + "\ExcelFiles"
filenames_list = []
for file in os.listdir(data_path):
    filename = data_path + "\\" + file
    filenames_list.append(filename)

# Concatenate dataframes from different months
frames = []
for file in filenames_list:
    df = MakeMyDataFrame(file)
    frames.append(df)
result = pd.concat(frames)

# Do overall analysis
df_overall = LifeAnalysis(result, True)
df_friends = TruncatedLifeAnalysis(result, [[2022,10,22],[2023,5,31]], plot = False)

# Perform analysis on significant dates
quarterly = False
if quarterly == True:
    df_22_q4 = TruncatedLifeAnalysis(result, [[2022,10,1],[2022,12,31]], plot = False)
    df_23_q1 = TruncatedLifeAnalysis(result, [[2023,1,1],[2023,3,31]], plot = False)

# Perform monthly analysis
monthly = False
if monthly == True:
    monthly_ranges = GetMonthlyRanges(result)
    dummy = result.copy(deep = True)
    for range in monthly_ranges:
        start, end = range[0], range[1]
        try:
            month_df = dummy.loc[start : end]
            LifeAnalysis(month_df, False)
        except:
            print("Unable to process: ", [start, end])
