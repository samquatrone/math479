from sage.all import *
import csv
from itertools import product, islice
from tqdm import tqdm
from re import findall
import pandas as pd
import pprint

import data_processing


def get_group_structure(a,b,p,k, file_path='data.csv'):
    df = data_processing.load_data(file_path)
    group_structure = df.loc[
        (df['a'] == a) &
        (df['b'] == b) &
        (df['p'] == p) &
        (df['k'] == k)
    ]['group_structure'].values
    return group_structure[0]


def test_1():
    '''
    Test 1: 
    - Find all (a,b, 3, 1) that give Z/4
    - For each (a,b) generate a sequence up to some k:
        group(a,b,3,1), group(a,b,3,2), group(a,b,3,3), ..., group(a,b,3,k)
    - If sequence not in list, add sequence
    '''
    p = 3
    group_structure = '(4,)'
    df = data_processing.load_data('data.csv')

    ab_pairs = df[
            (df['p'] == 3) & (df['k'] == 1) & (df['group_structure'] == '(4,)')
        ][['a','b']].values

    # print(ab_pairs)

    sequences = []

    for a,b in ab_pairs:
        sequence = []
        for k in range(1,10):
            sequence.append(get_group_structure(a,b,3,k))
        
        if sequence not in sequences:
            sequences.append(sequence)  

    print(sequences)
    

def test_2():
    '''
    Test 2:
    For p=3: 
    - find all initial group structures (k=1)
    - for each initial group structure, repeat test 1.
    '''
    p=3
    df = data_processing.load_data('data.csv')

    p1_data = df[(df['p'] == p) & (df['k'] == 1)].groupby('group_structure')
    group_structure_data = {k: data_table for k, data_table in p1_data}

    sequence_data = {}

    for group_structure, data in group_structure_data.items():
        
        ab_pairs = data[['a','b']].values
        sequences = []
        for a,b in ab_pairs:
            sequence = []
            for k in range(1,10):
                sequence.append(get_group_structure(a,b,p,k))
            
            if sequence not in sequences:
                sequences.append(sequence)  

        sequence_data[group_structure] = sequences


    pprint.pp(sequence_data)


'''
Test 3:
For all p:
Repeat test 2.
'''
# Take data
df = data_processing.load_data('data.csv')
k_range = range(1,10)


'''
Final data structure:

sequence_data = {
    p1: {
        structure1: sequence_list,
        structure2: sequence_list,
        ...
    },
    p2: {
        structure1: sequence_list,
        structure2: sequence_list,
        ...
    },
    ...
}
'''


# groupby primes
data_dict = {p: p_table[p_table['k'] == 1].groupby('group_structure') for p,p_table in df.groupby('p')}

sequence_data = {}

for p, group_structures in data_dict.items():
    sequence_data[p] = {}
    for group_structure, data in group_structures:
        ab_pairs = data[['a','b']].values

        sequences = []
        witnesses = []
        for a,b in ab_pairs:
            sequence = []
            for k in k_range:
                sequence.append(get_group_structure(a,b,p,k))
            
            if sequence not in sequences:
                sequences.append(sequence) 
                witnesses.append((a,b,p,group_structure))
                if len(sequences) > 1:
                    print(witnesses) 


        sequence_data[p][group_structure] = sequences


# pprint.pp(sequence_data)



