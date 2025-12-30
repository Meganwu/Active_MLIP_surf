#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 10:00:00 2025
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


parse = argparse.ArgumentParser()
parse.add_argument('-i','--input_xyz', type=str, default='iter1_md_opt.xyz', help='input xyz file')
args = parse.parse_args()

mols=read(args.input_xyz, format='extxyz',index=":")

os.mkdir('node_feats')


r_cut=6
n_max=6
l_max=2

soap = SOAP(
    species=["Au", "Zn", "C", "N", "H", "Cl", "Br", "Na", "O"],
    r_cut=r_cut,
    n_max=n_max,
    l_max=l_max,
    periodic=True
)



for id_i, mol in enumerate(mols):
    feat_a = soap.create([mol])

    np.save(f'node_feats/node_feats_{id_i}.npy',  feat_a)
