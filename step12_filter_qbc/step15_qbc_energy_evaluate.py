import numpy as np
from ase.io import read, write
import pandas as pd
import os
import sys


#we can use MACE as a calculator in ASE!
from mace.calculators import MACECalculator

from ase.io import read, write

import argparse
import os



if __name__ == "__main__":
    
    parse = argparse.ArgumentParser()
    parse.add_argument('-i','--input_xyz', type=str, default='iter1_md_opt.xyz', help='input xyz file')
    args = parse.parse_args()
    
    mols=read(args.input_xyz, format='extxyz',index=":")
    
    with open('Energy_evaluate_by_qbc.txt', 'a') as f:

        f.write(f"id energy_found_select energy_found_distort energy_found_both\n")


    

    mace_calc_select = MACECalculator(model_paths=['/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/refine_foundation/add_select/model_best.model'], device='cuda', default_dtype="float64")
    mace_calc_distort = MACECalculator(model_paths=['/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/refine_foundation/add_distort/model_best.model'], device='cuda', default_dtype="float64")    
    mace_calc_both = MACECalculator(model_paths=['/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/refine_foundation/add_select_plus_distort/model_best.model'], device='cuda', default_dtype="float64")


    for id, mol in enumerate(mols):
        energies = []


        for calc in [mace_calc_select, mace_calc_distort, mace_calc_both]: #[mace_calc_seed_25, mace_calc_seed_111, mace_calc_seed_2222, mace_calc_seed_80]:
            init_conf = mol.copy()
            init_conf.calc = calc   
            energy = init_conf.get_potential_energy()
            energies.append(energy)

        energy_found_select, energy_found_distort, energy_found_both = energies[0], energies[1], energies[2]

        with open('Energy_evaluate_by_qbc.txt', 'a') as f:
            f.write(f"{id} {energy_found_select} {energy_found_distort} {energy_found_both}\n")




