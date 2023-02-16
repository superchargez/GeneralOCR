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

def random_email_gen(length):
    alpha = sorted_alphabets
    id = ''
    for i in range(0,length):
        id += np.random.choice(alpha)
    id += np.random.choice(organization)
    id += np.random.choice(extension)
    print(id)
    return id

def random_name_gen(first_len, last_len):
    # strings = "".join(ch for ch in alphabets.translate(alphabets.maketrans("", "", digits)) if ch.isalnum())
    # strings = sorted("".join(ch for ch in
    # alphabets.translate(alphabets.maketrans("", "", digits))
    # if ch.isalnum()))
    first_name = ''
    for i in range(5,np.random.randint(first_len)):
        first_name += np.random.choice(strings)
    last_name = ''
    for i in range(5, np.random.randint(last_len)):
        last_name += np.random.choice(strings)
    print(first_name, last_name)
    user_name = first_name + " "+ last_name
    return user_name
    

def random_cnic_gen(m,l):
    cnic = ""
    cnic += str(np.random.randint(1,10))
    cnic += '-'
    for i in range(m):
        cnic += str(np.random.randint(1,10))
    cnic += '-'
    for i in range(l):
        cnic += str(np.random.randint(1,10))
    cnic += '-'
    cnic += str(np.random.randint(1,10))
    print(cnic)
    return cnic

def random_oderID_gen(n):
    orderID = ""
    orderID += str(np.random.randint(1,10))
    orderID += '-'
    for i in range(n):
        orderID += str(np.random.randint(1,10))
    print(orderID)
    return orderID

def random_phone_gen(n):
    phone = "03"
    for i in range(2):
        phone += str(np.random.randint(1,10))
    phone += '-'
    for i in range(n):
        phone += str(np.random.randint(1,10))
    print(phone)
    return phone

# for i in range(10):
#     random_email_gen(10)
random_email_gen(15)
random_name_gen(15, 15)
random_cnic_gen(5, 7)
random_oderID_gen(12)
random_phone_gen(7)
