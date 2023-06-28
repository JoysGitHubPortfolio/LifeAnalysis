# Life in Data

## Introduction
I used a digital well-being mobile app. Tracked various lifestyle features to motivate me to improve my habits and used feature engineering through the Shannon-Entropy theory to chain habits for a more productive day. It was seen that 4 variables were redundant i.e. they are constant with respect to time. Hence they could be eliminated from the dataset. This allowed for dimensionality reduction.

## Productivity Analysis
### Gantt Chart for Lifestyle Habits
![screenshot](Images/HabitsGanttChart.png)

### Average 'Success-rate' Bar Chart (and sorted)
<table>
  <tr>
    <td>
      <img src="Images/BarMapped.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/BarMappedSorted.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

### Average 'Success-rate' Binned by Hours
<table>
  <tr>
    <td>
      <img src="Images/PlotCondSuccess.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotCondSuccessDiff.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

### Daily Productivity Bar Charts 
<table>
  <tr>
    <td>
      <img src="Images/RollingProductivity.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/ProductivitySorted.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

### Daily Productivity Frequency Density Plots
<table>
  <tr>
    <td>
      <img src="Images/ProductivityHistogram.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/ProductivityKDE.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

## Statistical Dependence Analysis
### Joint Probability Distributions
<table>
  <tr>
    <td>
      <img src="Images/PlotJointDist.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotJointTheoretic.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

### Cross-correlation Matrix
![screenshot](Images/PlotPearson.png)

### Dissimilarity Map between ML-maxed Cross-Correlation & Conditional Probability Distribution
<table>
  <tr>
    <td>
      <img src="Images/PlotCondProb.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotCondProbML.png" alt="Image 2" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotCondProbDissimilarity.png" alt="Image 3" style="width: 100%;">
    </td>
  </tr>
</table>


### Joint-Probability-based Variable Dependence
![screenshot](Images/PlotFeatureDep.png)

### Shannon-Entropy-based Feature Significance
![screenshot](Images/PlotMI.png)

