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
            
            H = compute_group(a,b,p,k)
            if H is not None:
                group_structure_tuple = parse_group_string(H.abelian_group().short_name())
                group_structure_1 = group_structure_tuple[0] if len(group_structure_tuple) > 0 else 1
                group_structure_2 = group_structure_tuple[1] if len(group_structure_tuple) == 2 else 1
                group_order = H.order()
                
            data = (a,b,p,k, group_order, group_structure_1, group_structure_2)
            datawriter.writerow(data)



def compute_group(a,b,p,k):
    try:
        # FIXME: abelian_group() method not intended for large fields (must be reasonably factorable)
        return EllipticCurve(GF(p**k), [a,b])

    except Exception as e:
        return None

def parse_group_string(s):
    '''
    Takes in a group structure of the form `'Z/m + Z/n'` or `'Z/m'` and returns
    either `(m,n)` or `(m,)`, respectively.
    '''
    return tuple(map(int, findall(r'\d+', s)))

def is_singular(a,b,p,k):
    q = p**k
    return (4*a**3 + 27*b**2) % q == 0





if __name__ == '__main__':
    a_range = (-5,5)
    b_range = (-5,5)
    p_range = (1,50)
    k_range = (1,10)

    generate_range(a_range, b_range, p_range, k_range, 'data.csv')
 

    
        

