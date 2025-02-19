from sage.all import *
import csv
from itertools import product, islice
from tqdm import tqdm
from re import findall
import pandas as pd

# Import from other files
import data_processing


def generate_range(a_range,b_range,p_range,k_range, data_filename):
    '''
    Generates data with ranges for each parameter given as a tuple such as a_range = (a_initial, a_final).

    Note that p values represent indices of prime numbers and should always begin with index of 1.
    Similarly, k should always be >= 1
    '''
    a_1, a_2 = a_range
    b_1, b_2 = b_range
    p_1, p_2 = p_range
    k_1, k_2 = k_range

    # Load keys of existing data to avoid redundant computations
    existing_data_keys = data_processing.load_data_keys(data_filename)

    with open(data_filename, 'a', newline='') as csvfile:  # FIXME: handle case where file doesn't exist
        datawriter = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)

        for a,b,p,k in tqdm(    # wrapper for progress bar
            product(
                range(a_1, a_2+1),
                range(b_1, b_2+1),
                islice(Primes(), p_1, p_2+1),   # FIXME: Use something with less overhead
                range(k_1, k_2+1)
            ), 
            total=(a_2-a_1+1)*(b_2-b_1+1)*(p_2-p_1+1)*(k_2-k_1+1)  # number of iterations
        ):
            # print((a,b,p,k), is_singular(a,b,p,k))
            if (a,b) == (0,0) or (a,b,p,k) in existing_data_keys or is_singular(a,b,p,k):
                continue
            
            try:    
                H = EllipticCurve(GF(p**k), [a,b])
                # FIXME: abelian_group() method not intended for large fields (must be factorable)
                group_string = H.abelian_group().short_name()
                group_order = H.order()
                data = (a,b,p,k, parse_group_string(group_string), group_order)
                datawriter.writerow(data)
            except Exception as e:
                pass
                # print(f'{(a,b,p,k)}:    {e}')


def parse_group_string(s):
    '''
    Takes in a group structure of the form `'Z/m + Z/n'` or `'Z/m'` and returns
    either `(m,n)` or `(m,)`, respectively.
    '''
    return tuple(map(int, findall(r'\d+', s)))

def is_singular(a,b,p,k):
    q = p**k
    return (4*a**3 + 27*b**2) % q == 0


def get_groups(it, data_path='data.csv', generate=False):
    '''
    Note: `it` should iterate all wanted (a,b,p,k) values.
    '''
    data = data_processing.load_data(data_path)
    for a,b,p,k in it:
        
        row = data[
            (data['a'] == a) &
            (data['b'] == b) &
            (data['p'] == p) &
            (data['k'] == k)
        ]
        print(data[row])
        # print(data.dtypes)
    # print(data == data_processing.group_data)





if __name__ == '__main__':
    a_range = (-5,5)
    b_range = (-5,5)
    p_range = (1,50)
    k_range = (1,10)

    # generate_data(a_range, b_range, p_range, k_range, 'data.csv')
    # get_groups([(1,0,3,1)])
    # data_processing.group_data.dtypes

    df = data_processing.load_data('data.csv')

    # Find all p's with isomorphic group structures.
    # Generate a sequence for each of these
    
    # primes = primes_first_n(10)[1:]

    sequences = set()
    # indices = list(product(primes_first_n(10)[1:], range(1,10)))

    initial_groups = {}
    p_sequences = {}

    # TODO: Either design a test which doesn't require observation and will just check if our condition is 
    #       ever violated, or design a test which will group all of the data/construct the sequences I want 
    #       to see in a way that the same sequences should be next to each other. Highlight discrepancies.

    # initial_groups[3] = list(set(df.loc[(df['p'] == 3) & (df['k'] == 1)]['group_structure'].values))
    # print(initial_groups[3])
    for d in df.groupby(['p']):
        print(d)

    for p in primes_first_n(10)[1:]:
        ''
        # Find all group structures where 'p'=p 'k'=1 (and a,b are anything)
        p_data = df.loc[(df['p'] == p) & (df['k'] == 1)]
        # print(p_data)

        # print(p_data)

        # initial_groups[p] = list(set(df.loc[(df['p'] == p) & (df['k'] == 1)]['group_structure'].values))
        for k in range(1,11):
            # 
            ''



    
        

