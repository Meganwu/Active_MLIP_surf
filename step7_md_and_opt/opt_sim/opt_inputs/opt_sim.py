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


mace_calc = MACECalculator(model_paths=['/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/refine_foundation/add_select_plus_distort/model_best.model'], device='cuda', default_dtype="float64")


init_conf_opt = read('geometry.in', '0')
init_conf_opt.calc=mace_calc



opt = BFGS(init_conf_opt)


def write_frame():
        opt.atoms.write('mace_opt_traj.xyz', append=True)
opt.attach(write_frame, interval=5)
opt.run(fmax=0.001)
