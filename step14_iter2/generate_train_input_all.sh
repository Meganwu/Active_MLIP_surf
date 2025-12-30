#!/bin/bash

main_dir=/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_au/step17_iter2
mkdir refine_foundation

cd refine_foundation

mkdir add_distort 
cp $main_dir/refine_foundation/add_distort/submiss.sh  add_distort
mkdir add_select
#cp $main_dir/refine_foundation/add_select/submiss.sh  add_select
mkdir add_select_plus_distort
#cp $main_dir/refine_foundation/add_select_plus_distort/submiss.sh  add_select_plus_distort
cd ..

mkdir refine_scratch

cd refine_scratch

mkdir add_distort 
cp $main_dir/refine_scratch/add_distort/submiss.sh   add_distort
mkdir add_select
#cp $main_dir/refine_scratch/add_select/submiss.sh add_select
mkdir add_select_plus_distort
#cp $main_dir/refine_scratch/add_select_plus_distort/submiss.sh  add_select_plus_distort