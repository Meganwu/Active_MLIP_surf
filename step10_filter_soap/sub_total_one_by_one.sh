#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=05-00:00:00
#SBATCH --mem=20G
#SBATCH --partition=gpu-amd,gpu-a100-80g,gpu-h200-141g-short
#SBATCH --cpus-per-task=4


module load  cuda/11.3.1

#python  step15_cal_representation.py  -i dissim_ordered_mols_cosine_selected.xyz

python  step15_cal_sim_mace.py -i dissim_ordered_mols_cosine_selected.xyz -s soap_feat 
#python  step15_qbc_energy_evaluate.py -i dissim_ordered_mols_cosine_selected.xyz

# python  select_final_configs_DFT.py -m dissim_ordered_mols_cosine_selected.xyz -s similarity_cal_final.txt  -n 170

echo 'Active learning Done'
