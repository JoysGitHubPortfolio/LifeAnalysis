from itertools import islice
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def PlotMyMatrix(array, variables, plot, title, truncate):
    size = [len(variables)] * len(variables)
    input = iter(array)
    output = [list(islice(input, elem)) for elem in size]
    try:
        rounded_output = np.round(output, decimals = 2)
    except:
        rounded_output = output
    if truncate == True:
        rounded_output[np.triu_indices_from(rounded_output, 1)] = np.nan
    fig = px.imshow(rounded_output, text_auto = True, x = variables, y = variables,
                    title = title)
    fig.update_layout(title = {"x": 0.5})
    if plot == True:
        fig.show()
    return output, fig

def PlotMyDifference(m1, m2, variables, title, truncate, plot):
    diff = np.array(m1) - np.array(m2)
    diff_rounded = np.round(diff, decimals = 2)
    if truncate == True:
            diff_rounded[np.triu_indices_from(diff_rounded, 1)] = np.nan
    diff_fig = px.imshow(diff_rounded, text_auto = True, x = variables, y = variables, title = title)
    diff_fig.update_layout(title = {"x": 0.5})
    if plot == True:
        diff_fig.show()
    return diff_rounded

def BooleanTestMatrix(test_value, variables, test_matrix, output_matrix):
    boolean_matrix = []
    significant_matrix = []
    for i in range(0, len(variables)):
        for j in range(0, len(variables)):
            if i != j:
                if test_matrix[i][j] > test_value:
                    boolean_matrix.append(1)
                    significant_matrix.append(output_matrix[i][j])
                else:
                    boolean_matrix.append(0)
                    significant_matrix.append(0)
            else:
                boolean_matrix.append(0)
                significant_matrix.append(0)
    return boolean_matrix, significant_matrix

def ConcatMyMatrices(plots_array, titles):
    length = len(plots_array)
    dim = int(np.ceil(np.sqrt(length)))
    new_fig = make_subplots(rows=dim, cols=dim, subplot_titles=titles)
    for i, matrix in enumerate(plots_array):
        if matrix is not None:
            row = (i // dim) + 1
            col = (i % dim) + 1
            new_fig.add_trace(
                go.Heatmap(z=matrix.data[0].z,
                           x=matrix.data[0].x,
                           y=matrix.data[0].y),
                           row=row,
                           col=col
            )
    # Customize the title font for each subplot
    for i, title in enumerate(titles):
        row = i // (dim+1)
        col = i % (dim+1)
        new_fig.update_xaxes(title_text='', row=row, col=col)
        new_fig.update_yaxes(title_text='', row=row, col=col)
    new_fig.show()

    return new_fig
