#!/bin/bash

python  generate_neb_end_configs.py  -i mol_init_config.xyz  -s mol_end_config

neb_lists=$(ls *end*.xyz)

neb_init=$(ls mol_init_*.xyz)

for  neb in $neb_lists
do
    echo $neb
    name=$(basename $neb .xyz)
    neb_init_base=$(basename $neb_init .xyz)
    mkdir $name
    cp  $neb  mol_init_*.xyz  neb_mace.py md_mace.sh	$name/

    cd $name
    sed -i  "s/mol_init_config/${neb_init_base}/"  neb_mace.py
    sed -i  "s/mol_end_config/${name}/"  neb_mace.py
    sbatch md_mace.sh
    cd ../

done
