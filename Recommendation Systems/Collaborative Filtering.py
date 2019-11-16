# -*- coding: utf-8 -*-
"""
CS 351 - Artificial Intelligence 
Assignment 3

Student ID = XXXXXXXXXXXXXXXXX
"""

import numpy as np
import matplotlib.pyplot as plt

"""This function takes actual and predicted ratings and compute total mean square error(mse) in observed ratings.
"""
def computeError(R,predR):
    error = 0
    x_r, y_r = R.nonzero()
    for x,y in zip(x_r,y_r):
        error += pow(R[x, y] - predR[x, y],2)
    return error/len(x_r)


"""
This fucntion takes P (m*k) and Q(k*n) matrices alongwith user bias (U) and item bias (I) and returns predicted rating. 
where m = No of Users, n = No of items
"""
def getPredictedRatings(P,Q,U,I):

    """Your code to predict ratinngs goes here"""
    # Ri = bi + bj + (Pi Qj)
    i_range = P.shape[0]
    j_range = Q.shape[1]
    predicted = np.zeros((i_range, j_range))
    for i in range (i_range):
        for j in range (j_range):
            predicted[i][j] = U[i] + I[j] + P[i, :].dot(Q[:, j])
    return predicted
    
    
"""This fucntion runs gradient descent to minimze error in ratings by adjusting P, Q, U and I matrices based on gradients.
   The functions returns a list of (iter,mse) tuple that lists mse in each iteration
"""
def runGradientDescent(R,P,Q,U,I,iterations,alpha):
    stats = []
    for iter in range(iterations):
        predR = getPredictedRatings(P, Q, U, I)
        mse = computeError(R, predR)
        stats.append((iter, mse))
        eij = np.subtract(R, predR)
        for i in range(eij.shape[0]):
            for j in range(eij.shape[1]):
                if R[i,j] == 0:
                    continue
                #updating U
                U[i]-= alpha * 2 * eij[i][j]
                I[j]-= alpha * 2 * eij[i][j]
                #make copy of P
                P_copy = P[:, :]
                #update P & Q
                #Pi' = P[i] + alpha * 2 * eij * Qj
                P[i, :] += alpha * 2 * eij[i][j] * Q[:, j]
                # Qj' = Q[j] + alpha * 2 * eij * Pi
                Q[:, j] += alpha * 2 * eij[i][j] * P_copy[i, :]
    return stats
    
""" 
This method applies matrix factorization to predict unobserved values in a rating matrix (R) using gradient descent.
K is number of latent variables and alpha is the learning rate to be used in gradient decent
"""    

def matrixFactorization(R,k,iterations, alpha):
    """Your code to initialize P, Q, U and I matrices goes here. P and Q will be randomly initialized whereas U and I will be initialized as zeros. 
    Be careful about the dimension of these matrices
    """
    users,items = R.shape
    P = np.random.rand(users,k)
    Q = np.random.rand(k,items)
    U = np.zeros(users)
    I = np.zeros(items)
    #runGradientDescent(R, P, Q, U, I, iterations, alpha)
    # computeError(R, predR)

    #Run gradient descent to minimize error
    stats = runGradientDescent(R,P,Q,U,I,iterations,alpha)

    print('P matrx:')
    print(P)
    print('Q matrix:')
    print(Q)
    print("User bias:")
    print(U)
    print("Item bias:")
    print(I)
    print("P x Q:")
    print(getPredictedRatings(P,Q,U,I))
    plotGraph(stats)


def plotGraph(stats):
    i = [i for i,e in stats]
    e = [e for i,e in stats]
    plt.plot(i,e)
    plt.xlabel("Iterations")
    plt.ylabel("Mean Square Error")
    plt.show()
    
""""
User Item rating matrix given ratings of 5 users for 6 items.
Note: If you want, you can change the underlying data structure and can work with starndard python lists instead of np arrays
We may test with different matrices with varying dimensions and number of latent factors. Make sure your code works fine in those cases.
"""
R = np.array([
[5, 3, 0, 1, 4, 5],
[1, 0, 2, 0, 0, 0],
[3, 1, 0, 5, 1, 3],
[2, 0, 0, 0, 2, 0],
[0, 1, 5, 2, 0, 0],
])

k = 3
alpha = 0.01
iterations = 500

matrixFactorization(R,k,iterations, alpha)
