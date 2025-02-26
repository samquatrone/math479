import csv
import os
from itertools import product
from re import findall
import pandas as pd

'''
Note: pandas stores integers as their own int64 type, but since there are some 
large integers in the database (e.g. 'group_struc_1' contains very large integers),
these columns need to be converted to int before being read.


'''

group_data = None

def _group_parse_func(row):
    G_1,G_2 = row['group_struc_1'], row['group_struc_2']
    if G_1 == 1 and G_2 == 1:
        return "0"
    if G_2 == 1:
        return f"Z/{G_1}"
    return f"Z/{G_1} + Z/{G_2}"

def convert_to_table(A,B):
    '''
    Tabulates data indexed by (a,b) = (A,B)
    and places p values as rows and k values as columns
    (corresponding to the fixed elliptic equation y^2 = x^3 + Ax + B)
    '''
    df = load_data()
    ab_rows: pd.DataFrame = df.loc[(df['a'] == A) & (df['b'] == B)][['p','k','group_struc_1','group_struc_2']]
    # group_parse_func = lambda row: f"Z/{row['group_struc_1']}" if row['group_struc_2'] == 1 else f"Z/{row['group_struc_1']} + Z/{row['group_struc_2']}"
    ab_rows['group_structure'] = df.apply(_group_parse_func, axis=1)

    return ab_rows.pivot(index='p', columns='k', values='group_structure')


def create_file(content_string, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
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
    ][['group_struc_1','group_struc_2']].values
    return group_structure[0]


def load_data(file_path='data.csv'):
    global group_data
    if group_data is None:
        group_data = pd.read_csv(
            file_path, 
            delimiter=',',
            names=['a','b','p','k','group_order','group_struc_1','group_struc_2'],
            # dtype={'group_struc_1': int},
            quotechar="'",
            quoting=csv.QUOTE_MINIMAL
        )

    return group_data


def write_tables(option='txt'):
    '''
    a_range and b_range should be integer iterators
    '''
    df = load_data()
    ab_pairs = list(set(map(lambda x: tuple(x), df[['a','b']].values)))
    match(option):
        case 'txt':
            for a,b in ab_pairs:
                create_file(convert_to_table(a,b).to_string(), f'tables/txt/({a},{b})-table.txt')
        case 'html':
            for a,b in ab_pairs:
                convert_to_table(a,b).to_html(f'tables/html/({a},{b})-table.html')



if __name__ == '__main__':
    data_file_path = 'data.csv'
    df = load_data()

    write_tables()
    # print(convert_to_table(0,1))
    # print(get_group_structure(0,1,3,4))



