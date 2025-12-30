import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read, write
from ase.visualize import view
import argparse
import sys
sys.path.append('/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au')
from utils.utils import rank_dissim_projected
import os

parser = argparse.ArgumentParser(description="Select final configurations based on similarity")
parser.add_argument('-m', "--input_mols", type=str, default="similarity_cal.txt", help="Input similarity file")
parser.add_argument('-s', "--similarity_data", type=str, default="sim_matrix_min_max_mace_feats.txt", help="CSV file containing similarity data")
parser.add_argument('-q', "--qbc_data", type=str, default="Energy_evaluate_by_qbc.txt", help="CSV file containing QBC results")
parser.add_argument('-n', "--num_select", type=int, default=200, help="Number of configurations to select")
parser.add_argument('-f', "--output_folder", type=str, default="selected_results_min_max", help='folder for all outputs')
parser.add_argument('-c', "--output_xyz", type=str, default="selected_configs_for_DFT.xyz", help="Output file for selected configurations")
parser.add_argument('-i', "--output_ids", type=str, default="selected_configs_for_DFT_ids.txt", help="Output file for selected configuration IDs")
args = parser.parse_args()

# Load similarity data

output_folder=args.output_folder
os.makedirs(output_folder, exist_ok=True)

mols=read(args.input_mols, format='extxyz',index=":")
qbc_data=pd.read_csv(args.qbc_data, sep=" ")


# Compute dissimilarity matrix 

mols_num=len(mols)

data_min_max=pd.read_csv('sim_matrix_min_max_mace_feats.txt', delim_whitespace=True)
data_min_mean=pd.read_csv('sim_matrix_min_mean_mace_feats.txt', delim_whitespace=True)
data_whole=pd.read_csv('sim_matrix_whole_mace_feats.txt', delim_whitespace=True)


data_min_max_array=data_min_max['min_max_dissimilarity'].to_numpy().reshape((mols_num, mols_num))
data_min_mean_array=data_min_mean['min_mean_dissimilarity'].to_numpy().reshape((mols_num, mols_num))
data_whole_array=data_whole['whole_dissimilarity'].to_numpy().reshape((mols_num, mols_num))


min_max_order=rank_dissim_projected(data_min_max_array, mols=mols, output_folder=output_folder, output_suffix='mace_cosine')



# Computer Uncertainty-based selection

qbc_data=pd.read_csv('Energy_evaluate_by_qbc.txt', sep=" ")

eval_lists=list(qbc_data)[1:4]
qbc_data["uncertainty_std"] = qbc_data[eval_lists].std(axis=1, ddof=1)  # sample std dev

# Standard error of the mean (uncertainty of the mean)
qbc_data["uncertainty_stderr"] = qbc_data["uncertainty_std"] / np.sqrt(len(eval_lists))
qbc_data=qbc_data.sort_values(by="uncertainty_std", ascending=False)
data_qbc_order=qbc_data.reset_index(drop=True)
qbc_selected=data_qbc_order['id'].tolist()
qbc_selected_std=data_qbc_order['uncertainty_std'].tolist()
qbc_selected_stderr=data_qbc_order['uncertainty_stderr'].tolist()
with open(f'{output_folder}/uncertainty_selected_ordered_qbc.txt', 'w') as f:
    for i, id in enumerate(qbc_selected):
        f.write(f"{id}, {qbc_selected_std[i]}, {qbc_selected_stderr[i]}\n")
        write(f'{output_folder}/uncertainty_selected_ordered_mols_qbc.xyz', mols[id], format='extxyz', append=True)

print(qbc_data[["id", "uncertainty_std", "uncertainty_stderr"]])


# # select the common subset of the three methods (first 200 structures)
# num_select=args.num_select
# cos_candidate=set(cos_selected[:num_select])
# rmsd_candidate=set(rmsd_selected[:num_select])
# qbc_candidate=set(qbc_selected[:num_select])

# common_subset=cos_candidate.intersection(rmsd_candidate).intersection(qbc_candidate)

# common_subset=[i for i in common_subset]

# max_forces_all_mols=np.array([mols[i].get_forces().max() for i in range(len(mols))])
# mol_del_ids=np.where(max_forces_all_mols>100)[0].tolist()

# print('delete mol:', mol_del_ids)

# common_subset=[i for i in common_subset if i not in mol_del_ids]

