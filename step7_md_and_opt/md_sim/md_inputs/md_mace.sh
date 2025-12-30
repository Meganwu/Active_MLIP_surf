#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=0-00:10:00
#SBATCH --mem=32G
#SBATCH --partition=interactive,gpu-v100-32g,gpu-a100-80g
#SBATCH --cpus-per-task=4

module load  cuda/11.3.1

python md_sim.py

echo "Mace MD."
