#! /usr/bin/env python3
# Author: Nian Wu

import numpy as np
from scipy.spatial.distance import cdist
import os
from ase.io import write, read
from skimage.metrics import structural_similarity as ssim

def rmsd(a, b, translate=True, rotate=True):
    """Return root-mean-square distance between two sets of positions.

    Parameters
    ----------
    a, b : (N, 3) arrays
        Cartesian coordinates of two structures with N atoms.
        Cartesian coordinates of two structures with N atoms.
    translate : bool
        If True, remove center-of-mass translations before comparison.
    rotate : bool
        If True, also find optimal rotation (Kabsch algorithm).
    """
    a = a.reshape(-1, 3)
    b = b.reshape(-1, 3)
    a = np.array(a, float)
    b = np.array(b, float)

    if translate:
        a = a - a.mean(axis=0)
        b = b - b.mean(axis=0)

    if rotate:
        # Kabsch algorithm for optimal rotation
        C = np.dot(a.T, b)
        V, S, Wt = np.linalg.svd(C)
        d = np.sign(np.linalg.det(np.dot(V, Wt)))
        U = np.dot(V, np.dot(np.diag([1, 1, d]), Wt))
        a = np.dot(a, U)

    diff = a - b
    return np.sqrt((diff * diff).sum() / len(a))


def ssim_distance(u, v, num_atoms=669):
    # reshape back to 2D
    u2d = u.reshape(num_atoms, -1)
    v2d = v.reshape(num_atoms, -1)
    return 1 - ssim(u2d, v2d, data_range=1.0)   

def rank_dissim(dissim_matrix, mols=None, output_folder='selected_results', output_suffix='euclid'):
    """
    Rank dissimilarity matrix using greedy farthest-point selection.
    
    Parameters:
    - dissim_matrix: 2D numpy array, dissimilarity matrix (higher means more dissimilar)
    - mols (list): A list of molecule identifiers corresponding to the rows/columns of the matrix.
    - output_folder (str): The folder where the output file will be saved.
    - output_suffix (str): The suffix for the output file name.

    Returns:
    - selected: list of indices of selected samples
    """


    os.makedirs(output_folder, exist_ok=True)
    n = dissim_matrix.shape[0]
    k = n  # number of samples to choose

    # Step 1: start with the sample with largest average dissimilarity
    avg_dissim = dissim_matrix.mean(axis=1)
    start = np.argmax(avg_dissim)
    selected = [start]

    # Step 2: greedy farthest-point selection
    while len(selected) < k:
        # For each unselected, compute min dissimilarity to current set
        remaining = list(set(range(n)) - set(selected))
        min_dissim = []
        for r in remaining:
            d = np.min([dissim_matrix[r, s] for s in selected])
            min_dissim.append(d)
        # Pick the one with maximum min-dissimilarity
        best_idx = remaining[np.argmax(min_dissim)]
        selected.append(best_idx)

    with open(f'{output_folder}/dissim_ordered_{output_suffix}.txt', 'a') as f:
        for i in selected: 
            f.write(f"{i}\n")
            write(f'{output_folder}/dissim_ordered_mols_{output_suffix}.xyz', mols[i], format='extxyz', append=True)
            
    return selected



def rank_dissim_projected(dissim_matrix, mols=None, output_folder='selected_results', output_suffix='euclid'):
    """
    Rank dissimilarity matrix using greedy farthest-point selection.
    
    Parameters:
    - dissim_matrix: 2D numpy array, dissimilarity matrix (higher means more dissimilar)
    - mols (list): A list of molecule identifiers corresponding to the rows/columns of the matrix.
    - output_folder (str): The folder where the output file will be saved.
    - output_suffix (str): The suffix for the output file name.

    Returns:
    - selected: list of indices of selected samples
    """


    os.makedirs(output_folder, exist_ok=True)
    n = dissim_matrix.shape[0]
    k = n  # number of samples to choose

    # Step 1: start with the sample with largest average dissimilarity
    avg_dissim = dissim_matrix.mean(axis=1) # please check if axis is correct
    start = np.argmin(avg_dissim)
    selected = [start]
    dissim_min_to_selected = [1.0]

    # Step 2: greedy farthest-point selection
    while len(selected) < k:
        # For each unselected, compute min dissimilarity to current set
        remaining = list(set(range(n)) - set(selected))
        min_dissim = []
        for r in remaining:
            d = np.min([dissim_matrix[s, r] for s in selected])                    # check new molecule project on selected molecules
            min_dissim.append(d)
        # Pick the one with maximum min-dissimilarity
        best_idx = remaining[np.argmax(min_dissim)]
        selected.append(best_idx)
        dissim_min_to_selected.append(np.max(min_dissim))
       

    with open(f'{output_folder}/dissim_ordered_{output_suffix}.txt', 'a') as f:
        for i, idx in enumerate(selected): 
            f.write(f"{idx}, {dissim_min_to_selected[i]}\n")
            write(f'{output_folder}/dissim_ordered_mols_{output_suffix}.xyz', mols[idx], format='extxyz', append=True)
            
    return selected


