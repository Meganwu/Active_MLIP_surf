#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 10:00:00 2025
Author: Nian Wu
Description: This script selects dissimilar BOSS data based on SOAP similarity, calculating both mean and max dissimilarities, here the dissmilarity on mol_a and mol_b is not equal to mol_b and mol_a, it reflects the dissimilary of atoms in a molecules compared to all atoms in another molecule.
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

import argparse

# Define parameters
parser = argparse.ArgumentParser(description='Process SOAP parameters.')
parser.add_argument('-i', '--input_file', type=str, default='all_final_configs_nacl.xyz', help='Input XYZ file')

args = parser.parse_args()
input_file = args.input_file


r_cut=6
n_max=6
l_max=2
threshold=5
mols = read(input_file , index=':')
soap = SOAP(
    species=["Au", "Zn", "C", "N", "H", "Cl", "Br", "Na", "O"],
    r_cut=r_cut,
    n_max=n_max,
    l_max=l_max,
    periodic=True
)
dissim_matrix_min_mean = np.zeros((len(mols), len(mols)))
dissim_matrix_min_max = np.zeros((len(mols), len(mols)))


dissim_matrix_whole = np.zeros((len(mols), len(mols)))




with open(f'soap_sim_matrix_min_mean.txt', 'a') as f:
    f.write(f"mol_i, mol_j, min_mean_dissimilarity\n")
    
with open(f'soap_sim_matrix_min_max.txt', 'a') as f:
    f.write(f"mol_i, mol_j, min_max_dissimilarity\n")
    
with open(f'soap_sim_matrix_whole.txt', 'a') as f:
    f.write(f"mol_i, mol_j, whole_dissimilarity\n")


for id_i, mol_a in enumerate(mols):
        feat_a = soap.create([mol_a])
        for id_j, mol_b in enumerate(mols):    
           
                # print("Calculating dissimilarity between molecule {} and {}".format(id_i, id_j))

            feat_b = soap.create([mol_b])
            euclid_dist = cdist(feat_a, feat_b, metric='cosine')

            euclid_dist_min_mean = euclid_dist.min(axis=0).mean() # each element in mol_b to mol_a, then mean over all elements in mol_b
            dissim_matrix_min_mean[id_i, id_j] = euclid_dist_min_mean
            euclid_dist_min_max = euclid_dist.min(axis=0).max() # each element in mol_b to mol_a, then max over all elements in mol_b
            dissim_matrix_min_max[id_i, id_j] = euclid_dist_min_max
            
            
            euclid_dist_whole=cdist(feat_a.flatten().reshape(1, -1), feat_b.flatten().reshape(1, -1), metric='cosine')[0][0]
            dissim_matrix_whole[id_i, id_j] = euclid_dist_whole
            

                
            with open(f'soap_sim_matrix_min_mean.txt', 'a') as f:
                f.write(f"{id_i}, {id_j}, {euclid_dist_min_mean}\n")
                
            with open(f'soap_sim_matrix_min_max.txt', 'a') as f:
                f.write(f"{id_i}, {id_j}, {euclid_dist_min_max}\n")
            
            with open(f'soap_sim_matrix_whole.txt', 'a') as f:
                f.write(f"{id_i}, {id_j}, {euclid_dist_whole}\n")
                


