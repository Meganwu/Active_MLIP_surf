#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=0-10:30:00
#SBATCH --mem=200G
#SBATCH --partition=gpu-a100-80g,gpu-h200-141g-short
#SBATCH --cpus-per-task=4


module load  cuda/11.3.1

python bayessian_boss_multi_task.py


echo 'Active learning Done'
