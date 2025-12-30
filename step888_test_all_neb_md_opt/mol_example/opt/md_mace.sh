#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=00-01:00:00
#SBATCH --mem=32G
#SBATCH --partition=gpu-v100-32g,gpu-a100-80g
#SBATCH --cpus-per-task=4

module load  cuda/11.3.1

# config_input=$(ls *.in)
# cp    $config_input  geometry.in

python opt_sim.py

echo "Mace OPT."
