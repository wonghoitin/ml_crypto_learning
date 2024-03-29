#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

#cn_pow(10, 13, (11, 7)) is equivalent to pow(10, 13, 77), but faster
def cn_pow(a, b, pq):
    euler = [pq[0] - 1, pq[1] - 1]
    temp = [0, 0]
    for i in range(len(temp)):
        if b % euler[i] == 0:
            temp[i] = (a**euler[i]) % pq[i]
        else:
            temp[i] = (a**(b % euler[i])) % pq[i]
    m_1_inv = get_inv(pq[1], pq[0])
    m_2_inv = get_inv(pq[0], pq[1])
    x = (temp[0] * pq[1] * m_1_inv + temp[1] * pq[0] * m_2_inv) % (pq[0]*pq[1])
    return x

