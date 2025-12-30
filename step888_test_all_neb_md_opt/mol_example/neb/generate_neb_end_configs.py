#!/usr/bin/env python3
'''Author: Nian Wu
   Date: Oct 2025       
   Description: Generate the initial and final configurations for NEB calculations.
'''


from ase.io import read, write
import pandas as pd
from ase.visualize import view
import numpy as np

import argparse
import os


parser = argparse.ArgumentParser(description='Generate NEB end configurations.')

parser.add_argument('-i','--mol_init_file', type=str, default='mol_init_sample_1.xyz', help='File for the initial configuration.')
parser.add_argument('-s','--mol_end_prefix', type=str, default='mol_end_sample_1', help='Prefix for the end configuration files.')


args = parser.parse_args()

mol = read(args.mol_init_file)

mol_end_prefix = args.mol_end_prefix

mol_sub = mol[(mol.get_atomic_numbers() == 11) | (mol.get_atomic_numbers() == 17) | (mol.get_atomic_numbers() == 79)]
mol_mol = mol[(mol.get_atomic_numbers() != 11) & (mol.get_atomic_numbers() != 17) & (mol.get_atomic_numbers() != 79)]



mol_rot=mol_mol.copy()
mol_rot.translate([8, 0, 0])


mol_end_x_8=mol_sub + mol_rot
write(f'{mol_end_prefix}_x_8.xyz', mol_end_x_8)


mol_rot=mol_mol.copy()
mol_rot.translate([0, 8, 0])

mol_end_y_8=mol_sub + mol_rot
write(f'{mol_end_prefix}_y_8.xyz', mol_end_y_8)



mol_rot=mol_mol.copy()
mol_rot.translate([6, 6, 0])

mol_end_xy_6=mol_sub + mol_rot
write(f'{mol_end_prefix}_xy_6.xyz', mol_end_xy_6)


mol_rot=mol_mol.copy()


mol_rot.rotate(90, v='z', center=mol_rot.get_center_of_mass())
mol_end_rot_90=mol_sub + mol_rot
write(f'{mol_end_prefix}_rot_90.xyz', mol_end_rot_90)


mol_br=mol_mol.copy()
index_brs=np.where(mol.get_atomic_numbers()==35)[0].tolist()
center_of_mass=mol.get_center_of_mass()
mol_br=mol.copy()
for id in index_brs:
    pos=mol_br.get_positions()[id]
    
    new_pos=pos.copy()
    
    for xy in range(2):   # only change x and y coordinates
        if new_pos[xy]<center_of_mass[xy]:
            new_pos[xy]=pos[xy]-3
        else:
            new_pos[xy]=pos[xy]+3
    new_pos[2]=9      # set z coordinate to 9 angstrom, 1.7 angstrom away from the Cu(100)

    mol_br[id].position=new_pos
    
mol_end_br_3=mol_br.copy()
write(f'{mol_end_prefix}_br_3.xyz', mol_end_br_3)

