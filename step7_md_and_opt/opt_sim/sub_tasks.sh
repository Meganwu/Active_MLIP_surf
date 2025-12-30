confs_folder='soap_selected_dissimilar_thre5_boss_confs'
control_folder='opt_inputs'
cd  $confs_folder
opt_lists=$(ls *.in)
cd ..

for opt in $opt_lists
do
    base=$(basename $opt .in)
    echo $base
    mkdir $base
    cp ${confs_folder}/${opt}   ${control_folder}/opt_sim.py   ${control_folder}/md_mace.sh  $base
    cd $base
    cp $opt geometry.in
    sbatch md_mace.sh
    cd ..
done
