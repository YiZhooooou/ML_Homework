# -*- coding: utf-8 -*-
"""“tufts-cs135-2022spring-ps3.ipynb”的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zsX4yCSBW1-Xawan84ifPdbbs7Quw1Or

# Instructions

This file contains code that helps you get started on the programming assignment. You will need to complete the function `sample_images()`, `sparse_auto_encoder()`, and `compute_numerical_gradient()`.

**STEP 0:** Here we provide the relevant parameters values that will allow your sparse autoencoder to get good filters; you do not need to change the parameters below.
"""

import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random
import gc
import scipy
from scipy.io import loadmat
import scipy.optimize

patch_size = 8
num_patches = 10000
visible_size = 8*8     # number of input units 
hidden_size = 25       # number of hidden units 
sparsity_param = 0.01  # desired average activation of the hidden units.
                        # (This was denoted by the Greek alphabet rho, which 
                        # looks like a lower-case "p", in the lecture notes). 
decay_lambda = 0.0001  # weight decay parameter (lambda)
beta = 3               # weight of sparsity penalty term

"""**STEP 1:** Implement `sample_images()`

After implementing `sample_images()`, the `display_network()` function should display a random sample of 100 patches from the dataset
"""

# This function visualizes filters in matrix A. Each row of A is a
# filter. We will reshape each row into a square image and visualizes
# on each cell of the visualization panel.
# All other parameters are optional, usually you do not need to worry
# about it.
# opt_normalize: whether we need to normalize the filter so that all of
# them can have similar contrast. Default value is true.
# opt_graycolor: whether we use gray as the heat map. Default is true.
# cols: how many rows are there in the display. Default value is the
# squareroot of the number of rows in A.
def display_network(data, cols=-1, opt_normalize=True, opt_graycolor=True, save_figure_path=None):

    # rescale
    data -= np.mean(data)

    # compute rows, cols
    num, area = data.shape
    sz = int(math.sqrt(area))
    buf = 1
    if cols < 0:
        if math.floor(math.sqrt(num)) ** 2 != num:
            n = math.ceil(math.sqrt(num))
            while num % n != 0 and n < 1.2 * math.sqrt(num):
                n += 1
                m = math.ceil(num / n)
        else:
            n = math.sqrt(num)
            m = n
    else:
        n = cols
        m = math.ceil(num / n)
    n = int(n)
    m = int(m)

    array = -np.ones((buf + m * (sz + buf), buf + n * (sz + buf)))

    if not opt_graycolor:
        array *= 0.1

    k = 0
    for i in range(m):
        for j in range(n):
            if k >= num:
                continue
            if opt_normalize:
                clim = np.amax(np.absolute(data[k, :]))
            else:
                clim = np.amax(np.absolute(data))
            array[buf + i * (sz + buf):buf + i * (sz + buf) + sz,
            buf + j * (sz + buf):buf + j * (sz + buf) + sz] = data[k, :].reshape([sz, sz]) / clim
            k += 1

    # simulate imagesc
    ax = plt.figure().gca()
    pix_width = 5
    h, w = array.shape
    exts = (0, pix_width * w, 0, pix_width * h)
    if opt_graycolor:
        ax.imshow(array, interpolation='nearest', extent=exts, cmap=cm.gray)
    else:
        ax.imshow(array, interpolation='nearest', extent=exts)

    plt.axis('off')

    if save_figure_path:
        plt.savefig(save_figure_path)

    plt.show()

def initialize_parameters(hidden_size, visible_size):
    # Initialize parameters randomly based on layer sizes.
    r = math.sqrt(6) / math.sqrt(hidden_size + visible_size + 1)  # we'll choose weights uniformly from the interval [-r, r]
    w1 = np.random.rand(visible_size, hidden_size) * 2 * r - r
    w2 = np.random.rand(hidden_size, visible_size) * 2 * r - r

    b1 = np.zeros((1, hidden_size))
    b2 = np.zeros((1, visible_size))

    # Convert weights and bias gradients to the vector form.
    # This step will "unroll" (flatten and concatenate together) all
    # your parameters into a vector, which can then be used with minFunc.
    theta = np.concatenate((w1.flatten(), w2.flatten(), b1.flatten(), b2.flatten()))

    return theta

