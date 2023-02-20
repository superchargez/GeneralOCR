# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:31:35 2023

@author: PTCL
"""
# import numpy.random.randint as randint
import numpy as np
import random, string
from string import digits
extension = [".com", ".net", ".net.pk", ".org", ".edu", ".edu.pk"]
probas = [0.4, 0.3, 0.2, 0.08, 0.019, .001]
organization = ["@gmail", "@ptcl", "@uet"]
alphabets = "a quick brown fox jummped over a lazy dog _ 012345679 - "
sorted_alphabets = sorted(alphabets.replace(" ", ""))
strings = sorted("".join(ch for ch in
    alphabets.translate(alphabets.maketrans("", "", digits))
    if ch.isalnum()))

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

# import uuid
# print(uuid.uuid4())

# =============================================================================
# import os
# os.urandom(15)
# 
# =============================================================================
# print(np.random.choice(extension, p = probas))

def random_email_gen():
    alpha = sorted_alphabets
    id = ''
    email_len = int(np.random.rand()*20)
    for i in range(5,20):
        id += np.random.choice(alpha)
        if len(id) > email_len: break
    id += np.random.choice(organization)
    id += np.random.choice(extension)
    # print(id)
    return id
#%%
def random_name_gen():
    # strings = "".join(ch for ch in alphabets.translate(alphabets.maketrans("", "", digits)) if ch.isalnum())
    # strings = sorted("".join(ch for ch in
    # alphabets.translate(alphabets.maketrans("", "", digits))
    # if ch.isalnum()))
    first_name = ''
    first_name_len = int(np.random.rand()*10)
    for i in range(5,10):
        first_name += np.random.choice(strings)
        if len(first_name) > first_name_len: break
    last_name = ''
    last_name_len = int(np.random.rand()*10)
    for i in range(5,10):
        last_name += np.random.choice(strings)
        if len(last_name) > last_name_len: break
    user_name = first_name + " "+ last_name
    return user_name
#%% 

def random_cnic_gen():
    cnic = ""
    # cnic += str(np.random.randint(1,10))
    # cnic += '-'
    for i in range(5):
        cnic += str(np.random.randint(1,10))
    cnic += '-'
    for i in range(7):
        cnic += str(np.random.randint(1,10))
    cnic += '-'
    cnic += str(np.random.randint(1,10))
    # print(cnic)
    return cnic

def random_oderID_gen():
    orderID = ""
    orderID += str(np.random.randint(1,10))
    orderID += '-'
    for i in range(12):
        orderID += str(np.random.randint(1,10))
    # print(orderID)
    return orderID

def random_phone_gen():
    phone = "03"
    for i in range(2):
        phone += str(np.random.randint(1,10))
    phone += '-'
    for i in range(7):
        phone += str(np.random.randint(1,10))
    # print(phone)
    return phone

def gen_texts():
    return random_email_gen(), random_name_gen(), random_cnic_gen(), random_phone_gen(), random_oderID_gen()
    

# for i in range(10):
#     random_email_gen(10)
# =============================================================================
# def gen_texts(n):
#     texts = []
#     for i in range(n):
#         # random_email_gen(15)
#         # random_name_gen(15, 15)
#         # random_cnic_gen(5, 7)
#         # random_oderID_gen(12)
#         # random_phone_gen(7)
#         # texts.append([random_email_gen(10), random_name_gen(), random_cnic_gen(), random_oderID_gen(), random_phone_gen()])
#     return texts
# 
# =============================================================================
# gen_texts(1)[0][1][1]
# np.savetxt('data.csv', ("email", "name", "cnic", "orderID", "phone"), delimiter=',')
