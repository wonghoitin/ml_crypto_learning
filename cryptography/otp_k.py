#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random


# In[17]:


class otp():
    
    def __init__(self, pad, m = 0, k = 0, c = 0):
        self.pad = pad
        self.m = m
        self.k = k
        self.c = c

    def convert_to_bit(self, n):
        result = []
        while n >0:
            if n%2 == 0:
                result = [0] + result
            else:
                result = [1] + result
            n = n//2
        while len(result) < self.pad:
            result = [0] + result
        return result

    def convert_bin(self, string):
        output = []
        for i in string:
            output = output + self.convert_to_bit(ord(i))
        return output

    def run_back(self, m):
        longbit = str(m[0])
        for i in range(len(m)-1):
            longbit = longbit + str(m[i+1])
        return int(longbit, 2)

    def full_run_back(self, full_m):
        result = []
        for i in range(len(full_m)//self.pad):
            result.append(self.run_back(full_m[i*self.pad:(i+1)*self.pad]))
        return result

    def get_xor(self, c1, c2):
        xor = []
        for i in range(len(self.m)):
            if c1[i] + c2[i] == 0:
                xor.append(0)
            elif c1[i] + c2[i] == 2:
                xor.append(0)
            elif c1[i] + c2[i] == 1:
                xor.append(1)
        return xor

    def get_key(self): 
        k = []
        for i in range(len(self.m)//self.pad):
            k.append(
                self.convert_to_bit((
                    random.randint(0,128))
                ))
        k = [a for b in k for a in b]
        return k
