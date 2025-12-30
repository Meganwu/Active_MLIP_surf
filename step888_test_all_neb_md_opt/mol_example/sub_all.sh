#!/bin/bash

update_model='/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/refine_foundation/add_select_plus_distort/model_best.model'

for i in md opt neb
do

    if [ $i == opt ]; then
        cd opt
        cp ../*xyz .
        cp *xyz geometry.xyz

        sed -i "s|add_random_plus_distort_model_path|${update_model}|"  opt_sim.py



        sbatch md_mace.sh
        cd ../
    elif [ $i == md ]; then
        cd md

        sed -i "s|add_random_plus_distort_model_path|${update_model}|"  md_sim.py

        cp ../*xyz .
        cp *xyz geometry.xyz
        sbatch md_mace.sh
        cd ../
    elif [ $i == neb ]; then
        cd neb
        cp ../*xyz .
        cp *xyz mol_init_config.xyz

        sed -i "s|add_random_plus_distort_model_path|${update_model}|"  neb_mace.py

        bash sub_task_opt_end.sh
        cd ../
    fi
done