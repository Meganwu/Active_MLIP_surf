from ase import units
from ase.md.langevin import Langevin
from ase.io import read, write
import numpy as np
import time

from mace.calculators import MACECalculator

from ase import units
from ase.md.langevin import Langevin
from ase.io import read, write
import numpy as np
import time

from e3nn import *
from mace.modules import (
    AtomicEnergiesBlock,
    EquivariantProductBasisBlock,
    InteractionBlock,
    LinearDipoleReadoutBlock,
    LinearNodeEmbeddingBlock,
    LinearReadoutBlock,
    NonLinearDipoleReadoutBlock,
    NonLinearReadoutBlock,
    RadialEmbeddingBlock,
    ScaleShiftBlock,
    RealAgnosticInteractionBlock,
    RealAgnosticResidualInteractionBlock
)

from mace.modules import ScaleShiftMACE

mace_calc = MACECalculator(model_paths=['add_random_plus_distort_model_path'], device='cuda', default_dtype="float64")

init_conf = read('geometry.xyz', '0')
init_conf.calc=mace_calc

dyn = Langevin(init_conf, 0.5*units.fs, temperature_K=300, friction=5e-3)

def write_frame():
        dyn.atoms.write('mace_md_traj.xyz', append=True)
dyn.attach(write_frame, interval=20)
dyn.run(2000000)
print("MD finished!")
