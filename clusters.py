import data_processing
import pprint

df = data_processing.load_data()
max_cluster = []
max_cluster_index = None
entangled_data = {}
associated_data = {}

def ab_entangled_cluster(a,b,ab_df):
    global max_cluster
    global max_cluster_index
    cluster_dict = {}
    for (group_1,group_2), ab_cluster_df in ab_df.groupby(['group_struc_1','group_struc_2']):
        cluster = list(ab_cluster_df['p'])
        if len(cluster) > len(max_cluster):
            max_cluster = cluster
            max_cluster_index = (a,b,group_1,group_2)
        cluster_dict[(int(group_1),int(group_2))] = cluster

    return cluster_dict



for (a,b), ab_df in df.groupby(['a','b']):
    ab_cluster = ab_entangled_cluster(a,b,ab_df)
    entangled_data[(a,b)] = ab_cluster
    
print(max_cluster)
print(max_cluster_index)
# pprint.pp(entangled_data)



