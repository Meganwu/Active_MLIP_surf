import warnings
warnings.filterwarnings("ignore")
from mace.cli.run_train import main as mace_run_train_main
import sys
import logging

from ase.io import read, write
from ase import units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import Stationary, ZeroRotation, MaxwellBoltzmannDistribution

import random
import os
import time
import numpy as np
import pylab as pl
from IPython import display
from ase.neb import NEB


#we can use MACE as a calculator in ASE!
from mace.calculators import MACECalculator

from ase.optimize import BFGS


mace_calc = MACECalculator(model_paths=['add_random_plus_distort_model_path'], device='cuda', default_dtype="float64")

spring_constant = 0.1  # eV/Å^2
mol_init = read('mol_init_config.xyz', '0')
mol_end = read('mol_end_config.xyz', '0')
n_images = 11
images = [mol_init]
for i in range(n_images):
    image = mol_init.copy()
    image.calc = MACECalculator(
        model_paths=['add_random_plus_distort_model_path'],
        device='cuda', default_dtype="float64"
    )
    # Set the calculator to the MACE calculator
    images.append(image)
mol_end.calc = MACECalculator(
        model_paths=['add_random_plus_distort_model_path'],
        device='cuda', default_dtype="float64"
    )
images.append(mol_end)


neb = NEB(images, k=spring_constant, climb=True)
neb.interpolate()


# energies0 = [image.get_potential_energy() for image in images]
# print("Initial energies (eV):", energies0)

# We can now optimize the images using the BFGS algorithm
opt = BFGS(neb, trajectory='neb_test.traj', logfile="ci_neb.log")
opt.run(fmax=0.05)



for i, image in enumerate(images):
    write(f'neb_image_{i}.xyz', image, format='extxyz')
    
energies = [img.get_potential_energy() for img in images]
for i, (img, e) in enumerate(zip(images, energies)):
    print(f"Image {i:2d}: Energy = {e:.6f} eV")
    write(f"ci_image_{i:02d}.xyz", img)

# Identify climbing-image (highest-energy image)
max_idx = int(np.argmax(energies))
print(f"\nHighest energy image (CI guess): index {max_idx}, energy {energies[max_idx]:.6f} eV")
print("Saved all images to ci_image_XX.xyz; NEB trajectory saved to ci_neb.traj")



# def write_frame():
#         opt.atoms.write('opt_test.xyz', append=True)
# opt.attach(write_frame, interval=1)
# opt.run(fmax=0.001)
