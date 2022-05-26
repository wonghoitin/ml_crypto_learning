#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random


# In[2]:


def get_inverse(value, max_value):
    for i in range(1, max_value):
        if (i * value) % max_value == 1:
            return i
    return -1

def gcd_x_y(x, y):
    if y == 0:
        return x
    else:
        return gcd_x_y(y, x% y)
def calculate_p_q(x1, y1, x2, y2, a, p):
    flag = 1
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a
        denominator = 2 * y1
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)
        
    gcd_value = gcd_x_y(member, denominator)
    member = member// gcd_value
    denominator = denominator // gcd_value
    inverse = get_inverse(denominator, p)
    k = (member * inverse)
    if flag == 0:
        k = -k
    k = k%p
    x3 = (k ** 2 - x1 - x2)%p
    y3 = (k * (x1 - x3) - y1) %p
    return [x3, y3]

def get_order(x0, y0, a, b, p):
    x1 = x0
    y1 = (-1 * y0) %p
    temp_x = x0
    temp_y = y0
    n = 1
    while True:
        n += 1
        p_value = calculate_p_q(temp_x, temp_y, x0, y0, a, p)
        if p_value[0] == x1 and p_value[1] == y1:
            return n+1
        temp_x = p_value[0]
        temp_y = p_value[1]

def get_x0_y0_x1_y1(x0, a, b, p):
    y0 = -1
    for i in range(0, p):
        if i**2 %p == (x0**3 + a*x0 + b)%p:
            y0 = i
            break
    if y0 == -1:
        return False
    x1 = x0
    y1 = -1 * y0 %p
    return [x0, y0, x1, y1]

def draw_graph(a, b, p):
    x_y = []
    for i in range(p):
        x_y.append(["-" for i in range(p)])
    for i in range(p):
        value = get_x0_y0_x1_y1(i, a, b, p)
        if value != False:
            x0 = value[0]
            y0 = value[1]
            x1 = value[2]
            y1 = value[3]
            x_y[x0][y0] = 1
            x_y[x1][y1] = 1
    print("the graph is presented:")
    for j in range(p):
        if p - 1 - j >= 10:
            print(p - 1 - j, end = " ")
        else:
            print(p - 1 - j, end = " ")
        for i in range(p):
            print(x_y[i][p - j - 1], end = " ")
        print()
    print("  ", end = "")
    for i in range(p):
        if i >= 10:
            print(i, end = " ")
        else:
            print(i, end = " ")
    print()
    
def point_list(a, b, p):
    return [(x, y) for x in range(p) for y in range(p) if (y**2 - (x**3 + a*x + b)) % p == 0]

def calculate_np(G_x, G_y, private_key, a, p):
    temp_x = G_x
    temp_y = G_y
    while private_key != 1:
        p_value = calculate_p_q(temp_x, temp_y, G_x, G_y, a, p)
        temp_x = p_value[0]
        temp_y = p_value[1]
        private_key -= 1
    return p_value

def ecc_init(a, b, p, private):
    if (4 * (a ** 3) + 27 * (b ** 2)) % p ==0:
        print("please input again")
        return None
    else:
        points = point_list(a, b, p)
        g = random.choice(points)
        q = calculate_np(g[0], g[1], private, a, p)
        order = get_order(g[0], g[1], a, b, p)
        print(
            "public_key: a = {}, b = {}, p = {}, G({}, {}), Q({}, {}), order = {}".format(
                a, b, p, g[0], g[1], q[0], q[1], order)
        )
        return a, b, p, g[0], g[1], q[0], q[1], order, private

def ecc_encrypt(a, p, G_x, G_y, Q_x, Q_y, integer, message):
    k_G = calculate_np(G_x, G_y, integer, a, p)
    k_Q = calculate_np(Q_x, Q_y, integer, a, p)
    cipher = message * k_Q[0]
    C = [k_G[0], k_G[1], cipher]
    print("cipher: ({}, {}), {}".format(C[0], C[1], C[2]))
    return C, k_G, k_Q
    
def ecc_decrypt(C0, C1, C2, private_key, a, p):
    decrypted = calculate_np(C0, C1, private_key, a, p)
    inverse = decrypted[0]**-1
    m = C2 * inverse
    print("message: {}".format(m))
    return m
