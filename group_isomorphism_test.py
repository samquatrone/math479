import data_processing

'''
Conjecture:
If A = a + np, then E(A,b,p,k) = E(a,b,p,k)

Try to find counterexample in data:

Option 1:

    Find where:
    1. a mod p = A mod p
    2. group_a != group_A

    If this list is empty, the data supports the conjecture.

Option 2:

    groupby[a,b,p,k] would return a collection of singleton dataframes, so if we go mod_a, 
    then we will get groups which should be equivalent.

    1. df['a_mod_p'] = df.apply(...) 
    2. groupby[]

'''


df = data_processing.load_data()
df['a_mod_p'] = df.apply(lambda row: row['a'] % row['p'], axis=1)
# df['b_mod_p'] = df.apply(lambda row: row['a'] % row['b'], axis=1)

counterexamples = []

for (a_mod_p, b, p, k), mod_a_block in df.groupby(['a_mod_p','b','p','k']):
    groups = set(mod_a_block.apply(lambda row: (row['group_struc_1'], row['group_struc_2']), axis=1))
    if len(groups) != 1:
        counterexamples.append(groups)
        print(groups)


