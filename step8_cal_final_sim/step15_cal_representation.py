from mace.calculators import mace_mp
from ase import build
from ase.md import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase import units
import torch
import os


from copy import deepcopy
from pathlib import Path

import ase.build
import h5py
import numpy as np
import torch
from ase import Atoms
import sys


from mace.data import (
    AtomicData,
    Configuration,
    HDF5Dataset,
    config_from_atoms,
    get_neighborhood,
    save_configurations_as_HDF5,
)
from mace.tools import AtomicNumberTable, torch_geometric
from mace import data, modules, tools
from ase.io import read, write

from mace.data import (
    Configuration,
    Configurations,
    compute_average_E0s,
    config_from_atoms,
    config_from_atoms_list,
    load_from_xyz,
    random_train_valid_split,
    save_AtomicData_to_HDF5,
    save_configurations_as_HDF5,
    save_dataset_as_HDF5,
    test_config_types,
)

import argparse
import os


parse = argparse.ArgumentParser()
parse.add_argument('-i','--input_xyz', type=str, default='iter1_md_opt.xyz', help='input xyz file')
args = parse.parse_args()

mols=read(args.input_xyz, format='extxyz',index=":")

os.mkdir('node_feats')
model = torch.load('/scratch/phys/sin/Nian_Wu/active_both_au_nacl_latest_version/active_MLIP_nacl_au/step4_iter1/refine_foundation/add_select_plus_distort/model_best.model')

basename=args.input_xyz.split('.')[0]
torch.save(model, f'{basename}.model')


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# table = AtomicNumberTable([i for i in range(89)])
table = AtomicNumberTable([1, 6, 7, 8, 11, 17, 30, 35, 79])

data_config=[]
for i in range(len(mols)):
    atoms=mols[i]
    atoms.info["REF_energy"] = atoms.get_potential_energy()
    atoms.arrays["REF_forces"] = atoms.get_forces()
    data_config.append(data.config_from_atoms(atoms)) 

data_atomic=[AtomicData.from_config(data_config[i], z_table=table, cutoff=6.0) for i in range(len(data_config))]


data_loader=torch_geometric.dataloader.DataLoader(
        dataset=data_atomic,
        batch_size=1,
        shuffle=False,
        drop_last=False,
    )

for i, j in enumerate(data_loader):
    batch=j
    batch=batch.to(torch.device(device))
    
    for key, value in batch.__dict__.items():
        if torch.is_tensor(value):
            if value.dtype == torch.float32:
                batch[key] = value.double()
    abc=model(batch)

    np.save(f'node_feats/node_feats_{i}.npy',  abc['node_feats'].detach().cpu().numpy())
