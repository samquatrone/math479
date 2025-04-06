import data_processing
import numpy as np
from sympy import gcd
import pandas as pd
import pprint


'''
Question:
For a given (a,b), for which prime numbers p is group(a,b,p,1) of the form Z/n + Z/n?
'''
df = data_processing.load_data()


# Abstract groups/conditions

def is_group_square(row):
    return row['group_struc_1'] == row['group_struc_2']


def is_group_struc_equal(row, group_struc_1, group_struc_2):
    return row['group_struc_1'] == group_struc_1 and row['group_struc_2'] == group_struc_2

def is_trivial_group(row):
    return is_group_struc_equal(row,1,1)


# (a, 0 mod p, p, 1) and p=n^2+1
def is_square_case_1(row):
    if (row['b'] % row['p']) != 0 or row['k'] != 1:  
        return False
    return row['p'] == (row['group_struc_1']**2 + 1)  
  
# (0 mod p, b, p, 1) and p=n^2+n+1, n^2-n+1
def is_square_case_2(row):
    if (row['a'] % row['p']) != 0 or row['k'] != 1:  
        return False
    n = row['group_struc_1']
    val_1 = n**2 + n + 1
    val_2 = n**2 - n + 1
    return row['p'] == val_1 or row['p'] == val_2

# Supersingular in even column
def is_square_case_3(row):
    is_even = (row['k'] % 2) == 0
    is_supersingular = (row['group_order'] % row['p']) == 1
    return is_even and is_supersingular

# 
def is_square_case_4(row):
    return (row['k'] == 3 and 
            (row['a'] % 7) == 0 and 
            is_group_struc_equal(row,18,18))

def is_square_case_5(row):
    return (row['k'] == 1 and 
            is_group_struc_equal(row,2,2) and 
            (row['a'] % row['p'] == 0 or row['b'] % row['p'] == 0))



# Conjecture: Square => one of the cases holds
square_df = df[df.apply(is_group_square, axis=1)]

# Is square, but none of the cases hold.
counter_examples = square_df[
        square_df.apply(lambda row: not any(
            [
                is_square_case_1(row), 
                is_square_case_2(row),
                is_square_case_3(row),
                is_square_case_4(row),
                is_square_case_5(row),
                is_trivial_group(row)
            ]
        ), axis=1)
    ]

print(counter_examples)

