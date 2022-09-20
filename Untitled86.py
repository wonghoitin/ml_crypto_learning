#!/usr/bin/env python
# coding: utf-8

# In[14]:


import warnings
warnings.filterwarnings("ignore")


# In[15]:


import argparse
import pickle
import numpy as np
from keras.models import Sequential, load_model
from keras.datasets import mnist
from keras.layers import Dense
from keras import optimizers, utils


# In[16]:


inputs, hiddens, outputs = 784, 100, 10
learning_rate = 0.01
epochs = 50
batch_size = 64


# In[36]:


data = np.load("mnist.npz")
train_images = data["x_train"]
train_labels = data["y_train"]
test_images = data["x_test"]
test_labels = data["y_test"]
train_images = train_images.reshape(-1, inputs).astype("float32")/255
train_labels = utils.to_categorical(train_labels, outputs)
test_images = test_images.reshape(-1, inputs).astype("float32")/255
test_labels = utils.to_categorical(test_labels, outputs)


# In[38]:


def mlp():
    model = Sequential()
    model.add(Dense(hiddens, activation = "sigmoid", input_shape = (inputs, )))
    model.add(Dense(outputs, activation = "sigmoid"))
    return model

def train():
    model = mlp()
    sgd = optimizers.Adam(lr = learning_rate)
    model.compile(optimizer = sgd, loss = "mean_squared_error")
    model.fit(train_images, train_labels, batch_size = batch_size, epochs = epochs)
    model.save('mlp_model.h5')

def predict():
    model = load_model("mlp_model.h5")
    error = model.evaluate(test_images, test_labels)
    print("accuracy:", 1 - error)


# In[39]:


train()


# In[ ]:




