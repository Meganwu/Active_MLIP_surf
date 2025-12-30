#!/bin/bash



neb_lists=$(ls *end*.xyz)

neb_init=$(ls mol_init_*.xyz)


mkdir init_end_configs

mv *end*.xyz init_end_configs/



mkdir neb_end_configs


cp mol_init_*.xyz  neb_mace.py md_mace.sh  neb_end_configs/

cd neb_end_configs

for  neb in $neb_lists
do
    echo $neb
    name=$(basename $neb .xyz)
    neb_init_base=$(basename $neb_init .xyz)
    mkdir $name

    cp ../opt_end_configs/${name}/mace_opt_traj.xyz  $name/
    cp  mol_init_*.xyz  neb_mace.py md_mace.sh	$name/

    cd $name

    lattice_line=$(grep -n Lattice  mace_opt_traj.xyz    | tail -1 |  cut -d: -f1)
    delete_line=$((lattice_line-2))  

    sed -i "1,${delete_line}d"  mace_opt_traj.xyz

    mv  mace_opt_traj.xyz   $neb



    sed -i  "s/mol_init_config/${neb_init_base}/"  neb_mace.py
    sed -i  "s/mol_end_config/${name}/"  neb_mace.py
    sbatch md_mace.sh
    cd ../

done

cd ../