# -*- coding: utf-8 -*-
"""“tufts-cs135-spring2022-ps4.ipynb”的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HFiPNNIw5Y3QvpxZY_MOyGWdBgnGLWF7

# Instructions

We've attached a dataset, [MNIST.mat](https://piazza.com/class_profile/get_resource/kxw9rxad40i41x/l1i0smrrkhw1mv), containing a sample of the famous MNIST benchmark.

Your report must provide summaries of each method's performance and some additional details of your implementation. Compare the relative strengths and weaknesses of the methods based on both the experimental results and your understanding of the algorithms.

You can load the data with `scipy.io.loadmat`, which will return a Python dictionary containing the test and train data and labels.

The purpose of this assignment is for you to implement the SVM.
You are not allowed to import an SVM from, for instance, `scikit-learn`.
You may, however, use a library (such as `scipy.optimize.minimize` or `cvxopt.solvers.qp`) for the optimization process.
"""

import numpy as np
from numpy.linalg import matrix_rank
from scipy.io import loadmat
import cvxopt
import cvxopt.solvers
from scipy.spatial.distance import pdist, squareform
import scipy
from cvxopt import matrix

# drag and drop MNIST.mat in the files section of Google Colab
# the file should appear next to the default sample_data folder
mnist = loadmat('MNIST.mat')
test_samples = mnist['test_samples']
test_samples_labels = mnist['test_samples_labels']
train_samples = mnist['train_samples']
train_samples_labels = mnist['train_samples_labels']

"""(a) Develop code for training an SVM for binary classification with nonlinear kernels. You'll need to accomodate non-overlapping class distributions. One way to implement this is to maximize (7.32) subject to (7.33) and (7.34). It may be helpful to redefine these as matrix operations. Let ${1}\in\mathbb{R}^{N\times 1}$ be the vector whose entries are all 1's. Let $\mathbf{a}\in\mathbb{R}^{N\times 1}$ have entries $a_i$. Let $\mathbf{T}\in\mathbb{R}^{N\times N}$ be a diagonal matrix with $\mathbf{T}_{ii} = t_i$ on the diagonal. Then we can reformulate the objective to be

\begin{equation*}
\begin{aligned}
& \text{maximize}
& & \tilde{L}(\mathbf{a}) = {1}^{\mathrm{T}}\mathbf{a} - \frac{1}{2} \mathbf{a}^{\mathrm{T}} \mathbf{T}\mathbf{K} \mathbf{T}\mathbf{a} \\
& \text{subject to}
& & {1}^{\mathrm{T}} \mathbf{a} \preceq C \\
& & & {1}^{\mathrm{T}} \mathbf{a} \succeq 0 \\
& & & \mathbf{a}^{\mathrm{T}} \mathbf{t} = 0
\end{aligned}
\end{equation*}

The "$\preceq$" symbol here means element-wise comparison. This formulation is very close to what `cvxopt` expects.

Hint (`cvxopt` expects the following form):

\begin{equation*}
\begin{aligned}
& \text{minimize}
& & \tilde{L}(\mathbf{a}) = \frac{1}{2} \mathbf{a}^{\mathrm{T}} \mathbf{T}\mathbf{K} \mathbf{T}\mathbf{a} - {1}^{\mathrm{T}}\mathbf{a} \\
& \text{subject to}
& & G \mathbf{a} \preceq h \\
& & & {\mathbf{t}}^{\mathrm{T}}\mathbf{a} = 0
\end{aligned}
\end{equation*}

where $G$ is an $N\times N$ identity matrix ontop of $-1$ times an $N\times N$ identity matrix and $h \in\mathbb{R}^{2N}$ where the first $N$ entries are $C$ and the second $N$ enties are $0$.

(b) Develop code to predict the $\{-1,+1\}$ class for new data. To use the predictive model (7.13) you need to determine $b$, which can be done with (7.37).
"""

def nonlinear_kernel(X):
  """
  Implement a nonlinear kernel function. Function parameters will vary depending on kernel function.

  Parameters
  ----------
  X : {array-like, sparse matrix} of shape (n_samples, n_features) or (n_samples, n_samples)
    Training vectors, where n_samples is the number of samples and n_features 
    is the number of features. For kernel=”precomputed”, the expected shape 
    of X is (n_samples, n_samples).

  y : array-like of shape (n_samples,)
    Target values (class labels in classification, real numbers in regression).
  """
  pairwise_dists = squareform(pdist(X, 'euclidean'))
  K = scipy.exp(-pairwise_dists ** 2 / 1 ** 2)
  return K


