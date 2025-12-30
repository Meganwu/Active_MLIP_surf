python generate_aims_input.py    -i selected_configs_for_DFT_final.xyz


python distort_selected_configs.py  -i selected_configs_for_DFT_final.xyz


python generate_aims_input.py -i distorted_configs/selected_configs_for_DFT_final_distorted.xyz -o aims_inputs_distort
