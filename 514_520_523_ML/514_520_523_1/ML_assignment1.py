# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 16:09:50 2019

@author: Dhruv
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


path='seeddata.csv'
data=pd.read_csv(path, names = ["Area","Perimeter","Compactness","Length","Width","Assymetry","LengthOfKernel","Class"])


#set hyper parameters
alpha1 = 0.001
alpha2 = 0.0001
alpha3 = 0.00001
iters = 1000

data_normalized = (data - data.mean())/data.std()
data_normalized.head()

#setting the matrices
def make_matrix(data):
    X = data.iloc[:,0:7]
    ones = np.ones([X.shape[0],1])
    X = np.concatenate((ones,X),axis=1)
    
    y = data.iloc[:,7:8].values #.values converts it from pandas.core.frame.DataFrame to numpy.ndarray
    theta = np.zeros([1,8])
    
    return X,y,theta

def computeCost(X,y,theta):
    tobesummed = np.power(((X @ theta.T)-y),2)
    return np.sum(tobesummed)/(2 * len(X))

def gradientDescent(X,y,theta,iters,alpha):
    cost = np.zeros(iters)
    for i in range(iters):
        theta = theta - (alpha/len(X)) * np.sum(X * (X @ theta.T - y), axis=0)
        cost[i] = computeCost(X, y, theta)
    return theta,cost

def plot(iters,cost,alpha):
    fig, ax = plt.subplots()  
    ax.plot(np.arange(iters), cost, 'r')  
    ax.set_xlabel('Iterations')  
    ax.set_ylabel('Cost')  
    ax.set_title('For alpha = %f' %(alpha))

X,y,theta = make_matrix(data)
X1,y1,theta1 = make_matrix(data_normalized)


def driver(X,y,theta,iters,alpha):
    g,cost = gradientDescent(X,y,theta,iters,alpha)
    finalCost = computeCost(X,y,g)
    print("final cost without splitting for alpha =",alpha,": ",finalCost)
    plot(iters,cost,alpha)

#without normalization    
driver(X,y,theta,iters,alpha1)
driver(X,y,theta,iters,alpha2)
driver(X,y,theta,iters,alpha3)


#with normalization
print("After normalization:")
driver(X1,y1,theta1,iters,alpha1)

#First Fold
data1_train = data.drop(data.index[0:42])
data1_test = data.iloc[0:42]
X1,y1,theta1= make_matrix(data1_train)
X1_ts,y1_ts,theta1_ts=make_matrix(data1_test)
g1,cost1=gradientDescent(X1,y1,theta1,iters,alpha1)
f1=computeCost(X1_ts,y1_ts,g1)
print("final cost with 1st Split: ",f1)

#Second Fold
data2_train = data.drop(data.index[42:84])
data2_test = data.iloc[42:84]
X2,y2,theta2= make_matrix(data2_train)
X2_ts,y2_ts,thet2_ts=make_matrix(data2_test)
g2,cost2=gradientDescent(X2,y2,theta2,iters,alpha1)
f2=computeCost(X2_ts,y2_ts,g2)
print("final cost with 2nd Split: ",f2)

#Third Fold
data3_train = data.drop(data.index[84:126])
data3_test = data.iloc[84:126]
X3,y3,theta3= make_matrix(data3_train)
X3_ts,y3_ts,theta3_ts=make_matrix(data3_test)
g3,cost3=gradientDescent(X3,y3,theta3,iters,alpha1)
f3=computeCost(X3_ts,y3_ts,g3)
print("final cost with 3rd Split: ",f3)

#Fourth Fold
data4_train = data.drop(data.index[126:168])
data4_test = data.iloc[126:168]
X4,y4,theta4= make_matrix(data4_train)
X4_ts,y4_ts,theta4_ts=make_matrix(data4_test)
g4,cost4=gradientDescent(X4,y4,theta4,iters,alpha1)
f4=computeCost(X4_ts,y4_ts,g4)
print("final cost with 4th Split: ",f4)

#Fifth Fold
data5_train = data.drop(data.index[168:210])
data5_test = data.iloc[168:210]
X5,y5,theta5= make_matrix(data5_train)
X5_ts,y5_ts,theta5_ts=make_matrix(data5_test)
g5,cost5=gradientDescent(X5,y5,theta5,iters,alpha1)
f5=computeCost(X5_ts,y5_ts,g5)
print("final cost with 5th Split: ",f5)




