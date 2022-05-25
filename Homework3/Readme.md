# Instructions
This file contains code that helps you get started on the programming assignment. You will need to complete the function sample_images(), sparse_auto_encoder(), and compute_numerical_gradient().

## Step 1
Implement sample_images()

After implementing sample_images(), the display_network() function should display a random sample of 100 patches from the dataset

## Step 2
Implement sparseAutoencoderCost

You can implement all of the components (squared error cost, weight decay term, sparsity penalty) in the cost function at once, but it may be easier to do it step-by-step and run gradient checking (see STEP 3) after each step. We suggest implementing the sparse_autoencoder_cost() function using the following steps:

Implement forward propagation in your neural network, and implement the squared error term of the cost function. Implement backpropagation to compute the derivatives. Then (using lambda=beta=0), run Gradient Checking to verify that the calculations corresponding to the squared error cost term are correct.

Add in the weight decay term (in both the cost function and the derivative calculations), then re-run Gradient Checking to verify correctness.

Add in the sparsity penalty term, then re-run Gradient Checking to verify correctness. Feel free to change the training settings when debugging your code. (For example, reducing the training set size or number of hidden units may make your code run faster; and setting beta and/or lambda to zero may be helpful for debugging.) However, in your final submission of the visualized weights, please use parameters we gave in Step 0 above.

## Step 3
Gradient Checking

Hint: If you are debugging your code, performing gradient checking on smaller models and smaller training sets (e.g., using only 10 training examples and 1-2 hidden units) may speed things up.

## Step 4
After verifying that your implementation of sparse_autoencoder_cost() is correct, You can start training your sparse autoencoder with scipy's minimize function (L-BFGS).

## Step 5 Visualization