# cos_candidate=list(cos_candidate)
# rmsd_candidate=list(rmsd_candidate)
# qbc_candidate=list(qbc_candidate)

# print(f"Number of common selections among three methods: {len(common_subset)}")

# # Save selected configurations
# with open(f'{output_folder}/{args.output_ids}', 'w') as f:
#     for id in common_subset:
#         f.write(f"{id}\n")
#         write(f'{output_folder}/{args.output_xyz}', mols[id], format='extxyz', append=True)
        
# # Draw the distribution of the largest dissimilarity of each mol among selected mols


        
# np.fill_diagonal(dissim_matrix_rmsd, 0)
# np.fill_diagonal(dissim_matrix_cos, 0)


# # Draw the distribution of the least dissimilarity of each mol among selected mols
# dis_rmsd=dissim_matrix_rmsd[common_subset, :][:, common_subset].max(axis=1)
# dis_rmsd_all=dissim_matrix_rmsd.max(axis=1)


# dis_cos=dissim_matrix_cos[common_subset, :][:, common_subset].max(axis=1)
# dis_cos_all=dissim_matrix_cos.max(axis=1) 


# qbc_final_sel=qbc_data[qbc_data["id"].isin(common_subset)]

# plt.figure(figsize=(10, 3))
# plt.subplot(1,3,1)
# plt.hist(dis_rmsd_all, bins=20, alpha=0.5, label='RMSD-based all')
# plt.hist(dis_rmsd, bins=20, alpha=0.5, label='RMSD-based')
# plt.xlabel('RMSD_pos')
# plt.ylabel('Distribution')

# plt.subplot(1,3,2)
# plt.hist(dis_cos_all, bins=20, alpha=0.5, label='Cosine-based all')
# plt.hist(dis_cos, bins=20, alpha=0.5, label='Cosine-based')
# plt.xlabel('Cosine_features')
# plt.ylabel('Distribution')
# plt.subplots_adjust(wspace=0.5)

# plt.savefig(f'{output_folder}/largest_dissimilarity_among_mols.png', bbox_inches='tight')
        
        
        
# np.fill_diagonal(dissim_matrix_rmsd, np.inf)
# dis_rmsd=dissim_matrix_rmsd[common_subset, :][:, common_subset].min(axis=1)
# dis_rmsd_candidate=dissim_matrix_rmsd[rmsd_candidate, :][:, rmsd_candidate].min(axis=1)
# dis_rmsd_all=dissim_matrix_rmsd.min(axis=1)


# np.fill_diagonal(dissim_matrix_cos, np.inf)
# dis_cos=dissim_matrix_cos[common_subset, :][:, common_subset].min(axis=1)
# dis_cos_candidate=dissim_matrix_cos[cos_candidate, :][:, cos_candidate].min(axis=1)
# dis_cos_all=dissim_matrix_cos.min(axis=1)

# plt.figure(figsize=(14, 3))
# plt.subplot(1,3,1)
# plt.hist(dis_rmsd_all, bins=20, alpha=0.5, label='RMSD-based all')
# plt.hist(dis_rmsd_candidate, bins=20, alpha=0.5, color='b', label='RMSD-based candidate')
# plt.hist(dis_rmsd, bins=20, alpha=0.5, label='RMSD-based')
# plt.xlabel('RMSD_pos')
# plt.ylabel('Distribution')
# plt.legend()

# plt.subplot(1,3,2)
# plt.hist(dis_cos_all, bins=20, alpha=0.5, label='Cosine-based all')
# plt.hist(dis_cos_candidate, bins=20, alpha=0.5, color='b', label='Cosine-based candidate')
# plt.hist(dis_cos, bins=20, alpha=0.5, label='Cosine-based')
# plt.xlabel('Cosine_features')
# plt.ylabel('Distribution')
# plt.legend()

# plt.subplot(1,3,3)
# plt.hist(qbc_data["uncertainty_std"], bins=20, alpha=0.5, label='QBC-based all')
# plt.hist(qbc_final_sel["uncertainty_std"], bins=20, alpha=0.5, label='QBC-based')
# plt.xlabel('QBC_uncertainty')
# plt.ylabel('Distribution')
# plt.legend()

# plt.subplots_adjust(wspace=0.5)

# plt.savefig(f'{output_folder}/least_dissimilarity_among_mols.png', bbox_inches='tight')