# TODO:
def normalize_data(patches):
    mean = patches.mean(axis = 0)
    patches -= mean

    sd = patches.std() * 3
    patches /= sd

    patches = (patches + 1)* 0.4 + 0.1

    return patches

# @param: patch_size: the size of patch (patch_size x patch size)
#     num_patches: # of samples 
# return patches [[patch_size , patch_size], num_patches]
def sample_images(patch_size, num_patches):
    
    images = loadmat('IMAGES.mat')['IMAGES']  # load images from disk
    num_images = images.shape[2]
    images_length = images.shape[1]
    target = images_length - patch_size
    patches_collection = np.zeros(shape=(patch_size*patch_size, num_patches))
    for i in range(num_patches):
      # find a random image
      sample_idex = random.randint(0, num_images - 1)
      random_images = images[:, :, sample_idex]
      # find out a random starting origin
      left_xcoord = random.randint(0, target)
      top_ycoord = random.randint(0, target)
      # get the sample
      patch = random_images[left_xcoord: left_xcoord + patch_size, top_ycoord: top_ycoord + patch_size].reshape(patch_size*patch_size)
      # put it in the collection
      patches_collection[:, i] = patch

      
    return normalize_data(patches_collection)

patches = sample_images(patch_size, num_patches)

display_network(patches[np.random.randint(patches.shape[0], size=100), :])

# Obtain random parameters theta
theta = initialize_parameters(hidden_size, visible_size)

"""**STEP 2:** Implement sparseAutoencoderCost

You can implement all of the components (squared error cost, weight decay term, sparsity penalty) in the cost function at once, but it may be easier to do it step-by-step and run gradient checking (see STEP 3) after each step.  We suggest implementing the `sparse_autoencoder_cost()` function using the following steps:


*   Implement forward propagation in your neural network, and implement the squared error term of the cost function.  Implement backpropagation to compute the derivatives.   Then (using lambda=beta=0), run Gradient Checking to verify that the calculations corresponding to the squared error cost term are correct.

*   Add in the weight decay term (in both the cost function and the derivative calculations), then re-run Gradient Checking to verify correctness. 

*   Add in the sparsity penalty term, then re-run Gradient Checking to verify correctness. Feel free to change the training settings when debugging your code.  (For example, reducing the training set size or number of hidden units may make your code run faster; and setting beta and/or lambda to zero may be helpful for debugging.)  However, in your final submission of the visualized weights, please use parameters we gave in Step 0 above.
"""

from numpy.random.mtrand import exponential
# TODO:

# Sparse Autoencoder Cost:
# sparse_autoencoder_cost takes in parameters describing a neural network as well
# as data and computes the cost and gradient for that network given the data.

# To compute the cost, a feedforward pass is performed to compute the values of 
# both the output and hidden layers. From here the cost is computed using
# the formula listed in the pdf handout (see Piazza resources), which is
# towards the bottom of page 15.

# To compute the gradients, you will perform backpropogation and use the second
# formula listed on page 16.

# Most of the parameters describing the neural network are singular scaler
# values, however the theta parameter is an array containing all weights
# and bias terms. It is up to you to decide what elements in theta correspond
# to what parts of the network, but make sure that the gradient that you return
# is both the same size as theta and also uses the same schema as far as what
# elements correspond to what parts of the neural network.

# Parameters
#     - theta: a numpy array containing the weights and biases for each node in
#              the neural network
#     - visible_size: the number of input units (probably 64)
#     - hidden_size: the number of hidden units (probably 25)
#     - decay_lambda: weight decay parameter
#     - sparsity_param: The desired average activation for the hidden units (denoted in the lecture
#                       notes by the greek alphabet rho, which looks like a lower-case "p").
#     - beta: weight of sparsity penalty term
#     - data: Our 10000x64 matrix containing the training data.  So, data(i,:) is the i-th training example.

