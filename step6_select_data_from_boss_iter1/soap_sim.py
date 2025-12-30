#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 10:00:00 2025
Author: Nian Wu
Description: This script selects dissimilar BOSS data based on SOAP similarity, prescreen based on threshold 40.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from ase.visualize import view
from ase.io import read, write
from time import time
from dscribe.descriptors import SOAP
from scipy.spatial.distance import cdist
import os


r_cut=6
n_max=6
l_max=2
threshold=5
mols = read('/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step6_select_data_from_boss_iter1/config_energy_qbc_confs/config_energy_qbc_all.xyz', index=':')
soap = SOAP(
    species=["Au", "Zn", "C", "N", "H", "Cl", "Br", "Na", "O"],
    r_cut=r_cut,
    n_max=n_max,
    l_max=l_max,
    periodic=True
)
dissim_matrix = np.zeros((len(mols), len(mols)))

mol_id_deleted=[]
for id_i, mol_a in enumerate(mols):
    if id_i not in mol_id_deleted:
        for id_j, mol_b in enumerate(mols):
            # if id_j <= id_i and id_j not in mol_id_selected:
            if id_j != id_i and (id_j not in mol_id_deleted):
                
                print("Calculating dissimilarity between molecule {} and {}".format(id_i, id_j))


                feat_a = soap.create([mol_a])

                # print(r_cut, n_max, l_max,"Time taken:", time1 - time0)
                feat_b = soap.create([mol_b])
                euclid_dist = cdist(feat_a, feat_b, metric='euclidean')
                # print(r_cut, n_max, l_max,"Time taken:", time3 - time2)
                euclid_dist_min_mean = euclid_dist.min(axis=0).mean() # each element in mol_b to mol_a, then mean over all elements in mol_b
                dissim_matrix[id_i, id_j] = euclid_dist_min_mean
                dissim_matrix[id_j, id_i] = euclid_dist_min_mean
                with open(f'soap_sim_rcut{r_cut}_nmax{n_max}_lmax{l_max}_{threshold}.txt', 'a') as f:
                    f.write(f"{id_i}, {id_j}, {euclid_dist_min_mean}\n")
                if euclid_dist_min_mean<threshold:
                    mol_id_deleted.append(id_j)
                    
        print(f"Current deleted molecules: {id_i}, {mol_id_deleted}")
        with open(f'soap_sim_rcut_{threshold}.txt', 'a') as f:
            f.write(f"Current deleted molecules: {id_i}, {mol_id_deleted}\n")


mol_id_left=[i for i in range(len(mols)) if i not in mol_id_deleted]
with open(f'soap_selected_dissimilar_thre{threshold}.txt', 'w') as f:
    for index in mol_id_left:
        f.write(f"{index}\n")
        
        
boss_data=pd.read_csv('config_energy_qbc_all.txt', delim_whitespace=True)

boss_data_left=boss_data.iloc[mol_id_left]
boss_data_left.to_csv(f'soap_selected_dissimilar_thre{threshold}_boss.txt', sep=' ', index=False)

        
mol_left=[mols[i] for i in mol_id_left]
write(f'soap_selected_dissimilar_thre{threshold}.xyz', mol_left, format='extxyz')