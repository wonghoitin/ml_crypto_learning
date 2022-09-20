#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import argparse
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
from torch.utils.data import DataLoader


# In[2]:


inputs, hiddens, outputs = 784, 200, 10
learning_rate = 0.01
epochs = 50
batch_size = 64
transformation = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307, ),
                                    (0.3081,))])
train_set = datasets.MNIST("mnist/", train = True, transform = transformation, download = True)
train_loader = DataLoader(dataset = train_set, batch_size = batch_size, shuffle = True)
test_set = datasets.MNIST("mnist/", train = False, transform = transformation, download = True)
test_loader = DataLoader(dataset = test_set, batch_size = batch_size, shuffle = False)


# In[3]:


class mlp(nn.Module):
    def __init__(self):
        super(mlp, self).__init__()
        self.sigmoid = nn.Sigmoid()
        self.hidden_layer = nn.Linear(inputs, hiddens)
        self.output_layer = nn.Linear(hiddens, outputs)
    def forward(self, x):
        out = self.sigmoid(self.hidden_layer(x))
        out = self.sigmoid(self.output_layer(out))
        return out
    def name(self):
        return "mlp"

def train():
    model = mlp()
    loss = nn.MSELoss(reduction = "sum")
    optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
    for epoch in range(epochs):
        avg_error = 0
        for i, (images, labels) in enumerate(train_loader):
            images = Variable(images.view(-1, inputs))
            one_hot = torch.FloatTensor(labels.size(0), 10).zero_()
            target = one_hot.scatter_(1, labels.view((labels.size(0), 1)), 1)
            target = Variable(target)
            optimizer.zero_grad()
            out = model(images)
            error = loss(out, target)
            error.backward()
            optimizer.step()
            avg_error += error.item()
            
        avg_error /= train_loader.dataset.train_data.shape[0]
        print("Epoch [{}/{}, error: {}]".format(epoch+1, epochs, avg_error))
    torch.save(model.state_dict(), "model.pkl")

def predict():
    model = mlp()
    model.load_state_dict(torch.load("model.pkl"))
    correct, total = 0, 0
    for images, labels in test_loader:
        images = Variable(image.view(-1, inputs))
        out = model(images)
        _, predicted = torch.max(out.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum()
        print("accuracy: {}".format(100.0 * correct/total))


# In[4]:


train()

