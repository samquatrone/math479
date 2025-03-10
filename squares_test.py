import data_processing
import numpy as np
from sympy import gcd
import pandas as pd
import pprint


'''
Question:
For a given (a,b), for which prime numbers p is group(a,b,p,1) of the form Z/n + Z/n?
'''

def produce_square_primes(k=1):
    df = data_processing.load_data()

    square_primes_dict = {}
    square_orders_dict = {}

    # TODO: to generalize for any k, change here:
    for (a,b), ab_df in df[df['k'] == k].groupby(['a','b']):    

        ab_df['group_struc_1'] = ab_df['group_struc_1'].apply(int)
        square_primes = list(ab_df.loc[(ab_df['group_struc_1'] == ab_df['group_struc_2'])]['p'].values)
        square_orders = list(ab_df.loc[(ab_df['group_struc_1'] == ab_df['group_struc_2'])]['group_order'].values)
        
        square_primes_dict[(a,b)] = square_primes
        square_orders_dict[(a,b)] = square_orders


    pprint.pp(square_primes_dict)
# pprint.pp(square_orders_dict)

'''
It seems that this has something to do with supersingular curves, or when the size of group is 1 less than 
n^2 
'''
def find_a_scores():
    df = data_processing.load_data()

    # find where group_order = p^k + 1
    # find where group_order = p^k - 1

    # df['a_score'] = df.apply(lambda row: (row['p']**row['k'] + 1 - int(row['group_order'])) , axis=1)
    # df['mod_a_score'] = df.apply(lambda row: row['a_score'] % row['p'], axis=1)
    # df['max_a_score'] = df.apply(lambda row: int(np.floor(2*int(np.sqrt(float(row['p']**row['k']))))), axis=1)
    # df['min_a_score'] = df.apply(lambda row: int(np.ceil(-2*int(np.sqrt(float(row['p']**row['k']))))), axis=1)

    # min_a_score_rows = df[df.apply(lambda row: np.ceil(-2*int(np.sqrt(float(row['p']**row['k'])))), axis=1) == df['a_score']]

    # supersingular_rows = df[df['a_score'] == 0]
    # suprasingular_rows = df[
    #     (df['a_score'] == 2) & 
    #     (df['k'] == 1) & 
    #     ((df['a'] != 0) & df['b'] != 0) & 
    #     (df['group_struc_1'] == df['group_struc_2'])
    # ]

    counterexamples = df[
        (df['group_struc_1'] == df['group_struc_2']) &
        ((df['k'] != 1) | (df['b'] != 0) | (df['a_score'] != 2)) &
        ((df['k'].apply(lambda k: k % 2) == 1) | (df['mod_a_score'] != 0)) &
        (df['a'] != 0) 
        # ((df['a_score'] != df['min_a_score']) & (df['a_score'] != df['max_a_score']))
    ]

    # max_a_score_rows = df[df['a_score'] == df.apply(lambda row: np.floor(2*int(np.sqrt(float(row['p']**row['k'])))), axis=1 )]
    # case_1_failure_rows = df[(df.apply(lambda row: gcd(row['p'], row['a_score']), axis=1) != 1) & (df['a_score'] != 0)]
    print(counterexamples.to_string())

find_a_scores()


