#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# In[2]:


data = datasets.load_iris()["data"]
target = datasets.load_iris()["target"]


# In[3]:


ss = StandardScaler()
data = ss.fit_transform(data)


# In[4]:


onehot = []
for i in target:
    if i == 0:
        onehot.append([1, 0, 0])
    elif i == 1:
        onehot.append([0, 1, 0])
    else:
        onehot.append([0, 0, 1])
target = np.array(onehot)


# In[5]:


train_x, test_x, train_y, test_y = train_test_split(data, target, test_size= 0.2)


# In[6]:


neural_in = 4
neural_mid = 25
neural_out = 3
wb_width = 0.1
eta = 0.01
epoch = 250
batch_size = 8
interval = 10


# In[7]:


class BaseLayer:
    def __init__(self, n_upper, n):
        self.w = wb_width*np.random.randn(n_upper, n)
        self.b = wb_width*np.random.randn(n)
    def update(self, eta):
        self.w -= eta*self.grad_w
        self.b -= eta*self.grad_b
        
class MiddleLayer(BaseLayer):
    def forward(self, x):
        self.x = x
        self.u = np.dot(x, self.w) + self.b
        self.y = np.where(self.u <= 0, 0, self.u)
    def backward(self, grad_y):
        delta = grad_y *np.where(self.u <= 0, 0, 1)
        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis = 0)
        self.grad_x = np.dot(delta, self.w.T)
        
class OutputLayer(BaseLayer):
    def forward(self, x):
        self.x = x
        u = np.dot(x, self.w) + self.b
        self.y = np.exp(u)/np.sum(np.exp(u), axis = 1, keepdims = True)
    def backward(self, t):
        delta = self.y - t
        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis = 0)
        self.grad_x = np.dot(delta, self.w.T)


# In[8]:


middle_1 = MiddleLayer(neural_in, neural_mid)
middle_2 = MiddleLayer(neural_mid, neural_mid)
output_layer = OutputLayer(neural_mid, neural_out)


# In[9]:


def forward_propagation(x):
    middle_1.forward(x)
    middle_2.forward(middle_1.y)
    output_layer.forward(middle_2.y)

def backward_propagation(t):
    output_layer.backward(t)
    middle_2.backward(output_layer.grad_x)
    middle_1.backward(middle_2.grad_x)

def update_wb():
    middle_1.update(eta)
    middle_2.update(eta)
    output_layer.update(eta)

def get_error(t, batch_size):
    return -np.sum(t*np.log(output_layer.y + 1e-7))/batch_size

train_x_error, train_y_error, test_x_error, test_y_error = [], [], [], []


# In[10]:


n_batch = len(train_x)//batch_size

for i in range(epoch):
    forward_propagation(train_x)
    error_train = get_error(train_y, len(train_x))
    forward_propagation(test_x)
    error_test = get_error(test_y, len(test_x))
    
    test_x_error.append(i)
    test_y_error.append(error_test)
    train_x_error.append(i)
    train_y_error.append(error_train)
    
    if i%interval == 0:
        print("Epoch: " + str(i) + "/" + str(epoch),
             "Error_train: " + str(error_train),
             "Error_test: " + str(error_test))
    
    index_random = np.arange(len(train_x))
    np.random.shuffle(index_random)
    
    for j in range(n_batch):
        
        mb_index = index_random[j*batch_size: (j+1)*batch_size]
        x = train_x[mb_index, :]
        t = train_y[mb_index, :]
        
        forward_propagation(x)
        backward_propagation(t)
        
        update_wb()
        
plt.plot(train_x_error, train_y_error, label = "Train")
plt.plot(test_x_error, test_y_error, label = "Test")
plt.xlabel("Epochs")
plt.ylabel("Error")
plt.show()

forward_propagation(train_x)
count_train = np.sum(np.argmax(output_layer.y,
                              axis = 1) == np.argmax(train_y, axis = 1))

forward_propagation(test_x)
count_test = np.sum(np.argmax(output_layer.y,
                             axis = 1) == np.argmax(test_y, axis = 1))
print("Training data set accuracy: " + str(count_train/len(train_x)*100) + "%")
print("Test data set accuracy: " + str(count_test/len(test_x)*100) + "%")
