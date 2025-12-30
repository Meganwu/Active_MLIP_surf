#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=02-04:30:00
#SBATCH --mem=32G
#SBATCH --partition=gpu-h200-141g-short,gpu-a100-80g
#SBATCH --cpus-per-task=4

module load  cuda/11.3.1

python neb_mace.py

echo "Mace MD."
