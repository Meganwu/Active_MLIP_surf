import numpy as np
from boss.bo.bo_main import BOMain
from boss.pp.pp_main import PPMain
import sys
sys.path.append("/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au")

from utils.construct_utils import rotate_around_axis, get_dihedral, set_dihedral_with_mask, adjust_mol_dihedral


#we can use MACE as a calculator in ASE!
from mace.calculators import MACECalculator

from ase.io import read, write


def function_to_optimize(inputs):
    print("Inputs received for optimization:", inputs)
    z_from_surf, x_from_center, y_from_center, angle_frag1, angle_frag2, alpha, beta, gamma = inputs[:, 0][0], inputs[:, 1][0], inputs[:, 2][0], inputs[:, 3][0], inputs[:, 4][0], inputs[:, 5][0], inputs[:, 6][0], inputs[:, 7][0]
    print("Parsed inputs:", z_from_surf, angle_frag1, angle_frag2)
    # Here you would implement the actual function to optimize
    # For demonstration purposes, let's return a dummy value
    main_path='/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au'
    mace_calc_found = MACECalculator(model_paths=[f'{main_path}/foundation_model/2023-12-03-mace-128-L1_epoch-199.model'], device='cuda', default_dtype="float64")

    mol_znbr2=read(f'{main_path}/separate_configs/znbr2.in', format='aims')
    nacl_surf=read(f'{main_path}/separate_configs/NaCl_surf.in', format='aims')
    complex = adjust_mol_dihedral(mol_znbr2, nacl_surf, angle_frag1=angle_frag1, angle_frag2=angle_frag2, alpha=alpha, beta=beta, gamma=gamma, z_from_surf=z_from_surf, ref_atom=30, ref_one_atom=False)
    energies = []
    for calc in [mace_calc_found]: 
        init_conf = complex.copy()
        init_conf.calc = calc   
        energy = init_conf.get_potential_energy()
        energies.append(energy)

    energy_surrogate = energy  # Adjusted for single calculator
    with open('config_energy_qbc.txt', 'a') as f:
        f.write(f"{z_from_surf} {x_from_center} {y_from_center} {angle_frag1} {angle_frag2} {alpha} {beta} {gamma} {energy_surrogate}\n")

    return energy


if __name__ == "__main__":
    # Define the bounds for the optimization

    z_from_surf_bound = [0.5, 4.5]
    x_from_center_bound = [-14.1, 14.1]
    y_from_center_bound = [-19.74, 19.74]
    angle_frag1_bound = [-180, 180]
    angle_frag2_bound = [-180, 180]
    alpha_bound = [-180, 180]
    beta_bound = [-180, 180]
    gamma_bound = [-180, 180]

    bounds = np.array([z_from_surf_bound, x_from_center_bound, y_from_center_bound, angle_frag1_bound, angle_frag2_bound, alpha_bound, beta_bound, gamma_bound])
    with open('config_energy_qbc.txt', 'a') as f:
        f.write(f"z_from_surf x_from_center y_from_center angle_frag1 angle_frag2 alpha beta gamma energy_surrogate\n")


    bo = BOMain(
        function_to_optimize,
        bounds,
        kernel='rbf',
        initpts=10,
        iterpts=40
    )

    res = bo.run()
    print('Predicted global min: ', res.select('mu_glmin', -1))
    
    pp = PPMain(res, pp_models=True, pp_acq_funcs=True)
    pp.run()