# Returns
#     - cost: A single value denoting the 
#     - grad: The delta values for each weight and bias term of the network. These
#             values denote how much each weight or bias term should be changed
#             in the next iteration of gtadient descent.
def sparse_autoencoder_cost(theta, visible_size, hidden_size, decay_lambda, sparsity_param, beta, data):

    # # of training size
    m = data.shape[1]

    # edges between first and second layer
    W12 = theta[0: hidden_size * visible_size].reshape(hidden_size, visible_size)
    W23 = theta[hidden_size * visible_size: hidden_size * visible_size * 2].reshape(visible_size, hidden_size)
    B2 = theta[hidden_size * visible_size * 2: hidden_size * visible_size * 2 + hidden_size]
    B3 = theta[hidden_size * visible_size * 2 + hidden_size : hidden_size * visible_size * 2 + hidden_size + visible_size]
    # reshape bia vetor to matrix
    B2_ = np.tile(B2, (m, 1)).transpose()
    B3_ = np.tile(B3, (m, 1)).transpose()

    # compute feedfoward
    # compute Wx + b
    Z12 = np.dot(W12, data) + B2_
    Z23 = np.dot(W23, Z12) + B3_

    # activation 
    a12 = 1/ (1 + np.exp(-Z12))
    # print(a12.shape)
    a23 = 1/ (1 + np.exp(-Z23))

    # Sparsity
    # rho for hidden layer
    p = np.tile(sparsity_param, hidden_size)
    p_ = np.sum(a12, axis=1)/ m
    # print(p_)

    # KL paramater
    KL = np.sum(p * np.log(p/p_) + (1-p) * np.log((1-p)/(1-p_)))
    # print(np.log(p/p_))
    # print((1-p)/(1 -p_))

    # cost computation
    # J function
    J = np.sum((a23 - data) ** 2)/ m/ 2 + (decay_lambda / 2) * (np.sum(W12 ** 2) + np.sum(W23 ** 2)) 
    cost = J + beta * KL

    # back propogation
    # find activation prime
    a_12 = a12 * (1 - a12)
    a_23 = a23 * (1 - a23)

    # find out the error term for each layer
    p_trick = -p/p_ + (1 - p)/(1 - p_)
    e3 = -(data - a23) * a_23
    e2 = (np.dot(W23.transpose(), e3) + beta * np.tile(p_trick, (m, 1)).transpose()) * a_12
    
    
    # find out the gradient (not sure)

    W12_grad = (np.dot(e2, data.transpose()) / m + decay_lambda * W12).reshape(hidden_size * visible_size)
    W23_grad = (np.dot(e3, a12.transpose()) / m + decay_lambda * W23).reshape(hidden_size * visible_size)
    b1_grad = (np.sum(e2, axis=1) / m).reshape(hidden_size)
    b2_grad = (np.sum(e3, axis=1) / m).reshape(visible_size)

    grad = np.concatenate((W12_grad, W23_grad, b1_grad, b2_grad))

    return cost, grad

print(theta.shape)
cost, grad = sparse_autoencoder_cost(theta, visible_size, hidden_size, decay_lambda, sparsity_param, beta, patches)

"""**Step 3:** Gradient Checking

Hint: If you are debugging your code, performing gradient checking on smaller models and smaller training sets (e.g., using only 10 training examples and 1-2 hidden units) may speed things up.
"""

# TODO:
# theta: a vector of parameters
# func: a function that outputs a real-number. Calling y = J(theta) will return the
# function value at theta.
def compute_numerical_gradient(func, theta, *args, dtype=float):

    # Initialize numgrad (no need to initialize to zero, empty_like is a good fit here)
    numgrad = np.empty_like(theta)
    numgrad.astype(np.float64)
    # set a small epsilon
    eps = 0.0001

    # Instructions: 
    # Implement numerical gradient checking, and return the result in numgrad.  
    # (See Section 2.3 of the lecture notes.)
    # You should write code so that numgrad(i) is (the numerical approximation to) the 
    # partial derivative of func with respect to the i-th input argument, evaluated at theta.
    # I.e., numgrad(i) should be the (approximately) the partial derivative of func with
    # respect to theta(i).
    #
    # Hint: You will probably want to compute the elements of numgrad one at a time.

    for i in range(theta.shape[0]):
      left_term, right_term = theta.copy(), theta.copy()
      left_term[i] = theta[i] + eps
      right_term[i] = theta[i] - eps
      numgrad[i] = (func(left_term, *args)[0] - func(right_term, *args)[0]) / 2 / eps

    return numgrad

