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


#we can use MACE as a calculator in ASE!
from mace.calculators import MACECalculator

from ase.optimize import BFGS


mace_calc = MACECalculator(model_paths=['add_random_plus_distort_model_path'], device='cuda', default_dtype="float64")


init_conf_opt = read('geometry.xyz', '0')
init_conf_opt.calc=mace_calc



opt = BFGS(init_conf_opt)


def write_frame():
        opt.atoms.write('mace_opt_traj.xyz', append=True)
opt.attach(write_frame, interval=5)
opt.run(fmax=0.001)
