import data_processing
import pandas as pd
import pprint


'''
Question:
For a given (a,b), for which prime numbers p is group(a,b,p,1) of the form Z/n + Z/n?
'''

df = data_processing.load_data()

square_primes_dict = {}
square_orders_dict = {}

# TODO: to generalize for any k, change here:
for (a,b), ab_df in df[df['k'] == 1].groupby(['a','b']):    

    ab_df['group_struc_1'] = ab_df['group_struc_1'].apply(int)
    square_primes = list(ab_df.loc[(ab_df['group_struc_1'] == ab_df['group_struc_2'])]['p'].values)
    square_orders = list(ab_df.loc[(ab_df['group_struc_1'] == ab_df['group_struc_2'])]['group_order'].values)
    
    square_primes_dict[(a,b)] = square_primes
    square_orders_dict[(a,b)] = square_orders


pprint.pp(square_primes_dict)
# pprint.pp(square_orders_dict)