# this function accepts a 2D vector as input. 
# Its outputs are:
# value: h(x1, x2) = x1^2 + 3*x1*x2
# grad: A 2x1 vector that gives the partial derivatives of h with respect to x1 and x2 
# Note that when we pass @simpleQuadraticFunction(x) to computeNumericalGradients, we're assuming
# that computeNumericalGradients will use only the first returned value of this function.
def simple_quadratic_function(x):
    value = pow(x[0], 2) + 3*x[0]*x[1]
    grad = np.zeros(2)
    grad[0]  = 2*x[0] + 3*x[1]
    grad[1]  = 3*x[0]
    return value, grad

# This code can be used to check your numerical gradient implementation 
# in computeNumericalGradient.m
# It analytically evaluates the gradient of a very simple function called
# simpleQuadraticFunction (see below) and compares the result with your numerical
# solution. Your numerical gradient implementation is incorrect if
# your numerical solution deviates too much from the analytical solution.
def check_numerical_gradient():
    # Evaluate the function and gradient at x = [4; 10] (Here, x is a 2d vector.)
    x = [4, 10]
    value, grad = simple_quadratic_function(x)

    # Use your code to numerically compute the gradient of simpleQuadraticFunction at x.
    # (The notation "@simpleQuadraticFunction" denotes a pointer to a function.)
    numgrad = compute_numerical_gradient(simple_quadratic_function, x)

    # Visually examine the two gradient computations.  The two columns
    # you get should be very similar. 
    disp = "\n".join("{} {}".format(x, y) for x, y in zip(numgrad, grad))
    print(disp)
    print("The above two columns you get should be very similar.\n(Left-Your Numerical Gradient, Right-Analytical Gradient)\n\n")

    # Evaluate the norm of the difference between two solutions.  
    # If you have a correct implementation, and assuming you used EPSILON = 0.0001 
    # in computeNumericalGradient.m, then diff below should be 2.1452e-12 
    diff = np.linalg.norm(numgrad-grad)/np.linalg.norm(numgrad+grad)
    print(diff)
    print("Norm of the difference between numerical and analytical gradient (should be < 1e-9)\n\n")

# First, lets make sure your numerical gradient computation is correct for a 
# simple function.  After you have implemented computeNumericalGradient.m, 
# run the following:
check_numerical_gradient()

# Now we can use it to check your cost function and derivative calculations
# for the sparse autoencoder. 
 
numgrad = compute_numerical_gradient(sparse_autoencoder_cost, theta, visible_size, hidden_size, decay_lambda, sparsity_param, beta, patches)

# Use this to visually compare the gradients side by side
disp = "\n".join("{} {}".format(x, y) for x, y in zip(numgrad, grad))
print(disp)

# Compare numerically computed gradients with the ones obtained from backpropagation
diff = np.linalg.norm(numgrad - grad)/np.linalg.norm(numgrad + grad)
print(diff)  # Should be small. In our implementation, these values are
              # usually less than 1e-9.
              # When you got this working, Congratulations!!!

"""**Step 4:** After verifying that your implementation of `sparse_autoencoder_cost()` is correct, You can start training your sparse autoencoder with scipy's minimize function (L-BFGS)."""

# Randomly initialize the parameters
theta = initialize_parameters(hidden_size, visible_size)

# Here, we use L-BFGS to optimize our cost
# function. Generally, for minimize to work, you
# need a function pointer with two outputs: the
# function value and the gradient. In our problem,
# sparseAutoencoderCost.m satisfies this.

# Use scipy's minimize to minimize the function
res = scipy.optimize.minimize(
    fun=sparse_autoencoder_cost, 
    x0=theta, 
    args=(visible_size, hidden_size, decay_lambda, sparsity_param, beta, patches), 
    method="L-BFGS-B", 
    jac=True,
    options={"maxiter":400,"disp":True})

"""**STEP 5:** Visualization"""

W1 = res.x[0:hidden_size * visible_size].reshape(visible_size, hidden_size)
display_network(W1.T, 5)

