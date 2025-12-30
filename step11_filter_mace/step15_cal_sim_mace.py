import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ase.io import read, write
from ase.visualize import view

from skimage.metrics import structural_similarity as ssim

import pandas as pd
from tqdm import tqdm

import sys
sys.path.append("/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_au")

import argparse
import os

from utils.utils import ssim_distance
import argparse
import os
import numpy as np
from scipy.spatial.distance import cdist
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Process MACE features.')
parser.add_argument('-i', '--input_file', type=str, default='all_final_configs_nacl.xyz', help='Input XYZ file')
parser.add_argument('-s','--save_suffix', type=str, default='mace_feats', help='suffix for saved files')



args = parser.parse_args()
mols=read(args.input_file, format='extxyz',index=":")
save_suffix=args.save_suffix




node_feature_all=[]
pos_feature_all=[]
for i in tqdm(range(len(mols))):
    mol_feat = np.load(f"node_feats/node_feats_{i}.npy", allow_pickle=True)
    mol_pos=mols[i].get_positions()
    node_feature_all.append(mol_feat)
    pos_feature_all.append(mol_pos)

node_feature_all = np.stack(node_feature_all, axis=0)
pos_feature_all = np.stack(pos_feature_all, axis=0)


dissim_matrix_min_mean = np.zeros((len(mols), len(mols)))
dissim_matrix_min_max = np.zeros((len(mols), len(mols)))


dissim_matrix_whole = np.zeros((len(mols), len(mols)))



with open(f'sim_matrix_min_mean_{save_suffix}.txt', 'a') as f:
    f.write(f"mol_i, mol_j, min_mean_dissimilarity\n")
    
with open(f'sim_matrix_min_max_{save_suffix}.txt', 'a') as f:
    f.write(f"mol_i, mol_j, min_max_dissimilarity\n")
    
with open(f'sim_matrix_whole_{save_suffix}.txt', 'a') as f:
    f.write(f"mol_i, mol_j, whole_dissimilarity\n")


for id_i, mol_a in enumerate(mols):
        feat_a = node_feature_all[id_i]
        for id_j, mol_b in enumerate(mols):    
           
                # print("Calculating dissimilarity between molecule {} and {}".format(id_i, id_j))

            feat_b = node_feature_all[id_j]
            dist = cdist(feat_a, feat_b, metric='cosine')

            dist_min_mean = dist.min(axis=0).mean() # each element in mol_b to mol_a, then mean over all elements in mol_b
            dissim_matrix_min_mean[id_i, id_j] = dist_min_mean
            dist_min_max = dist.min(axis=0).max() # each element in mol_b to mol_a, then max over all elements in mol_b
            dissim_matrix_min_max[id_i, id_j] = dist_min_max
            
            
            dist_whole=cdist(feat_a.flatten().reshape(1, -1), feat_b.flatten().reshape(1, -1), metric='cosine')[0][0]
            dissim_matrix_whole[id_i, id_j] = dist_whole
            

                
            with open(f'sim_matrix_min_mean_{save_suffix}.txt', 'a') as f:
                f.write(f"{id_i}, {id_j}, {dist_min_mean}\n")
                
            with open(f'sim_matrix_min_max_{save_suffix}.txt', 'a') as f:
                f.write(f"{id_i}, {id_j}, {dist_min_max}\n")
            
            with open(f'sim_matrix_whole_{save_suffix}.txt', 'a') as f:
                f.write(f"{id_i}, {id_j}, {dist_whole}\n")
                

