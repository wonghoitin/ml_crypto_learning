#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math


# In[2]:


class rsa():
    
    def __init__(self, p, q, n, e, d):
        self.p = p
        self.q = q
        self.n = n
        self.e = e
        self.d = d

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

    def prime_gen(range1, range2, s):
        p = random.randint(range1, range2)
        while not rsa.mailler_rabin(p,s):
            p = random.randint(range1, range2)
        return p

    def relative_prime(m,n):
        u, v = 0, 0
        if n == 0:
            u = 1
            v = 0
            return (m,u,v)    
        a1 = b = 1
        a = b1 = 0
        c = m
        d = n
        q = c // d
        r = c % d
        while r:
            c = d
            d = r
            t = a1
            a1 = a
            a = t - q * a
            t = b1
            b1 = b
            b = t - q * b
            q = c // d
            r = c % d
        u = a
        v = b
        if d == 1:
            return True
        else:
            return False

    def exgcd(a,b):
        if b == 0:
            return 1,0,a
        x,y,gcd = rsa.exgcd(b, a%b)
        return y, x - a//b * y, gcd

    def get_inv(a, b):
        x, y, gcd = rsa.exgcd(a, b)
        if gcd == 1:
            return (x%b + b) %b
        else:
            print("No inverse facotr")
            return None

    def rsa_init(range1, range2, s):
        if range1 < 10**16 or range2 < 10**16:
            print("Please input larger range")
            return None
        p = rsa.prime_gen(range1, range2, s)
        q = rsa.prime_gen(range1, range2, s)
        n = p*q
        euler_n = (p-1)*(q-1)
        e = random.randint(10**2, 10**5)
        while not rsa.relative_prime(e, euler_n):
            e = random.randint(10**2, 10**5)
        d = rsa.get_inv(e, euler_n)
        private_key = (d, n)
        public_key = (e, n)
        return private_key, public_key