class SVM(object):

  def __init__(self, C=1, kernel=nonlinear_kernel):
    """
    Initialize SVM

    Parameters
    ----------
    kernel : callable
      Specifies the kernel type to be used in the algorithm. If none is given,
      ‘rbf’ will be used. If a callable is given it is used to pre-compute 
      the kernel matrix from data matrices; that matrix should be an array 
      of shape (n_samples, n_samples).
    C : float, default=1.0
      Regularization parameter. The strength of the regularization is inversely
      proportional to C. Must be strictly positive. The penalty is a squared l2
      penalty.
    """
    self.kernel = kernel
    self.C = C
    print(self.C)
    self.b = 0.0
    self.W = 0.0
    self.alpha = 0.0

  def fit(self, X, y):
    """
    Fit the SVM model according to the given training data.

    Parameters
    ----------
    X : {array-like, sparse matrix} of shape (n_samples, n_features) or (n_samples, n_samples)
      Training vectors, where n_samples is the number of samples and n_features 
      is the number of features. For kernel=”precomputed”, the expected shape 
      of X is (n_samples, n_samples).

    y : array-like of shape (n_samples,)
      Target values (class labels in classification, real numbers in regression).

    Returns
    -------
    self : object
      Fitted estimator.
    """
    # Hint:
    # 1. Define Quadratic Programming (QP) parameters. Given a QP optimization 
    #    problem in standard form, cvxopt is looking for P, q, G, h, A, and b
    #    (https://cvxopt.org/userguide/coneprog.html#quadratic-cone-programs).
    # 2. Construct the QP, invoke solver (use cvxopt.solvers.qp to maximize the Lagrange (7.32))
    # 3. Extract optimal value and solution. cvxopt.solvers.qp(P, q, G, h, A, b)["x"]
    #    are the Lagrange multipliers.
    # P = TKT, Q = -1(np.ones), G = ?, h∈R2N  where the first N entries are C and the second N enties are 0.
    # Cvxopt.matrix
    # Cvxopt.matrix(np.ndarray)
    # self.w += (a[i] * y[i] * X[i])



    length = X.shape[0]

    A = y.T

    

    T = np.zeros((length, length))
    for i in range(length):
      T[i, i] = y[i]
    

    
    K = nonlinear_kernel(X)

    P = T @ K @ T # dot product 
    P = cvxopt.matrix(P)
    A = cvxopt.matrix(A.astype(np.double))
    K = cvxopt.matrix(K)
    T = matrix(T)

    q = cvxopt.matrix(np.ones(length)* -1)
    
    G = cvxopt.matrix(np.zeros((2*length, length)))
    for i in range(length):
      G[i, i] = 1
    for i in range(length + 1, 2* length):
      G[i, i - length] = -1

    h = cvxopt.matrix(np.zeros(2*length))
    for i in range(length):
      h[i] = self.C

    b1 = 0.0
    b1 = matrix(b1)

    # print('p', P.size)
    # print('q', q.size)
    # print('G', G.size)
    # print('h', h.size)
    # print('A', A.size)
    # print('b1', b1.size)


    

    self.alpha = cvxopt.solvers.qp(P, q, G, h, A, b1)["x"]
    # print('alpha', self.alpha.size)

    W = np.zeros(X.shape[1])
    for i in range(length):
        W  += self.alpha[i] * X[i] * y[i]

    self.W = W

    # self.b = (-0.5) * ((np.max(X[y==-1]) + np.max(X[y==1])) * (self.W * X.T))
    # compute bias:
    for i in range(length):
      temp = 0.0
      for j in range(length):
        temp += self.alpha[i] * y[i] * K[i,j]
      self.b += (y[i] - temp)/length

    # print(self.alpha)
    # print(y)
    # print(self.b)
    return self

  def predict(self, X):
    """
    Perform classification on samples in X.

    For an one-class model, +1 or -1 is returned.

    Parameters
    ----------
    X : {array-like, sparse matrix} of shape (n_samples, n_features) or (n_samples_test, n_samples_train)

    Returns
    -------
    y_pred : ndarray of shape (n_samples,)
      Class labels for samples in X.
    """
    res = np.zeros(X.shape[0])
    # print(self.W.size, X.size, self.b.size)
    for i in range(X.shape[0]):
        temp = self.W @ X[i].T + self.b
        if temp > 0:
          res[i] = 1
        else:
          res[i] = -1
    return res

  def score(self, X, y):
    """
    Return the mean accuracy on the given test data and labels. 
    
    In multi-label classification, this is the subset accuracy which is a harsh 
    metric since you require for each sample that each label set be correctly 
    predicted.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
      Test samples.
    y : array-like of shape (n_samples,) or (n_samples, n_outputs)
      True labels for X.

    Return
    ------
    score : float
      Mean accuracy of self.predict(X)
    """
    right_count = 0
    result = self.predict(X)
    for i in range(X.shape[0]):
        if result[i] == y[i]:
            right_count += 1
    return right_count / len(X)

