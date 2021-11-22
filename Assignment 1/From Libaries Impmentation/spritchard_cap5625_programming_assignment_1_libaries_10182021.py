# -*- coding: utf-8 -*-
"""SPritchard_CAP5625_Programming_Assignment 1_Libaries_10182021.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W0aaP4C2_QJo4NTQ-mrODOepyaWxnQa-

- **Programmer: Shaun Pritchard**
- **Date: 10-10-2021**
- **Assignment: 1**
- **Prof: Michael DeGiorgio**
<hr>

# **CAP 52625 COMPUTATIONAL FOUDNATIONS OF AI**

##Ridge Regression using Gradient Descent using Scikit Learn - Assignment 1
<hr>

**Perform a penalized (regularized) least squares fit of a linear model using ridge regression, with the model parameters obtained by batch gradient descent. The tuning parameter will be chosen using five-fold cross validation, and the best-fit model parameters will be inferred on the training dataset conditional on an optimal tuning parameter**

## **Deliverables**
*   **Deliverable 6**  Implement the assignment using statistical or machine learning libraries in a language of your choice.Compare the results with those obtained above, and
provide a discussion as to why you believe your results are different if you found them to be different.

> Note:  I implemented 2 variations of the cross validation tuning prama error output charts using using the absolute vlaue on the regression errors to check variation as per the asignment.



***Deliverable 1-5 located here:***
https://colab.research.google.com/gist/shaungt1/83c9e75f7062e34897957859165f3a0d/spritchard_cap5625_programming_assignment-1_10182021.ipynb

<hr>

## **Set Up and Import Data for proccessing**
> Import the credit balance dataset 
- 𝑁=400 training  observations
- 𝑝=9 features
"""

# Commented out IPython magic to ensure Python compatibility.
#Project Imports
# Data Science libs
from math import sqrt
from scipy import stats
import numpy as np
import pandas as pd
# Graphics libs
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
# labries for stat testing
import statsmodels.api as sm
import statsmodels.formula.api as smf
# sklearn liabries for ridge regression and cross vlaidation
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import make_scorer, mean_squared_error

# Mount Google Drive for data access
from google.colab import drive
drive.mount('/content/drive')

# Set up dataframe
df = pd.read_csv('/content/drive/MyDrive/Florida_Atlantic_University/Computational_Foundations_of_ AI/Credit_N400_p9.csv')
# Set up datafeme for testing
# df = pd.read_csv('/content/Credit_N400_p9.csv')

# Check the imported data & features
df.head(3)

"""## **Pre-Proccess Data**

- Re-assign categorical featre attributes with bianary dummy variables
- Split real X and y nx1 features
"""

#Assign dummy variables to catigorical features with new dataframe
df1 = df.replace({'Male': 0, 'Female':1, 'No': 0, 'Yes': 1})

# Validate categorical dummy variables
df1.head(3)

# Seperate real features to variable X
X = df1.iloc[:, :-1].values

# Seperate real features to variable X
y = df1.iloc[:, -1].values

# Check X features
print('Matrix shape X := {X}\nValidate array:(row:col)'  .format(X = X.shape), '\n', X)

# Check y features
print('Matrix shape y := {y}\nValidate array:(row:col)'  .format(y = y.shape), '\n', y)

"""## **Scale, Center and Standardize Data**"""

# Implement standardize used for X with SciKit learn
standardize = StandardScaler()
#Implement Center for y (implemented in scikit learn Ridge() method)
y_center = StandardScaler(with_std=False)

# Apply standardize to X
X = standardize.fit_transform(X)
X = pd.DataFrame(X)

# Label column headers for X
X.columns=['Income', 'Limit', 'Rating', 'Cards', 'Age', 'Education', 'Gender', 'Student', 'Married']

# Check X column head
print('X standardized feture vector\n', X)

"""## **Evaluate Model with Ridge Regression BGD w/ Scikit Learn**"""

# Set local tunning parameters 
λ=[1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4]

# Evaluate tuning parameters with ridge regression L2 penalty
𝛽x=[] # set empty list
for lamb in λ:
    # Solver set to auto to best fit data 
    ridge=Ridge(alpha=lamb, max_iter=1000)
    # fir the ridge regression coefficients
    ridge.fit(X, y)
    print('X & y features:={}\n'.format(ridge.fit(X, y)))
    𝛽x.append(ridge.coef_)

