import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au")
from utils.construct_utils import rotate_around_axis, get_dihedral, set_dihedral_with_mask, adjust_mol_dihedral

#we can use MACE as a calculator in ASE!
from mace.calculators import MACECalculator

from ase.io import read, write

from ase.visualize import view
import os
from utils.utils import rmsd

save_prefix='all_posible_confs_br_diss'



os.chdir('opt_sim')
opt_list=os.listdir('./')
opt_list=[i for i in opt_list if 'complex' in i]

all_mols=[]
mol_num=0
for i in opt_list:
    if not os.path.exists(f'{i}/mace_opt_traj.xyz'):
        continue
    traj=read(f'{i}/mace_opt_traj.xyz', index='1::5')
    mol_ref_pos=traj[0].get_positions()

    for mol in traj:
        c_br_1=mol.get_distance(600, 634)
        c_br_2=mol.get_distance(601, 637)
        upper_br_pos_max=mol[mol.get_atomic_numbers()==35].get_positions()[:, 2].max()
        h_atoms=mol[mol.get_atomic_numbers()==1]
        c_atoms=mol[mol.get_atomic_numbers()==6]
        dist_h_c=np.linalg.norm(h_atoms.get_positions()[:, np.newaxis, :] - c_atoms.get_positions()[np.newaxis, :, :], axis=-1)
        min_h_c=np.min(dist_h_c, axis=1)
        h_too_far=False
        if min_h_c.max()>2.0:
            h_too_far=True
        if (c_br_1>2.3 or c_br_2>2.3) and (upper_br_pos_max<20) and not h_too_far:
            mol_pos=mol.get_positions()
            rmsd_ref=rmsd(mol_ref_pos, mol_pos, translate=True, rotate=True)
            if rmsd_ref>0.2:
                mol_num=mol_num+1
                print('Found it!')
                print('C-Br1:', c_br_1)
                print('C-Br2:', c_br_2)
                write(f'{save_prefix}_opt.xyz', mol, format='extxyz', append=True)
                all_mols.append(mol)
                print(mol_num)
                mol_ref_pos=mol.get_positions()
            else:
                pass
        
os.chdir('../md_sim')
opt_list=os.listdir('./')
opt_list=[i for i in opt_list if 'complex' in i]


all_mols=[]
mol_num=0
for i in opt_list:
    if not os.path.exists(f'{i}/mace_md_traj.xyz'):
        continue
    traj=read(f'{i}/mace_md_traj.xyz', index='1::5')
    
    mol_ref_pos=traj[0].get_positions()

    for mol in traj:
        c_br_1=mol.get_distance(600, 634)
        c_br_2=mol.get_distance(601, 637)
        upper_br_pos_max=mol[mol.get_atomic_numbers()==35].get_positions()[:, 2].max()
        h_atoms=mol[mol.get_atomic_numbers()==1]
        c_atoms=mol[mol.get_atomic_numbers()==6]
        dist_h_c=np.linalg.norm(h_atoms.get_positions()[:, np.newaxis, :] - c_atoms.get_positions()[np.newaxis, :, :], axis=-1)
        min_h_c=np.min(dist_h_c, axis=1)
        h_too_far=False
        if min_h_c.max()>2.0:
            h_too_far=True
        if (c_br_1>2.3 or c_br_2>2.3) and (upper_br_pos_max<20) and not h_too_far:
            mol_pos=mol.get_positions()
            rmsd_ref=rmsd(mol_ref_pos, mol_pos, translate=True, rotate=True)
            if rmsd_ref>0.2:
                mol_num=mol_num+1
                print('Found it!')
                print('C-Br1:', c_br_1)
                print('C-Br2:', c_br_2)
                write(f'{save_prefix}_md.xyz', mol, format='extxyz', append=True)
                all_mols.append(mol)
                print(mol_num)
                mol_ref_pos=mol.get_positions()
            else:
                pass