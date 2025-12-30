confs_folder='soap_selected_dissimilar_thre5_boss_confs'
control_folder='md_inputs'
cd  $confs_folder
md_lists=$(ls *.in)
cd ..

for md in $md_lists
do
    base=$(basename $md .in)
    echo $base
    mkdir $base
    cp ${confs_folder}/${md}   ${control_folder}/md_sim.py   ${control_folder}/md_mace.sh  $base
    cd $base
    cp $md  geometry.in
    sbatch  md_mace.sh
    cd ..
done
