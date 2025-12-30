#!/bin/bash                                                             
#SBATCH --gres=gpu:1
#SBATCH --time=1-01:00:00
#SBATCH --mem=200G
#SBATCH --partition=gpu-h100-80g,gpu-a100-80g,gpu-h200-141g-short
#SBATCH --cpus-per-task=4


module load  cuda/11.3.1

srun python /scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/run_train_mace.py \
    --name="MACE_model" \
    --train_file='/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step17_iter2/dataset/train_iter1_select_DFT.xyz' \
    --valid_file='/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/dataset/val_iter0_both_DFT_10.xyz' \
    --foundation_model='/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/foundation_model/2023-12-03-mace-128-L1_epoch-199.model' \
    --test_file='/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/dataset/test_iter0_both_DFT_10.xyz' \
    --config_type_weights='{"Default":1.0}' \
    --model="MACE" \
    --atomic_numbers='[1, 6, 7, 8, 11, 17, 30, 35, 79]' \
    --E0s='{1:-13.598030178, 6:-1029.087494198, 7:-1485.307647843, 8:-2043.220684883, 11:-4422.011244216, 17:-12577.599814567, 30:-49117.029297278, 35:-71401.358069985, 79:-535649.538385919}' \
    --hidden_irreps='128x0e+128x1o+128x2e' \
    --energy_key='energy' \
    --forces_key='forces' \
    --batch_size=8 \
    --valid_batch_size=4 \
    --results_dir='retrain_results' \
    --max_num_epochs=5000 \
    --swa_lr=0.0001 \
    --swa \
    --start_swa=2 \
    --ema \
    --ema_decay=0.99 \
    --amsgrad \
    --restart_latest \
    --device=cuda \
    --seed=111 \

