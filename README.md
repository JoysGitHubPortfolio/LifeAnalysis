# Life in Data

## Introduction
I used a digital well-being mobile app. Tracked various lifestyle features to motivate me to improve my habits and used feature engineering through the Shannon-Entropy theory to chain habits for a more productive day. It was seen that 4 variables were redundant i.e. they are constant with respect to time. Hence they could be eliminated from the dataset. This allowed for dimensionality reduction.


## Method
### Gantt Chart for Lifestyle Habits
![screenshot](Images/GanttChart.png)


## Results
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

### Conditional Expectation Distributions
<table>
  <tr>
    <td>
      <img src="Images/PlotCondExp.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotCondExpReduced.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

### Mutually Exclusive Truth Tests
<table>
  <tr>
    <td>
      <img src="Images/TruthFreq.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/TruthExp.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>


## Productivity Analysis
### Daily Productivity Bar Charts 
<table>
  <tr>
    <td>
      <img src="Images/ProductivityAll.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/ProductivityAllSorted.png" alt="Image 2" style="width: 100%;">
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
### Cross-correlation Matrix
![screenshot](Images/PlotPearson.png)

### Shannon-Entropy Dissimilarity Map for Joint Probability Distribution
<table>
  <tr>
    <td>
      <img src="Images/PlotJointDist.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotJointTheoretic.png" alt="Image 2" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotJointDissimilarity.png" alt="Image 3" style="width: 100%;">
    </td>
  </tr>
</table>

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


## Feature Significance Analysis
### Conditional Entropy & Information Flow
<table>
  <tr>
    <td>
      <img src="Images/PlotEntropyConditional.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/PlotEntropyAsymmetry.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

### Mutual Information Matrix
![screenshot](Images/PlotMI.png)


## Causal-Delta Predictions
### Thresholding ML-maximised Cross-correlation > 0.7
<table>
  <tr>
    <td>
      <img src="Images/BooleanML.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/BooleanMLDelta.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>

### Thresholding Dissimilarity > 0.2
<table>
  <tr>
    <td>
      <img src="Images/BooleanDiss.png" alt="Image 1" style="width: 100%;">
    </td>
    <td>
      <img src="Images/BooleanDissDelta.png" alt="Image 2" style="width: 100%;">
    </td>
  </tr>
</table>


