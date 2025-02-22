import csv
from tabulate import tabulate
from itertools import product
from re import findall
import pandas as pd

group_data = None

def convert_to_table(A,B, csv_filename):    # FIXME: Broken
    '''
    Tabulates `csv_filename` by sorting through all data with (A,B) in the index
    and places p values as rows and k values as columns
    (corresponding to the fixed elliptic equation y^2 = x^3 + Ax + B)
    '''

    # Collect all data entries beginning with (a,b)
    data_dict = {}
    p_values, k_values = [], []
    

    with open(csv_filename, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            (a,b,p,k), group_string = map(int, row[:4]), row[4]
            if (a,b) == (A,B):
                data_dict[(p,k)] = group_string
                if p not in p_values:
                    p_values.append(p)
                if k not in k_values:
                    k_values.append(k)
                
    p_values.sort()
    k_values.sort()

    header = [''] + k_values
    table = []
    for p in p_values:
        row = [p] + [data_dict.get((p,k), '') for k in k_values]
        table.append(row)

    return tabulate(table, headers=header)

def create_file(content_string, filename):
    with open(filename, 'w') as f:
        f.write(content_string)


def parse_group_string(s):
    return tuple(map(int, findall(r'\d+', s)))


def load_data_keys(data_filename):
    # FIXME: Might be unnecessary/slow. Consider using load_data
    data_keys = set()

    with open(data_filename, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            a,b,p,k = map(int, row[:4])
            data_keys.add((a,b,p,k))
    
    return data_keys

def get_group_structure(a,b,p,k, file_path='data.csv'):
    df = load_data(file_path)
    group_structure = df.loc[
        (df['a'] == a) &
        (df['b'] == b) &
        (df['p'] == p) &
        (df['k'] == k)
    ]['group_struc_1','group_struc_2'].values
    return group_structure[0]


def load_data(file_path):
    global group_data
    if group_data is None:
        group_data = pd.read_csv(
            file_path, 
            delimiter=',',
            names=['a','b','p','k','group_order','group_struc_1','group_struc_2'],
            # dtype={'a': int, 'b': int, 'p': int, 'group_order': int},
            quotechar="'",
            quoting=csv.QUOTE_MINIMAL
        )

    return group_data


def create_tables(a_range, b_range):
    '''
    a_range and b_range should be integer iterators
    '''
    for (a,b) in product(a_range, b_range):
        if (a,b) != 0:
            create_file(convert_to_table(a,b, data_path), f'tables/({a},{b})-table.txt')



if __name__ == '__main__':
    # convert_to_table(1,0,'data_test.csv')

    data_path = 'data.csv'
    data = load_data(data_path)
    print(data['group_structure'])