"""(c) Using your implementation, compare multiclass classification performance of two different voting schemes:

* one versus rest
* one versus one
"""

# one to rest 
rest_res = []
for m in range(10):
  one_to_rest_label = np.int16(train_samples_labels.copy())
  for i in range(len(train_samples_labels)):
    if one_to_rest_label[i] != m:
      one_to_rest_label[i] = -1
    else:
      one_to_rest_label[i] = 1
  svm = SVM()

  svm.fit(train_samples, one_to_rest_label)

  one_to_rest_test_label = np.int16(test_samples_labels.copy())
  for i in range(len(test_samples_labels)):
    if one_to_rest_test_label[i] != m:
      one_to_rest_test_label[i] = -1
    else:
      one_to_rest_test_label[i] = 1
  rest_res.append(svm.score(test_samples, one_to_rest_test_label))

print(rest_res)

# one to one 
res = np.zeros((10,10))
training_result = {}
for i in range(10):
  for j in range(i+1, 10):
    svm = SVM()
    # get training samples and label
    index = np.concatenate((np.where(train_samples_labels == i)[0],np.where(train_samples_labels == j)[0]), axis = None)
    one_one_train_sample = train_samples[index]
    one_one_train_label = train_samples_labels[index]

    for m in range(len(one_one_train_label)):
      if one_one_train_label[m] == i:
        one_one_train_label[m] = 1
      else:
        one_one_train_label[m] = -1
    svm.fit(one_one_train_sample, one_one_train_label)

    # get testing samples and labels
    index_test = np.concatenate((np.where(test_samples_labels == i)[0],np.where(test_samples_labels == j)[0]), axis = None)
    one_one_test_sample = test_samples[index_test]
    one_one_test_label = test_samples_labels[index_test]

    for k in range(len(one_one_test_label)):
      if one_one_test_label[k] != i:
        one_one_test_label[k] = -1
      else:
        one_one_test_label[k] = 1

    # score
    temp = svm.score(one_one_test_sample, one_one_test_label)
    training_result[i,j] = temp
print(training_result)

"""(d) The parameter $C>0$ controls the tradeoff between the size of the margin and the slack variable penalty. It is analogous to the inverse of a regularization coefficient. Include in your report a brief discussion of how you found an appropriate value."""

# one to rest 
c_values = np.logspace(0, 1, 10, endpoint=True)
mean_cal = {}
for k in range(10):
  rest_res = []
  for m in range(10):
    one_to_rest_label = np.int16(train_samples_labels.copy())
    for i in range(len(train_samples_labels)):
      if one_to_rest_label[i] != m:
        one_to_rest_label[i] = -1
      else:
        one_to_rest_label[i] = 1
    svm = SVM(c_values[k])

    svm.fit(train_samples, one_to_rest_label)

    one_to_rest_test_label = np.int16(test_samples_labels.copy())
    for i in range(len(test_samples_labels)):
      if one_to_rest_test_label[i] != m:
        one_to_rest_test_label[i] = -1
      else:
        one_to_rest_test_label[i] = 1
    rest_res.append(svm.score(test_samples, one_to_rest_test_label))
  mean_cal[c_values[k]] = rest_res

