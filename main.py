from sage.all import *
import csv
from itertools import product, islice
from tqdm import tqdm

# Import from other files
from data_processing import load_data_keys



a = 1
b = 0
max_k = 20
max_p = 100


# Load keys of existing data to avoid redundant computations
existing_data_keys = load_data_keys('data.csv')


with open('data.csv', 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',')

    # Generate elliptic curve data for a,b over the field GF(p^k) 
    #   for 1<=p<=max_p and 1<=k<=max_k
    for p, k in tqdm(product(islice(Primes(), 1, max_p+1), range(1,max_k+1)), total=max_k*max_p):
        if (a,b,p,k) not in existing_data_keys:
            H = EllipticCurve(GF(p**k), [a,b])
            data = (a,b,p,k, H.abelian_group().short_name())
            datawriter.writerow(data)
            # print('added data:', data)
        

