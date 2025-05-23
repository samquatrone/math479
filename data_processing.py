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

df = None
DATA_PATH = os.path.join(os.getcwd(), 'data')

def _group_parse_func(row):
    G_1,G_2 = row['group_struc_1'], row['group_struc_2']
    if G_1 == 1 and G_2 == 1:
        return "0"
    if G_2 == 1:
        return f"Z/{G_1}"
    return f"Z/{G_1} + Z/{G_2}"

def _group_string_format(G_1, G_2):
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


# def load_data_keys(data_filename):
#     # FIXME: Might be unnecessary/slow. Consider using load_data
#     data_keys = set()

#     with open(data_filename, newline='') as csvfile:
#         datareader = csv.reader(csvfile, delimiter=',')
#         for row in datareader:
#             a,b,p,k = map(int, row[:4])
#             data_keys.add((a,b,p,k))
    
#     return data_keys

def get_group(a,b,p,k, data_path=DATA_PATH):
    df = load_data(data_path)
    return _group_string_format(*df.loc[(a,b,p,k)][['group_struc_1','group_struc_2']])
    


def load_data(data_path=DATA_PATH):
    global df
    if df is None:
        data_files = [os.path.join(data_path, f) for f in os.listdir(data_path)]
        df_iter = (
            pd.read_csv(
                file_path, 
                delimiter=',',
                names=['a','b','p','k','group_order','group_struc_1','group_struc_2'],
                dtype={'a': int, 'b': int, 'p': int, 'k': int, 'group_order': str, 'group_struc_1': str, 'group_struc_2': str},
                quotechar="'",
                quoting=csv.QUOTE_MINIMAL,
            ) for file_path in data_files
        )
        
        df = pd.concat(df_iter, ignore_index=True)

        df['p'] = df['p'].apply(int)
        df['group_order'] = df['group_order'].apply(int)
        df['group_struc_1'] = df['group_struc_1'].apply(int)
        df['group_struc_2'] = df['group_struc_2'].apply(int)
        df.set_index(['a','b','p','k'], inplace=True)

    return df


def write_tables(option='txt'): # TODO: Add control (i.e. only write the (a,b) table etc.)
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
    data_file_path = DATA_PATH
    df = load_data()

    print(
        _group_string_format(*df.loc[(1,0,5,3)][['group_struc_1','group_struc_2']])
        )