"""I created np.logspace(0, 1, 10, endpoint=True) to generate 10 different C value between 1 and 10. Due to the long run time I decide only running one to rest instead of one to one. And I ran it locally, the code above also work if like to try.*(But so far SVM has set C=1 as default, if you like to run it just replace C=1 to C, and run the code above)*

And here is the result:

{1.0: [0.962, 0.995, 0.904, 0.813, 0.897, 0.955, 0.95, 0.949, 0.54, 0.838], 1.2915496650148839: [0.961, 0.988, 0.905, 0.805, 0.895, 0.955, 0.948, 0.947, 0.504, 0.834], 1.6681005372000588: [0.961, 0.986, 0.906, 0.813, 0.902, 0.954, 0.941, 0.949, 0.475, 0.82], 2.154434690031884: [0.963, 0.98, 0.894, 0.805, 0.901, 0.95, 0.934, 0.952, 0.442, 0.817], 2.7825594022071245: [0.962, 0.976, 0.872, 0.798, 0.904, 0.947, 0.924, 0.952, 0.396, 0.813], 3.5938136638046276: [0.958, 0.966, 0.852, 0.798, 0.904, 0.945, 0.918, 0.949, 0.362, 0.799], 4.641588833612778: [0.958, 0.957, 0.831, 0.8, 0.898, 0.944, 0.913, 0.946, 0.344, 0.786], 5.994842503189409: [0.957, 0.954, 0.822, 0.805, 0.894, 0.941, 0.907, 0.944, 0.329, 0.779], 7.742636826811269: [0.957, 0.953, 0.814, 0.804, 0.892, 0.941, 0.903, 0.942, 0.329, 0.779], 10.0: [0.959, 0.95, 0.813, 0.812, 0.891, 0.942, 0.903, 0.942, 0.336, 0.771]}
"""

import numpy as np
result = {1.0: [0.962, 0.995, 0.904, 0.813, 0.897, 0.955, 0.95, 0.949, 0.54, 0.838], 1.2915496650148839: [0.961, 0.988, 0.905, 0.805, 0.895, 0.955, 0.948, 0.947, 0.504, 0.834], 1.6681005372000588: [0.961, 0.986, 0.906, 0.813, 0.902, 0.954, 0.941, 0.949, 0.475, 0.82], 2.154434690031884: [0.963, 0.98, 0.894, 0.805, 0.901, 0.95, 0.934, 0.952, 0.442, 0.817], 2.7825594022071245: [0.962, 0.976, 0.872, 0.798, 0.904, 0.947, 0.924, 0.952, 0.396, 0.813], 3.5938136638046276: [0.958, 0.966, 0.852, 0.798, 0.904, 0.945, 0.918, 0.949, 0.362, 0.799], 4.641588833612778: [0.958, 0.957, 0.831, 0.8, 0.898, 0.944, 0.913, 0.946, 0.344, 0.786], 5.994842503189409: [0.957, 0.954, 0.822, 0.805, 0.894, 0.941, 0.907, 0.944, 0.329, 0.779], 7.742636826811269: [0.957, 0.953, 0.814, 0.804, 0.892, 0.941, 0.903, 0.942, 0.329, 0.779], 10.0: [0.959, 0.95, 0.813, 0.812, 0.891, 0.942, 0.903, 0.942, 0.336, 0.771]}

analysis = {}
for key in result.keys():
  temp = result[key]
  temp_list = [np.average(temp), np.var(temp), np.std(temp)]
  analysis[key] = temp_list

print(analysis)

"""I compute score of each label with 10 different C. Also, I compute the **mean, variance and std** for list of score for each C. The result is showed above. It is not hard to find out that as C grows high from 1 to 10 the score is getting lower. So, I believe 1 is the best. But I didn't have time to compute the C lower than 1 given that compute such data took me 5 hours.

(e) In addition to calculating percent accuracy, generate multiclass [confusion matrices](https://en.wikipedia.org/wiki/confusion_matrix) as part of your analysis.
"""

import pandas as pd
# the following code will compute the predict result but not score
# here I test one to rest not one to one( it takes too long :( )
confustion_matrix = []
for m in range(5):
  one_to_rest_label = np.int16(train_samples_labels.copy())
  for i in range(len(train_samples_labels)):
    if one_to_rest_label[i] != m:
      one_to_rest_label[i] = -1
    else:
      one_to_rest_label[i] = 1
  svm = SVM()

  svm.fit(train_samples, one_to_rest_label)

  one_to_rest_test_label = np.int16(test_samples_labels.copy())
  for i in range(len(test_samples_labels)):
    if one_to_rest_test_label[i] != m:
      one_to_rest_test_label[i] = -1
    else:
      one_to_rest_test_label[i] = 1

  temp = svm.predict(test_samples)
  temp_matrix = []
  # the confusion matrix is generate here
  for w in range(temp.shape[0]):
    if one_to_rest_test_label[w] ==1 and temp[w] == 1:
      temp_matrix.append('TP')
    if one_to_rest_test_label[w] ==1 and temp[w] != 1:
      temp_matrix.append('FN')
    if one_to_rest_test_label[w] !=1 and temp[w] == 1:
      temp_matrix.append('FP')
    if one_to_rest_test_label[w] !=1 and temp[w] != 1:
      temp_matrix.append('TN')
    confustion_matrix.append(temp_matrix)
df = pd.DataFrame(confustion_matrix)

df