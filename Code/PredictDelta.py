import numpy as np
import pandas as pd
import plotly.express as px
from JoysCustomML import *

def PredictDelta(dates_df, boolean_df, var1, var2, plot, verbose):
    # Statistical learning approach my minimising sum square error
    if var1 != var2:
        print("\nSSE")
        x1, x2 = boolean_df[var1].values, boolean_df[var2].values
        stats = SlidingWindow(x1,x2)
        stats = {k:v for k,v in sorted(stats.items(), key = lambda item: item[1])}
        deltas_sse = {}
        count = 0
        for i in stats:
            stats[i] = np.sqrt(stats[i])
            if abs(i) < 14 and count < 10:
                deltas_sse[i] = stats[i]
                count += 1
        for i in deltas_sse:
            print(i, deltas_sse[i])

        # Statistical learning approach by maximising dot-product i.e. cross-correlation
        print("\nCross-correlation")
        stats = MaximiseCrossCorr(x1,x2)
        stats = {k:v for k,v in sorted(stats.items(), key = lambda item: item[1], reverse = True)}
        deltas_r = {}
        count = 0
        for i in stats:
            # Get the top 10 values within a 2-week range
            if abs(i) < 14 and count < 10:
                deltas_r[i] = stats[i]
                count += 1
        for i in deltas_r:
            print(i, deltas_r[i])

        # NEED ANOTHER WAY TO DEFINE OBJECTIVE FUNCTION IF NO INTERSECTION
        key1 = deltas_sse.keys()
        key2 = deltas_r.keys()
        intersection = []
        for k in key1:
            if k in key2:
                intersection.append(k)
        print("\nIntersection", intersection)

        # Create an objective function proportional to correlation and inversely proportional to error
        delta_prediction = {}
        for k in intersection:
            err = deltas_sse[k]
            corr = deltas_r[k]
            objective = (1/err) * corr
            delta_prediction[k] = objective
        delta_prediction = {k:v for k,v in sorted(delta_prediction.items(), key = lambda item: item[1])}
        try:
            delta = list(delta_prediction.keys())[-1]
        except:
            delta = 0

        # Now find the Pearson correlation for the predicted delta
        if delta < 0:
            x1_predicted = x1[-delta :]
        else:
            x1_predicted = x1[delta :]
        x2_predicted = x2[0: len(x1_predicted)]
        r = np.corrcoef(list(x1_predicted), list(x2_predicted))[0][1]
        max_sum = sum(x1)
        actual_sum = DotProd(list(x1_predicted), (x2_predicted))
        cross_correlation = actual_sum/max_sum
        print("Cross-correlation: ", cross_correlation)
        if verbose == True:
            print(delta_prediction)
            print(delta)
            print(x1_predicted, x2_predicted)
            print(len(x1_predicted), len(x2_predicted))

        # Find the variables and shif the dateset for one of them by the predicted delta
        theoretical_dict = {}
        theoretical_dict[var1] = dates_df.loc[dates_df["Variable"] == var1]
        theoretical_dict[var2] = dates_df.loc[dates_df["Variable"] == var2]
        pd.options.mode.chained_assignment = None
        theoretical_dict[var1]["Start"] = theoretical_dict[var1]["Start"] + pd.Timedelta(days = delta)
        theoretical_dict[var1]["End"] = theoretical_dict[var1]["End"] + pd.Timedelta(days = delta)
        pd.options.mode.chained_assignment = "warn"

        # Plotting the comparison Gantt chart
        df_compare = pd.concat([theoretical_dict[var1], theoretical_dict[var2]], axis = 0)
        if plot == True:
            print(df_compare)
            fig_compare = px.timeline(df_compare, x_start = "Start", x_end = "End", y = "Variable",
                color = df_compare["Variable"],
                color_discrete_sequence = ["#922B21", "#E74C3C"])
            fig_compare.show()
    else:
        delta = 0
        r = 1
        cross_correlation = 1
        
    print("Pearson Correlation: ", r)
    return [delta, cross_correlation]
