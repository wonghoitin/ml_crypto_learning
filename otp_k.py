#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random


# In[17]:


def convert_to_bit(n, pad):
    result = []
    while n >0:
        if n%2 == 0:
            result = [0] + result
        else:
            result = [1] + result
        n = n//2
    while len(result) < pad:
        result = [0] + result
    return result

def convert_bin(string, pad):
    output = []
    for i in string:
        output = output + convert_to_bit(ord(i), pad)
    return output

def run_back(m):
    longbit = str(m[0])
    for i in range(len(m)-1):
        longbit = longbit + str(m[i+1])
    return int(longbit, 2)

def full_run_back(full_m, pad):
    result = []
    for i in range(len(full_m)//pad):
        result.append(run_back(full_m[i*pad:(i+1)*pad]))
    return result

def get_xor(c1,c2, total_pad):
    xor = []
    for i in range(total_pad):
        if c1[i] + c2[i] == 0:
            xor.append(0)
        elif c1[i] + c2[i] == 2:
            xor.append(0)
        elif c1[i] + c2[i] == 1:
            xor.append(1)
    return xor

def get_key(total_pad, pad):
    k = []
    for i in range(total_pad//pad):
        k.append(
            convert_to_bit((
                random.randint(0,128)),
            pad))
    k = [a for b in k for a in b]
    return k

