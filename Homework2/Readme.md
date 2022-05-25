# Instruction

## Linear Regression
We are given data used in a study of the homicide rate (HOM) in Detroit, over the years 1961-1973. The following data were collected by J.C. Fisher, and used in his paper ”Homicide in Detroit: The Role of Firearms,” Criminology, vol. 14, pp. 387-400, 1976. Each row is for a year, and each column are values of a variable.

It turns out that three of the variables together are good predictors of the homicide rate: FTP, WE, and one more variable. Use methods described in Chapter 3 of the textbook to devise a mathematical formulation to determine the third variable. Implement your formulation and then conduct experiments to determine the third variable. In your report, be sure to provide the step-by-step mathematical formulation (citing Chapter 3 as needed) that corresponds to the implementation you turn in. Also give plots and a rigorous argument to justify the scheme you use and your conclusions.

Note: the file detroit.npy containing the data can be downloaded to your current directory on Colab using the command shown below. To load the data into Python, use X=numpy.load(‘detroit.npy’) command. Least-squares linear regression in Python can be done with the help of numpy.linalg.lstsq().

## k-Nearest Neighbors
For this problem, you will be implementing the k-Nearest Neighbor (k-NN) classifier and evaluating on the Credit Approval (CA) dataset. It describes credit worthiness data (in this case, binary classification). (see http://archive.ics.uci.edu/ml/datasets/Credit+Approval) We have split the available data into a training set crx.data.training and a testing set crx.data.testing. These are both comma-separated text files (CSVs).

The first step to working with the CA dataset is to process the data. In looking at the data description crx.names, note that there are some missing values, there exist both numerical and categorical features, and that it is a relatively balanced dataset (meaning a roughly equal number of positive and negative examples - not that you should particularly care in this case, but something you should look for in general). A great Python library for handling data like this is Pandas (https://pandas.pydata.org/pandas-docs/stable/). You can read in the data with X = pandas.read csv(‘crx.data.training’, header=None, na values=‘?’). The last option tells Pandas to treat the character ? as a missing value.

Pandas holds data in a "dataframe". We'll deal with individual rows and columns, which Pandas calls "series". Pandas contains many convenient tools, bu the most basic you'll use is X.iloc[i,j], accessing the element in the i-th row and j-th column. You can use this for both getting and setting values. You can also slice like normal Python, grabbing the i-th row with [i,:].

You can view the first 20 rows with X.head(20). The last column, number 15, contains the labels. You’ll see some elements are missing, marked with NaN. While there are more sophisticated (and better) methods for imputing missing values, for this assign- ment, we will just use mean/mode imputation. This means that for feature 0, you should replace all of the question marks with a b as this is the mode, the most common value (regardless if you condition on the label or not). For real-valued features, just replace missing values with the label-conditioned mean (e.g.  μ(x1|+)  for instances labeled as positive).

The second aspect one should consider is normalizing features. Nominal features can be left in their given form where we define the distance to be a constant value (e.g. 1) if they are different values, and 0 if they are the same. However, it is often wise to normalize real-valued features. For the purpose of this assignment, we will use  z -scaling, where

z(m)i←x(m)i−μiσi 

such that  z(m)  indicates feature  i  for instance  m  (similarly  x(m)  is the raw input),  μi  is the average value of feature  i  over all instances, and  σi  is the corresponding standard deviation over all instances.

In this notebook, include the following functions:

i. A function impute_missing_data() that accepts two Pandas dataframes, one training and one testing, and returns two dataframes with missing values filled in. In your report include your exact methods for each type of feature. Note that you are free to impute the values using statistics over the entire dataset (training and testing combined) or just training, but please state your method.

ii. A function normalize features() that accepts a training and testing dataframe and returns two dataframes with real-valued features normalized.

iii. A function distance() that accepts two rows of a dataframe and returns a float, the L2 distance:  DL2(a,b)=∑i(ai−bi)2−−−−−−−−−−√  . Note that we define  DL2  to have a component-wise value of 1 for categorical attribute-values that disagree and 0 if they do agree (as previously implied). Remember not to use the label column in your distance calculation!

iv. A funtion predict() that accepts three arguments: a training dataframe, a testing dataframe, and an integer  k  - the number of nearest neighbors to use in predicting. This function should return a column of  +/−  labels, one for every row in the testing data.

v. A function accuracy() that accepts two columns, one true labels and one predicted by your algorithm, and returns a float between 0 and 1, the fraction of labels you guessed correctly.

In your report, include accuracy results on crx.data.testing for at least three different values of k.

vi. Try your algorithm on some other data! We’ve included the “lenses” dataset (https://archive.ics.uci.edu/ml/datasets/Lenses). It has no missing values and only categorical attributes, so no need for imputation or normalization. Include accuracy results from lenses.testing in your report as well.

The code you submit must be your own. If you find/use information about specific algorithms from the Web, etc., be sure to cite the source(s) clearly in your sourcecode. You are not allowed to submit code downloaded from the internet (obviously).
