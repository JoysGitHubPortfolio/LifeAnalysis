# Convert string and Boolean into consistent numeric values
def TranslateValueType(df, col_index):
    test_col = df.iloc[:, col_index: col_index + 1]
    new_col = []
    for row in test_col.iterrows():
        val = row[1][0]
        if (type(val) == str):
            if "mins" in val:
                val = float(val.strip("mins"))/60
            elif "hours" in val:
                val = float(val.strip("hours"))
        val = float(val)
        new_col.append(val)
    df.iloc[:, col_index: col_index + 1] = new_col
