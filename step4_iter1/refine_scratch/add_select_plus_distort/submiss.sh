#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=4-04:00:00
#SBATCH --mem=200G
#SBATCH --partition=gpu-h200-141g-short
#SBATCH --cpus-per-task=4


module load  cuda/11.3.1

mace_run_train \
    --name="MACE_model" \
    --train_file="/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/dataset/iter0_both_DFT_train.xyz" \
    --valid_fraction=0.05 \
    --test_file="/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/dataset/iter0_both_DFT_test.xyz" \
    --config_type_weights='{"Default":1.0}' \
    --model="MACE" \
    --E0s="average" \
    --atomic_numbers="[1, 6, 7, 8, 11, 17, 30, 35, 79]" \
    --batch_size=8 \
    --results_dir="retrain_results" \
    --max_num_epochs=1000 \
    --swa_lr=0.0001 \
    --swa \
    --start_swa=2 \
    --ema \
    --ema_decay=0.99 \
    --amsgrad \
    --restart_latest \
    --device=cuda \
    --seed=111 \

