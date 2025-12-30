#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=00-00:30:00
#SBATCH --mem=32G
#SBATCH --partition=interactive,gpu-v100-32g,gpu-a100-80g
#SBATCH --cpus-per-task=4

module load  cuda/11.3.1

python opt_sim.py

echo "Mace OPT."
