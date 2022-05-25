# Instruction
We've attached a dataset, MNIST.mat, containing a sample of the famous MNIST benchmark.

Your report must provide summaries of each method's performance and some additional details of your implementation. Compare the relative strengths and weaknesses of the methods based on both the experimental results and your understanding of the algorithms.

You can load the data with scipy.io.loadmat, which will return a Python dictionary containing the test and train data and labels.

The purpose of this assignment is for you to implement the SVM. You are not allowed to import an SVM from, for instance, scikit-learn. You may, however, use a library (such as scipy.optimize.minimize or cvxopt.solvers.qp) for the optimization process

## (a)
Develop code for training an SVM for binary classification with nonlinear kernels. You'll need to accomodate non-overlapping class distributions. One way to implement this is to maximize (7.32) subject to (7.33) and (7.34). It may be helpful to redefine these as matrix operations.

## (b)
Develop code to predict the  {−1,+1}  class for new data. To use the predictive model (7.13) you need to determine  b , which can be done with (7.37).

## (c)
Using your implementation, compare multiclass classification performance of two different voting schemes:

one versus rest

one versus one

## (d)
The parameter  C>0  controls the tradeoff between the size of the margin and the slack variable penalty. It is analogous to the inverse of a regularization coefficient. Include in your report a brief discussion of how you found an appropriate value.

## (e)
In addition to calculating percent accuracy, generate multiclass confusion matrices as part of your analysis.