"""## **Deliverable 1**
- Build graph of dataset N=9 features tuning parameter effect on inferred Ridge regression
"""

# Output Deviverable 6.1: inferred tuning parmeters of ridge regresion using libaries
sns.set_theme()
sns.set_style("darkgrid", {"grid.color": ".5","image.cmap": "mako", "grid.linestyle": ":" })
dev1=pd.DataFrame(𝛽x)
dev1.index=λ
dev1.columns=['Income', 'Limit', 'Rating', 'Cards', 'Age', 'Education', 'Gender', 'Student', 'Married']
plt.rcParams["figure.figsize"] = (16,10)
dev1.plot()
plt.title('Deliverable 6.1: Tuning parameter effect on inferred Ridge Regression')
plt.xlabel('λ Tuning Params')
plt.ylabel('p=9 features')
plt.xscale('log')
plt.legend(loc='lower right', title='Beta_λ')
plt.show()

"""## **(5) K-fold Cross Validation Algorithm w/ Scikit Learn**"""

# Evaluate Ridge with CV gridsearch 5 k-folds 1000 iterations
ridge=Ridge(max_iter=1000)
parameters={'alpha': λ}
# Calculate MSE 
MSE=make_scorer(mean_squared_error, greater_is_better=False)
# use grid search with 5-k-folds
ridge_regressor=GridSearchCV(ridge, parameters, scoring=MSE, cv=5, refit=False)
# Fit ridge regression to cross validation folds
ridge_regressor.fit(X, y)

"""## **Deliverable 2**

 Illustrate the effect of the tuning parameter on the cross-validation error
"""

# Plot the effect of the tuning parameter on the cross-validation error
sns.set_theme()
sns.set_style("darkgrid", {"grid.color": ".5","image.cmap": "mako", "grid.linestyle": ":" })
plt.plot(λ, np.absolute(ridge_regressor.cv_results_['mean_test_score']), color="purple")
plt.title('Effect of the tuning parameter on the 5 K-fold CV error')
plt.rcParams["figure.figsize"] = (16,10)
plt.xscale('log')
plt.xlabel('λ')
plt.ylabel('CV error')
plt.show()
plt.figure(figsize=(10, 16), dpi=300)

"""## **Deliverable 3** 
Indicate the value of 𝜆 that generated the smallest CV(5)error
"""

# Output final results of lowest λ tuning param and best score
print("Best MSE score of λ\n", ridge_regressor.best_score_)
print("Best params of λ\n",ridge_regressor.best_params_)

"""## **Deliverable 4** 

- Given the optimal 𝜆, retrain your model on the entire dataset of 𝑁 = 400 observations and provide the estimates of the 𝑝 = 9 best-fit model parameters.
"""

# Retrain model based on λ = 1.0
ridge=Ridge(alpha=1, max_iter=1000)
# Fit data
ridge.fit(X, y)
# Output coefficients based on retrianed model at  λ = 1.0
ridge.coef_

"""<hr>

## **Alternate 2nd CV error Algorthm |X|**
"""

#Evaluate Ridge with CV gridsearch 5 k-folds 1000 iterations
# using grid search hyperparameters for ridge regression
# define model find best tuning param errors
model = Ridge()
# define model evaluation method
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)
# define grid
grid = dict()
grid['alpha'] = λ # set parementer to 1e-5
# define search
search = GridSearchCV(model, grid, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
# perform the search
results = search.fit(X, y)
# summarize
print('𝜆 that generated the smallest CV(5)error')
print('MSE: %.3f' % results.best_score_)
print('Config: %s' % results.best_params_)

# Illustrate the effect of the tuning parameter on the cross-validation error
plt.plot(λ, np.absolute(ridge_regressor.cv_results_['mean_test_score']), color="green")
plt.title('Effect of the tuning parameter on the 5 K-fold CV error')
plt.xscale('log')
plt.xlabel('λ')
plt.ylabel('CV error')
plt.show()
plt.figure(figsize=(10, 16), dpi=90)