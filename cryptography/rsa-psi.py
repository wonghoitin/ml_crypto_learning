#!/usr/bin/env python
# coding: utf-8

# In[1]:


import hashlib
import random
from Crypto.PublicKey import RSA
import gmpy2


# In[2]:


def hash_(num):
    hash_result = hashlib.sha1(str(num).encode('utf-8')).hexdigest()
    return int(hash_result,16)

def rsa():
    key = RSA.generate(1024)
    pk = (key.e,key.n)
    sk = (key.d,key.n)
    return pk,sk


# In[3]:


def server1():
    pk, sk = rsa()
    print("Send the hash function and pk = {}, {} to client".format(pk[0], pk[1]))
    return pk, sk

def server2(c1,sk):
    c2 = []
    for i in c1:
        c2.append(gmpy2.powmod(i,sk[0],sk[1]))
    print("Send the decrypted but still hashed and blinded client data back to client")
    return c2

def server3(server_data,sk):
    s1 = []
    for i in server_data:
        hash_i = hash_(i)
        c_hash_i = gmpy2.powmod(hash_i,sk[0],sk[1])
        s1.append(hash_(c_hash_i))
    print("Send the double-hashed and encrypted server data to client")
    return s1


# In[4]:


def client1(client_data, pk):
    c1 = []
    r_list = [] 
    for i in client_data:
        hash_i = hash_(i) % pk[1]
        ra = random.randint(10**127, 10**128)
        c_ra = gmpy2.powmod(ra,pk[0],pk[1])
        r_list.append(ra)
        c1.append(hash_i*c_ra)
    print("Send the encrypted, hashed and blinded client data to server")
    return c1, r_list

def client2(c2, r_list, pk):
    c3 = []
    for i,ra in zip(c2,r_list):
        ra_inv = gmpy2.invert(ra,pk[1])
        c3.append(hash_((i * ra_inv) % pk[1]))
    return c3

def client3(c3, s1):
    return sorted(set(c3).intersection(s1), key = lambda x: c3.index(x))

