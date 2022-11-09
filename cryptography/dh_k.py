#!/usr/bin/env python
# coding: utf-8

# In[32]:


import random


# In[33]:


def mailler_rabin(p, s):
    if p ==2:
        return True
    if p%2 == 0 or p ==1:
        return False
    a = p-1
    b = 0
    while a%2 ==0:
        a =a >>1
    for ind1 in range(s):
        b = pow(random.randint(2,p-1), a, p)
        if b == 1 or b == p-1:
            continue
        for ind2 in range(b):
            b = pow(b, 2, p)
            if b == p-1:
                break
            else:
                return False
    return True

def large_prime_gen(range1, range2, s):
    p = random.randint(range1, range2)
    while not mailler_rabin(p,s):
        p = random.randint(range1, range2)
    return p

def is_primitive_root(r, p, s):
    sec = set()
    if p <= s*4:
        print("Please check your input")
        return None
    a = [random.randrange(1, p) for ind in range(s*4)] 
    for i in a:
        t = pow(r, i, p)
        if t in sec:
            return False
        sec.add(t)
    return True

def cal_mod(a, x, p):
    return pow(a, x, p)

def dh_init(range1, range2, s = 32, kind = "small"):
    if kind == "small":
        while True:
            p = random.randint(range1, range2)
            shell = []
            for i in range(p):
                if p % (i+1) == 0:
                    shell.append(i+1)
            if len(shell) == 2:
                break
        while True:
            r = random.randint(1,p-1)
            if is_primitive_root(r, p, s):
                break
        print("The primitive root is {} \nand the prime number is {}".format(r,p))
        return r, p
    elif kind == 'large':
        p = large_prime_gen(range1,range2,s)
        while True:
            r = random.randint(1,p-1)
            if is_primitive_root(r, p, s):
                break
        print("The primitive root is {} \nand the prime number is {}".format(r,p))
        return r, p

def client_a_1(range1, range2, XA, kind = "small", s = 32):
    a, p = dh_init(range1, range2, kind = kind, s = s)
    YA = cal_mod(a, XA, p)
    print("Now send public_key_a = {}, primitive_root = {} and prime_number = {} to client_b".format(YA, a, p))
    return YA, a, p

def client_b_1(a, XB, p):
    YB = cal_mod(a, XB, p)
    print("Now send public_key_b = {} to client_a".format(YB))
    return YB

def client_a_2(y, x, p):
    common_key = cal_mod(y, x, p)
    print("The common secret key is {}".format(common_key))
    return common_key

def client_b_2(y, x, p):
    common_key = cal_mod(y, x, p)
    print("The common secret key is {}".format(common_key))
    return common_key

