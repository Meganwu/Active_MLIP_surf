#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=1-10:30:00
#SBATCH --mem=4G
#SBATCH --partition=gpu-v100-16g,gpu-v100-32g
#SBATCH --cpus-per-task=4


module load  cuda/11.3.1

python soap_sim.py


echo 'Active learning Done'
