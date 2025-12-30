#!/bin/bash

python  generate_neb_end_configs.py  -i mol_init_config.xyz  -s mol_end_config

neb_lists=$(ls *end*.xyz)

neb_init=$(ls mol_init_*.xyz)

mkdir opt_end_configs

cp ../opt/md_mace.sh  opt_end_configs/
cp ../opt/opt_sim.py  opt_end_configs/

cd opt_end_configs

for  neb in $neb_lists
do
    echo $neb
    name=$(basename $neb .xyz)
    neb_init_base=$(basename $neb_init .xyz)

    mkdir $name
    cp  ../$neb  md_mace.sh  opt_sim.py	$name

    cd $name
    cp $neb    geometry.xyz

    sbatch md_mace.sh
    cd ../

done


