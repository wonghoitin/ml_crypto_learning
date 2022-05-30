#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math


# In[2]:


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
    while not mailler_rabin(p,s):
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
    x,y,gcd = exgcd(b, a%b)
    return y, x - a//b * y, gcd

def get_inv(a, b):
    x, y, gcd = exgcd(a, b)
    if gcd == 1:
        return (x%b + b) %b
    else:
        print("No inverse facotr")
        return None
    
def rsa_init(range1, range2, s):
    if range1 < 10**16 or range2 < 10**16:
        print("Please input larger range")
        return None
    p = prime_gen(range1, range2, s)
    q = prime_gen(range1, range2, s)
    n = p*q
    euler_n = (p-1)*(q-1)
    e = random.randint(10**2, 10**5)
    while not relative_prime(e, euler_n):
        e = random.randint(10**2, 10**5)
    d = get_inv(e, euler_n)
    private_key = (d, n)
    public_key = (e, n)
    return private_key, public_key

def rsa_gen(range1, range2, s, pad):
    private, public = rsa_init(range1, range2, s)
    private_bit, public_bit = convert_rsa_to_bit(private, public, pad)
    return private_bit, public_bit

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

def convert_rsa_to_bit(rsa_private, rsa_public, length):
    rsa_private_bit = tuple([convert_to_bit(i, length) for i in rsa_private])
    rsa_public_bit = tuple([convert_to_bit(i, length) for i in rsa_public])
    return rsa_private_bit, rsa_public_bit

def run_back(m):
    longbit = str(m[0])
    for i in range(len(m)-1):
        longbit = longbit + str(m[i+1])
    return int(longbit, 2)

def full_run_back(full_m, pad):
    result = []
    for i in range(int(len(full_m)/pad)):
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
    for i in range(int(total_pad/pad)):
        k.append(
            convert_to_bit((
                random.randint(0,128)),
            pad))
    k = [a for b in k for a in b]
    return k

def rsa_cbc_init(string, rsa_public_bit):
    rsa_public = (run_back(rsa_public_bit[0]), run_back(rsa_public_bit[1]))
    sk = rsa_public_bit[0]
    iv = get_key(total_pad = len(sk), pad = len(sk))
    c_list = []
    m = convert_bin(string, len(sk))
    for i in range(int(len(m)/len(sk))):
        if i == 0:
            c_list.append(
                convert_to_bit(
                    pow(run_back(get_xor(m[:len(sk)], 
                                               iv, len(sk))), rsa_public[0], rsa_public[1]), len(sk)))
            continue
        c_list.append(
            convert_to_bit(
                pow(run_back(get_xor(m[i*len(sk):(i+1)*len(sk)], 
                                               c_list[-1], len(sk))), rsa_public[0], rsa_public[1]), len(sk)))
    c_list = [a for b in c_list for a in b]
    return c_list, iv

def rsa_cbc_decrypt(c_list, rsa_private_bit, iv):
    rsa_private = (run_back(rsa_private_bit[0]), run_back(rsa_private_bit[1]))
    sk = rsa_private_bit[0]
    ans = []
    for i in range(int(len(c_list)/len(sk))):
        if i == 0:
            ans.append(get_xor(convert_to_bit(
                pow(run_back(c_list[i*len(sk):(i+1)*len(sk)]), rsa_private[0], rsa_private[1]), len(sk)), iv, len(sk)))
            continue
        ans.append(get_xor(convert_to_bit(
                pow(run_back(c_list[i*len(sk):(i+1)*len(sk)]), rsa_private[0], rsa_private[1]), len(sk))
                           , c_list[(i-1)*len(sk):i*len(sk)], len(sk)))
    ans = [a for b in ans for a in b]
    return ans

