# Life Analysis
I used a digital well-being mobile app. Tracked various lifestyle features to motivate me to improve my habits and used feature engineering through the Shannon-Entropy theory to chain habits for a more productive day. It was seen that 4 variables were redundant i.e. they are constant with respect to time. Hence they could be eliminated from the dataset. This allowed for dimensionality reduction.

## Gantt Chart for Lifestyle Habits
![screenshot](Images/HabitsGanttChart.png)

## Productivity over Time
![screenshot](Images/RollingProductivity.png)

## Productivity Distribution Sorted
![screenshot](Images/ProductivitySorted.png)

## Productivity Frequency Distribution
![screenshot](Images/ProductivityKDE.png)

## Cross-correlation Matrix
![screenshot](Images/PlotPearson.png)

## Conditional Probability Disitribution
![screenshot](Images/PlotCondProb.png)

## ML-maximised Distribution
![screenshot](Images/PlotMLMax.png)

## Joint-Probability-based Variable Dependence
![screenshot](Images/PlotFeatureDep.png)

## Shannon-Entropy-based Feature Significance
![screenshot](Images/PlotMI.png)

$$ {\displaystyle {\begin{aligned}\operatorname {I} (X;Y)&{}=\sum _{x\in {\mathcal {X}},y\in {\mathcal {Y}}}p_{(X,Y)}(x,y)\log {\frac {p_{(X,Y)}(x,y)}{p_{X}(x)p_{Y}(y)}}\\&{}=\sum _{x\in {\mathcal {X}},y\in {\mathcal {Y}}}p_{(X,Y)}(x,y)\log {\frac {p_{(X,Y)}(x,y)}{p_{X}(x)}}-\sum _{x\in {\mathcal {X}},y\in {\mathcal {Y}}}p_{(X,Y)}(x,y)\log p_{Y}(y)\\&{}=\sum _{x\in {\mathcal {X}},y\in {\mathcal {Y}}}p_{X}(x)p_{Y\mid X=x}(y)\log p_{Y\mid X=x}(y)-\sum _{x\in {\mathcal {X}},y\in {\mathcal {Y}}}p_{(X,Y)}(x,y)\log p_{Y}(y)\\&{}=\sum _{x\in {\mathcal {X}}}p_{X}(x)\left(\sum _{y\in {\mathcal {Y}}}p_{Y\mid X=x}(y)\log p_{Y\mid X=x}(y)\right)-\sum _{y\in {\mathcal {Y}}}\left(\sum _{x\in {\mathcal {X}}}p_{(X,Y)}(x,y)\right)\log p_{Y}(y)\\&{}=-\sum _{x\in {\mathcal {X}}}p_{X}(x)\mathrm {H} (Y\mid X=x)-\sum _{y\in {\mathcal {Y}}}p_{Y}(y)\log p_{Y}(y)\\&{}=-\mathrm {H} (Y\mid X)+\mathrm {H} (Y)\\&{}=\mathrm {H} (Y)-\mathrm {H} (Y\mid X).\\\end{aligned}}} $$
