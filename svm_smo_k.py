#!/usr/bin/env python
# coding: utf-8

# In[1]:
#This is modified from Peter Harrington's simplified smo algorithm for svm. 
#It's slower than Platt's version, but easier to implement and understand.

import pandas
import random
import sklearn
import numpy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sklearn.datasets



# In[2]:


def selectJrand(i, m):
    j = i
    while j == i:
        j = int(random.uniform(0, m))
    return j

def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

def smo_simple_core(x, y, C, toler, maxiter):
    mat_x = numpy.mat(x)
    mat_y = numpy.mat(y).transpose()
    b = 0
    m, n = numpy.shape(mat_x)
    alphas = numpy.mat(numpy.zeros((m, 1)))
    i = 0
    while (i < maxiter):
        alphapairschanged = 0
        for _ in range(m):
            fx_ = float(numpy.multiply(alphas, mat_y).T*(mat_x*mat_x[_, :].T)) + b
            E_ = fx_ - float(mat_y[_])
            if ((mat_y[_] * E_ < -toler) and (alphas[_] < C)) or ((mat_y[_] * E_ > toler) and (alphas[_] > 0)):
                j = selectJrand(_, m)
                fxj = float(numpy.multiply(alphas, mat_y).T*(mat_x*mat_x[j, :].T)) + b
                Ej = fxj - float(mat_y[j])
                alpha_old = alphas[_].copy()
                alphaJold = alphas[j].copy()
                if mat_y[_] != mat_y[j]:
                    L = max(0, alphas[j] - alphas[_])
                    H = min(C, C + alphas[j] - alphas[_])
                else:
                    L = max(0, alphas[j] + alphas[_] - C)
                    H = min(C, alphas[j] + alphas[_])
                if L == H:
                    continue
                eta = 2 * mat_x[_, :]* mat_x[j, :].T - mat_x[_, :]* mat_x[_, :].T - mat_x[j, :]* mat_x[j, :].T
                if eta >= 0:
                    continue
                alphas[j] -= mat_y[j]* (E_ - Ej)/ eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if (abs(alphas[j] - alphaJold) < 0.00001):
                    continue
                alphas[_] += mat_y[j] * mat_y[_] * (alphaJold - alphas[j])
                b1 = b - E_ - mat_y[_] * (alphas[_] - alpha_old) * mat_x[_, :] *mat_x[_, :].T 
                - mat_y[j] * (alphas[j] - alphaJold) * mat_x[_, :] * mat_x[j, :].T
                b2 = b - Ej - mat_y[_] * (alphas[_] - alpha_old) * mat_x[_, :] *mat_x[j, :].T
                - mat_y[j] * (alphas[j] - alpha_old) * mat_x[j, :] * mat_x[j, :].T
                if (0 < alphas[_]) and (C > alphas[_]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2)/2
                alphapairschanged = 0
        if alphapairschanged == 0:
            i += 1
        else:
            i = 0
    return b, alphas

def cal_w(alphas, x, y):
    mat_x = numpy.mat(x)
    mat_y = numpy.mat(y).transpose()
    m, n = numpy.shape(mat_x)
    w = numpy.zeros((n, 1))
    for i in range(m):
        w += numpy.multiply(alphas[i]*mat_y[i], mat_x[i, :].T)
    return w

def svm_pred_y(x, w, b): 
    pred_y = []
    for i in range(len(numpy.mat(x))):
        if (numpy.mat(x)[i]*numpy.mat(w) + b).sum() > 0:
            pred_y.append(1)
        else:
            pred_y.append(0)
    return pred_y

def svm_accuracy(pred_y, y):
    e = 0
    for i in range(len(pred_y)):
        if pred_y[i] != y[i]:
            e += 1
    return 1 - (e/len(pred_y))

def svm_confusion_mat(pred_y, y):
    tn, fn, fp, tp = 0, 0, 0, 0
    for i in range(len(pred_y)):
        if pred_y[i] == 0 and y[i] == 0:
            tn += 1
        elif pred_y[i] == 0 and y[i] == 1:
            fn += 1
        elif pred_y[i] == 1 and y[i] == 0:
            fp += 1
        elif pred_y[i] == 1 and y[i] == 1:
            tp += 1
    print("\t\t     predicted\n\t\t0\t\t1\nactual  0\t{}\t\t{}\n\t1\t{}\t\t{}".format(tn, fp, fn, tp))
    return tn, fn, fp, tp

def smo_simple(x, y, C, toler, maxiter):
    if 0 in y:
        y = y.map({0 : -1, 1 : 1})
    b, alphas = smo_simple_core(x, y, C, toler, maxiter)
    w = cal_w(alphas, x, y)
    return b, alphas, w 

