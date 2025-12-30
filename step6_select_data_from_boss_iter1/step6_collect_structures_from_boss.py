import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au")
from utils.construct_utils import rotate_around_axis, get_dihedral, set_dihedral_with_mask, adjust_mol_dihedral


from ase.io import read, write
import argparse

parser = argparse.ArgumentParser(description="Process some molecular configurations.")
parser.add_argument("-i", "--input_file", type=str, default="boss_dissim_train_50.txt", help="Input file containing molecular data")

args = parser.parse_args()
basename=args.input_file.split('.')[0]

confs_save_folder=f'{basename}_confs'
os.mkdir(confs_save_folder)

data=pd.read_csv(args.input_file, delim_whitespace=True)  # You can adjust the slicing as needed

all_mols = []

main_path='/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au'

for i in range(len(data)):
        z_from_surf = float(data.loc[i, 'z_from_surf'])
        angle_frag1 = float(data.loc[i, 'angle_frag1'])
        angle_frag2 = float(data.loc[i, 'angle_frag2'])
        x_from_center = float(data.loc[i, 'x_from_center'])
        y_from_center = float(data.loc[i, 'y_from_center'])
        alpha = float(data.loc[i, 'alpha'])
        beta = float(data.loc[i, 'beta'])
        gamma = float(data.loc[i, 'gamma'])

        print("Parsed inputs:", z_from_surf, x_from_center, y_from_center, angle_frag1, angle_frag2, alpha, beta, gamma)
        # Here you would implement the actual function to optimize
        # For demonstration purposes, let's return a dummy value
#        mace_calc_found_5 = MACECalculator(model_paths=['/scratch/work/wun2/active_learning_full_new/step1_iter0/refine_foundation/iter0_mace_first_30_frame_5/model_best.model'], device='cuda', default_dtype="float64")
        mol_znbr2=read(f'{main_path}/separate_configs/znbr2.in', format='aims')
        nacl_surf=read(f'{main_path}/separate_configs/NaCl_surf.in', format='aims')
        complex = adjust_mol_dihedral(mol_znbr2, nacl_surf, angle_frag1=angle_frag1, angle_frag2=angle_frag2, alpha=alpha, beta=beta, gamma=gamma, z_from_surf=z_from_surf, ref_atom=30, ref_one_atom=False)
        
        init_conf = complex.copy()
        all_mols.append(init_conf)
        mid_name = f"{int(z_from_surf)}_{int(x_from_center)}_{int(y_from_center)}_{int(angle_frag1)}_{int(angle_frag2)}_{int(alpha)}_{int(beta)}_{int(gamma)}"
        file_name = f"{confs_save_folder}/complex_nacl_{mid_name}.in"
        write(file_name, init_conf, format='aims')
write(f'{confs_save_folder}/{basename}_all.xyz', all_mols, format='extxyz')
    
