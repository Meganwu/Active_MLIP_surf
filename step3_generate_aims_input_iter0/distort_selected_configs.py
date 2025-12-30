#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 2025
Author: Nian Wu
Distort selected configurations from an input XYZ file and save to output XYZ file.
"""


from ase.io import read, write
from ase.visualize import view


import ase.neighborlist
import numpy as np
from itertools import combinations

from ase.neighborlist import neighbor_list, natural_cutoffs, NeighborList
import argparse
import os





np.random.seed(0)

class Distort:
    def __init__(self, atoms):
        self.atoms = atoms

    def apply_rattle(self, sd = 0.1):
        # Apply random distortion to atomic positions
        atoms_rattle = self.atoms.copy()
        rattle = np.random.normal(0, sd, atoms_rattle.positions.shape)
        atoms_rattle.positions += rattle

        return atoms_rattle
    def apply_bond_distort(self, sd=0.1, threshold=0.7):
        # Apply random distortion to bond lengths
        atoms_bond_distort = self.atoms.copy()
        
        # Define cutoffs automatically (element-dependent radii)
        cutoffs = natural_cutoffs(atoms_bond_distort)

# Build neighbor list
        i, j = neighbor_list("ij", atoms_bond_distort, cutoffs)

        for idx1, idx2 in zip(i, j):

            atomic_number_idx1 = atoms_bond_distort.get_atomic_numbers()[idx1]
            atomic_number_idx2 = atoms_bond_distort.get_atomic_numbers()[idx2]
            

            distance = atoms_bond_distort.get_distance(idx1, idx2)
            
            print(f"Distorting bond {distance} between atoms {idx1} (Z={atomic_number_idx1}) and {idx2} (Z={atomic_number_idx2})")
            distortion = np.random.normal(0, sd) * distance
            new_distance = distance + distortion
            count = 0
            while new_distance < threshold and count<10:  # Prevent unphysical bond lengths
                print(f"Warning: Bond length {new_distance:.3f} Å is below threshold {threshold:.3f} Å. Redistorting...")
                distortion = np.random.normal(0, sd) * distance
                new_distance = distance + distortion
                count += 1
                
            if count ==10:
                if distance < threshold:
                    new_distance=threshold  # Ensure bond length is above threshold
                else:
                    new_distance=distance  # Reset to original distance if too many attempts
                print(f"Resetting bond length to original value {distance:.3f} Å after 10 attempts.")

            atoms_bond_distort.set_distance(idx1, idx2, new_distance, fix=0.5)

        return atoms_bond_distort

    def apply_angle_distort(self, sd=0.001):
        """Randomly distort bond angles"""
        atoms_angle_distort = self.atoms.copy()

        cutoffs = natural_cutoffs(atoms_angle_distort)
        nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
        nl.update(atoms_angle_distort)

        for j in range(len(atoms_angle_distort)):
            neighbors, _ = nl.get_neighbors(j)
            for i, k in combinations(neighbors, 2):
                angle = atoms_angle_distort.get_angle(i, j, k)
                distortion = np.random.normal(0, sd) * angle
                new_angle = angle + distortion
                # Build boolean mask
                mask = [False] * len(atoms_angle_distort)
                mask[k] = True
                
                if np.abs(new_angle) < 1 or np.abs(new_angle - 180) < 1:
                    pass

                else:
                    atoms_angle_distort.set_angle(i, j, k, new_angle, mask=mask)

        return atoms_angle_distort


    def apply_torsion_distort(self, sd=5.0):
        """Randomly distort dihedral (torsion) angles"""
        atoms_torsion_distort = self.atoms.copy()

        cutoffs = natural_cutoffs(atoms_torsion_distort)
        nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
        nl.update(atoms_torsion_distort)

        # Loop over bonds j-k as central axis
        for j in range(len(atoms_torsion_distort)):
            neighbors_j, _ = nl.get_neighbors(j)
            for k in neighbors_j:
                neighbors_k, _ = nl.get_neighbors(k)

                # i is neighbor of j (excluding k), l is neighbor of k (excluding j)
                for i in neighbors_j:
                    if i == k:
                        continue
                    for l in neighbors_k:
                        if l == j:
                            continue
                        # Valid torsion i-j-k-l
                        dihedral = atoms_torsion_distort.get_dihedral(i, j, k, l)
                        distortion = np.random.normal(0, sd)  # in degrees
                        new_dihedral = dihedral + distortion
                        # Move atom l and its "side"
                        mask = [False] * len(atoms_torsion_distort)
                        mask[l] = True
                        atoms_torsion_distort.set_dihedral(i, j, k, l, new_dihedral, mask=mask)

        return atoms_torsion_distort

if __name__ == "__main__":
    
    
    argparser = argparse.ArgumentParser(description='Distort selected configurations.')
    argparser.add_argument('-i', '--input_xyz', type=str, required=True, help='Path to the input XYZ file containing multiple molecules.')
    argparser.add_argument('-o', '--output_dir', default='distorted_configs', type=str, help='Directory to save the distorted configurations.')

    args = argparser.parse_args()
    mols = read(f'{args.input_xyz}', index=':')
    distor_select=['bond', 'angle', 'rattle'] 
    output_xyz = args.input_xyz.split('/')[-1].split('.xyz')[0] + '_distorted.xyz'
    
    os.makedirs(args.output_dir, exist_ok=True) 
    for i, mol_i in enumerate(mols):
            distort = Distort(mol_i)
            method = np.random.choice(3, size=1, replace=False)[0]
            if distor_select[method]=='bond':
                mol_distorted = distort.apply_bond_distort(sd=0.1)
            elif distor_select[method]=='angle':

                mol_distorted = distort.apply_angle_distort(sd=0.001)

            # elif distor_select[method]=='torsion':
            #     mol_distorted = distor.apply_torsion_distort(sd=5.0)
            elif distor_select[method]=='rattle':
                mol_distorted = distort.apply_rattle(sd=0.1)
            write(os.path.join(args.output_dir, f'{output_xyz}'), mol_distorted, format='extxyz', append=True)
