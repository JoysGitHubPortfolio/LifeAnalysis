from ImportFile import *

def LifeAnalysis(result, do_plot):
    # Set the title of following plots as given date range
    start_date, end_date = GetDateRange(result)
    plot_title = start_date.strftime('%Y-%m-%d') + ' to ' + end_date.strftime('%Y-%m-%d')
    print(plot_title)

    # Set the threshold values for achieving a target activity
    bool_values = [0.33, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1]
    ProductivityAnalysis(result, bool_values, plot_title)

    # Set boolean_df for Gantt Chart
    boolean_df = MakeMyBooleanDF(result, bool_values)
    print(boolean_df)

    # Plot a Gantt chart with dates where a streak is true
    variables = boolean_df.columns
    system = []
    for var in variables:
        df = GetMyBooleanDates(boolean_df, var)
        system.append(df)
    dates_df = pd.concat(system, axis = 0)

    # Define the colour scheme for the Gantt chart
    fig0 = px.timeline(dates_df, x_start = "Start", x_end = "End", y = "Variable",
        color = dates_df["Variable"],
        color_discrete_sequence = ["#922B21", "#E74C3C", "#F0B27A", "#FDEBD0",
                                   "#F4D03F", "#F9E79F", "#ABEBC6", "#2ECC71",
                                   "#A3E4D7", "#85C1E9", "#5499C7", "#8E44AD",
                                   "#D2B4D3", "#979A9A"],
        title = str("Habits Gantt Chart:<br>" + plot_title))
    fig0.update_layout(title = {"x": 0.5})
    fig0.show()

    # Can see these 4 variables are redundant information so can reduce dimensions
    boolean_df = boolean_df.drop(["Brush", "Night Brush", "Spanish", "Hindi"], axis = 1)
    float_df = result.drop(["Brush", "Night Brush", "Spanish", "Hindi"], axis = 1)
    variables = boolean_df.columns

    # Get the average success rate for each variable
    average_probabilities = []
    days = len(boolean_df)
    for var in variables:
        total = boolean_df[var].sum()
        p = total/days
        average_probabilities.append(p)
        print(var, total, p)

    # Create R^2 Matrix for pairwise combinations. NOTE: undefined if all x in X == 1 or 0
    values = float_df.values.transpose()
    corr_values = []
    for i in range(0, len(values)):
        for j in range(0, len(values)):
            r = np.corrcoef(list(values[i]), list(values[j]))[0,1]
            if math.isnan(r):
                r = 0
            corr_values.append(r)
    corr_title = str("Pearson-Correlation Matrix:<br>" + plot_title)
    corr_output, fig1 = PlotMyMatrix(corr_values, variables, plot = do_plot, title = corr_title, truncate = True)

    # Create Matrix for causality analysis that finds the delta that maximises cross-correation
    deltas = []
    cross_corrs = []
    for var1 in variables:
        for var2 in variables:
            delta = PredictDelta(dates_df, boolean_df, var1, var2, plot=False, verbose=False)[0]
            cross = PredictDelta(dates_df, boolean_df, var1, var2, plot=False, verbose=False)[1]
            deltas.append(delta)
            cross_corrs.append(cross)
            print(var1, var2, delta)
    cross_corr_title = str("ML Maximised Cross-Correlation Matrix:<br>" + plot_title)
    delta_title = str("Delta Matrix:<br>" + plot_title)
    cross_corr_matrix, fig2 = PlotMyMatrix(cross_corrs, variables, plot = do_plot, title = cross_corr_title, truncate = False)
    delta_matrix, fig3 = PlotMyMatrix(deltas, variables, plot = False, title = delta_title, truncate = False)

    # Create Matrices to do causality analysis for values of delta that produced significant cross-correlation
    test_value = 0.7
    boolean_cross_correlation, sig_delta_matrix = BooleanTestMatrix(test_value, variables, cross_corr_matrix, delta_matrix)
    sig_delta_title = str("Initial Predicted-Delta Matrix:<br>" + plot_title)
    bool_delta_title = str("Initial Boolean-Delta Matrix:<br>" + plot_title)
    boolean_ouput, fig4 = PlotMyMatrix(boolean_cross_correlation, variables, plot = do_plot, title = bool_delta_title, truncate = False)
    delta_output, fig5 = PlotMyMatrix(sig_delta_matrix, variables, plot = do_plot, title = sig_delta_title, truncate = False)

    # Create Conditional Probability Matrix for all pairwise combination of variables
    cond_probabilities = []
    for var1 in variables:
        variable_df = boolean_df.loc[boolean_df[var1] == 1]
        for var2 in variables:
            p = variable_df[var2].sum()/len(variable_df)
            cond_probabilities.append(p)
            print(var1, var2 , round(p, 2))
    cond_title = str("Conditional-Probability Distribution:<br>" + plot_title)
    cond_matrix, fig6 = PlotMyMatrix(cond_probabilities, variables, plot = do_plot, title = cond_title, truncate = False)
    print(cond_matrix)

    # Create Join Probability Matrix
    joint_probabilities = []
    cond_entropy_matrix = []
    rowwise_entropies = []
    for i in range(0, len(average_probabilities)):
        sum = 0
        row = []
        for j in range(0, len(cond_matrix[i])):
            joint_p = cond_matrix[i][j] * average_probabilities[i]
            joint_probabilities.append(joint_p)
            sum += ElementShannonEntropy(joint_p)
            cond_entropy = ElementShannonEntropy(cond_matrix[i][j])
            row.append(cond_entropy)
        cond_entropy_matrix.append(row)
        rowwise_entropies.append(sum)
        print("Entropy", sum)
    joint_title = str("Joint-Probability Distribution:<br>" + plot_title)
    joint_ouput, fig7 = PlotMyMatrix(joint_probabilities, variables, plot = do_plot, title = joint_title, truncate = True)

    # Get the Conditional Entropy matrix in a similar fashion
    element_cond_entropies = []
    for i in range(0, len(average_probabilities)):
        for j in range(0, len(cond_matrix[i])):
            element_cond_entropy = ElementMutualInformation(average_probabilities[i], cond_matrix[i][j])
            element_cond_entropies.append(element_cond_entropy)
            print(element_cond_entropy)
    cond_entropy_title = str("Conditional-Entropy Matrix:<br>" + plot_title)
    entropy_ouput, fig8 = PlotMyMatrix(element_cond_entropies, variables, plot = do_plot, title = cond_entropy_title, truncate = False)

    # Get the Mutual Information matrix in a similar fashion
    mi_list = []
    for i in range(0, len(rowwise_entropies)):
        for j in range(0, len(cond_entropy_matrix[i])):
            mutual_information = rowwise_entropies[i] - cond_entropy_matrix[i][j]
            mi_list.append(mutual_information)
            print(mutual_information)
    mi_title = str("Mutial-Information Matrix:<br>" + plot_title)
    mi_output, fig9 = PlotMyMatrix(mi_list, variables, plot = do_plot, title = mi_title, truncate = False)

    # Plot how well the ML algorithm performed by looking at the information gain/uncertainty reduction from original metrics
    diff_title = str("Probability Gain between ML-maximised Cross-Correlation & Conditional Probability Distribution:<br>" + plot_title)
    diff = PlotMyDifference(cross_corr_matrix, cond_matrix, variables, diff_title, truncate = False, plot = True)

    cross_corr_entropy = [[ElementShannonEntropy(x) for x in row] for row in cross_corr_matrix]
    cond_prob_entropy = [[ElementShannonEntropy(x) for x in row] for row in cond_matrix]
    diff_entropy_title = str("Uncertainty Gain between ML-maxised Cross-Correlation & Conditional Probability Distribution:<br>" + plot_title)
    diff_entropy = PlotMyDifference(cross_corr_entropy, cond_prob_entropy, variables, diff_entropy_title, truncate = False, plot = True)

    # Get new predictions for Delta by seeing which pairwise variable saw an increase in probability difference of the test-value
    test_value = 0.2
    boolean_cross_correlation, sig_delta_matrix = BooleanTestMatrix(test_value, variables, diff, delta_matrix)
    sig_delta_title = str("Predicted-Delta Matrix based on Probability Gain:<br>" + plot_title)
    bool_delta_title = str("Boolean-Delta Matrix based on Probability Gain:<br>" + plot_title)
    boolean_ouput, fig_10 = PlotMyMatrix(boolean_cross_correlation, variables, plot = do_plot, title = bool_delta_title, truncate = False)
    delta_output, fig_11 = PlotMyMatrix(sig_delta_matrix, variables, plot = do_plot, title = sig_delta_title, truncate = False)

    # Understand which of the variables show a higher degree of dependence & pair with mutual information to infer causality
    independent_probabilities = []
    for i, p1 in enumerate(average_probabilities):
        for j, p2 in enumerate(average_probabilities):
            if i != j:
                p = p1 * p2
            else:
                p = p1
            independent_probabilities.append(p)
    independent_probabilities = np.array(independent_probabilities)

    # Distribution calculated by iterating through P(X) * P(Y)
    independent_title = str("Theoretical Independent Joint Distribution:<br>" + plot_title)
    independent_matrix, independent_matrix_fig = PlotMyMatrix(independent_probabilities, variables, plot = True, title = independent_title, truncate = True)

    # Subtract action from theoretical distribution and non-0 values indicate some level of "interference" i.e. may indicate causality
    dependence_bias_title = str("Dependence Bias: The Entropy Difference Between Actual Joint Distribution & Distribution for P(X)*P(Y):<br>" + plot_title)
    dependence_bias = PlotMyDifference(joint_ouput, independent_matrix, variables, dependence_bias_title, truncate = True, plot = True)

    # create a subplot to display all plots
    plots_array = [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig_10, fig_11]
    plots_titles = [corr_title,
                    cross_corr_title,
                    delta_title,
                    bool_delta_title,
                    sig_delta_title,
                    cond_title,
                    joint_title,
                    cond_entropy_title,
                    mi_title,
                    bool_delta_title,
                    sig_delta_title]
    ConcatMyMatrices(plots_array, plots_titles)
    return boolean_df

def TruncatedLifeAnalysis(result, dates, plot):
    first, second = dates[0], dates[1]
    start, end = dt.date(first[0], first[1], first[2]), dt.date(second[0], second[1], second[2]),
    dummy = result.copy(deep = True)
    dummy = dummy.truncate(before=start, after=end, axis="rows")
    truncated_df = LifeAnalysis(dummy, plot)
    return truncated_df
