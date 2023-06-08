import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from PlotMyMatrix import PlotMyMatrix
from MakeMyDataFrame import MakeMyBooleanDF

def SortedPlot(productivity_df):
    sorted_df = productivity_df.sort_values(by='Productivity', ascending=False).reset_index(drop=True)
    dates = sorted_df.index.tolist()
    avg_productivity = sorted_df['Productivity'].mean()
    plt.bar(dates, sorted_df['Productivity'])
    plt.axhline(y=avg_productivity, color='red', linestyle='--', label='Average')
    text_x = plt.xlim()[0] + (plt.xlim()[1] - plt.xlim()[0]) * 0.75
    text_y = plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) * 0.40
    plt.text(text_x, text_y, f'Average: {avg_productivity:.2f}', color='red', va='top', ha='left')
    plt.xlabel('Date (index)')
    plt.ylabel('Productivity (h)')
    plt.title('Productivity Distribution sorted Descending')
    plt.show()
    return sorted_df

def AnalysisKDE(productivity_df):
    # Plot histogram of 'Productivity' values
    plt.hist(productivity_df['Productivity'], bins=9)
    plt.xlabel('Productivity (h)')
    plt.ylabel('Frequency (number of days)')
    plt.title('Productivity Histogram showing Trimodal Distribution')
    plt.axvline(x=0, color='red', linestyle='--', label='Low')
    plt.axvline(x=3, color='orange', linestyle='--', label='Medium')
    plt.axvline(x=6, color='green', linestyle='--', label='High')
    plt.text(0, plt.ylim()[1] * 0.9, 'Low', color='red', va='top', ha='right')
    plt.text(3, plt.ylim()[1] * 0.9, 'Medium', color='orange', va='top', ha='right')
    plt.text(6, plt.ylim()[1] * 0.9, 'High', color='green', va='top', ha='right')
    plt.show()

    # Get the density values from the KDE plot
    sns.histplot(data=productivity_df['Productivity'], kde=True, color='skyblue')
    plt.xlabel('Productivity')
    plt.ylabel('Density')
    plt.title('Continuous Productivity Histogram showing Bimodal Distribution')

    kde_density = sns.histplot(data=productivity_df['Productivity'], kde=True).get_lines()[0].get_data()
    peaks, _ = find_peaks(kde_density[1])
    peak_positions = kde_density[0][peaks]
    for peak in peak_positions:
        plt.axvline(x=peak, color='red', linestyle='--', label='Peak')
        plt.text(peak, 0, str(round(peak, 2)), color='red', va='top', ha='center')
    plt.legend()
    plt.show()
    return kde_density

def RollingProductivity(productivity_df, num_days, col):
    # Plot productivity over time
    dates = productivity_df.index.values
    productivity_daily = productivity_df['Productivity']
    sma = productivity_daily.rolling(window=num_days).mean()
    plt.bar(dates, productivity_df['Productivity'], color = 'gray')
    fig = plt.plot(dates, sma, color=col, label=f'SMA {num_days}')
    plt.xlabel('Date (index)')
    plt.ylabel('Productivity (h)')
    plt.title('Productivity over Time with SMA = 7 (red), 14 (orange), 28 (green)')
    return sma

def ConditionalProductivity(result, bool_values, productivity_daily, plot_title):
    # Float df
    new_df = result.copy(deep = True)
    new_df["Productivity"] = productivity_daily
    new_df = new_df.drop(["Brush", "Night Brush", "Spanish", "Hindi"], axis = 1)
    print(new_df)

    # Booolean df
    boolean_df = result.copy(deep = True)
    boolean_df = MakeMyBooleanDF(boolean_df, bool_values)
    boolean_df = boolean_df.drop(["Brush", "Night Brush", "Spanish", "Hindi"], axis = 1)
    boolean_df["Productivity"] = productivity_daily
    print(boolean_df)

    def PlotConditionExpectation(boolean_df):
        # Remove last element i.e. "Productivity" as this is the output for which we are iterating
        variables = list(boolean_df.columns.values)
        vars_prod = variables[:-1]
        cond_prods = []
        for var1 in vars_prod:
            for var2 in vars_prod:
                cond_prod = boolean_df.loc[(boolean_df[var1] == 1) & (boolean_df[var2] == 1), "Productivity"]
                mean = cond_prod.values.mean()
                cond_prods.append(mean)
                print(var1, var2, mean)
        cond_prod_title = "Conditional Expectation for Productivity (h) with respect to Pairwise-Combinations of Variables:<br>"
        cond_prod_title = cond_prod_title + plot_title
        cond_prod_output, cond_prod_fig = PlotMyMatrix(cond_prods, vars_prod, plot = True, title = cond_prod_title, truncate = True)
        return cond_prod_output

    # Plot producitivty matrix for all parameters
    cond_prod_values = PlotConditionExpectation(boolean_df)

    # Float elements contribute to producitivity hours which leads to bias. Account for this:
    accounted_df = boolean_df.copy(deep = True)
    accounted_df = accounted_df.drop(["Journal", "Piano", "Reading", "Deep Work"], axis = 1)
    cond_prod_nonvalues = PlotConditionExpectation(accounted_df)
    return new_df

def ProductivityAnalysis(result, bool_values, plot_title):
    # Create values dataframe
    productivity_df = result.copy(deep = True)
    productivity_df = productivity_df[["Journal", "Piano", "Reading", "Deep Work"]]
    productivity_daily = productivity_df.sum(axis = 1)
    productivity_df["Productivity"] = productivity_daily
    productivity_df = productivity_df.reset_index(drop=True)

    # Get rolling average for productivity across various time dataframes
    sma_7 = RollingProductivity(productivity_df, 7, 'red')
    sma_14 = RollingProductivity(productivity_df, 14, 'orange')
    sma_28 = RollingProductivity(productivity_df, 28, 'green')
    plt.show()

    # Analyse density and frequency of productivity distribution
    sorted_df = SortedPlot(productivity_df)
    kde_density = AnalysisKDE(productivity_df)

    # Get the conditional expectation matrix for completion of 2 habits
    new_df = ConditionalProductivity(result, bool_values, productivity_daily, plot_title)
    return productivity_df
