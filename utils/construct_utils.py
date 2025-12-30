#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2024-06-05 11:00:00
Author: Nian Wu
Goal: Adjust the torsion angle of a molecule on a surface and save the configurations.
This script uses ASE and MACE to adjust the torsion angles of a molecule on a surface
and save the configurations in an extxyz file. The molecule is adjusted by rotating
the dihedral angles and translating the molecule to a specified height above the surface.
The script also calculates the potential energy and forces of the initial configuration
using MACE and saves the results in a text file.
'''

import ase
from ase.visualize import view
from ase.io import read, write
import numpy as np
import matplotlib.pyplot as plt


from ase import Atoms
from ase.neighborlist import neighbor_list
import random

from ase.geometry import get_distances
from ase.visualize import view
from scipy.spatial.transform import Rotation as R
import itertools

import warnings
warnings.filterwarnings("ignore")


import random
import numpy as np
import matplotlib.pyplot as plt


#we can use MACE as a calculator in ASE!
from mace.calculators import MACECalculator


def rotate_around_axis(v, axis, angle):
    """Rotate vector v around axis by angle (in radians) using Rodrigues' formula."""
    axis = axis / np.linalg.norm(axis)
    return (v * np.cos(angle)
            + np.cross(axis, v) * np.sin(angle)
            + axis * np.dot(axis, v) * (1 - np.cos(angle)))
    

# Compute current dihedral angle
def get_dihedral(p1, p2, p3, p4):
    b1 = p2 - p1
    b2 = p3 - p2
    b3 = p4 - p3
    n1 = np.cross(b1, b2)
    n2 = np.cross(b2, b3)
    n1 /= np.linalg.norm(n1)
    n2 /= np.linalg.norm(n2)
    m1 = np.cross(n1, b2 / np.linalg.norm(b2))
    x = np.dot(n1, n2)
    y = np.dot(m1, n2)
    return np.arctan2(y, x)

def set_dihedral_with_mask(positions, i, j, k, l, angle_deg, rotate_indices):
    """Set dihedral i-j-k-l to angle_deg by rotating only atoms in rotate_indices."""
    angle_rad = np.radians(angle_deg)

    # Define rotation axis (bond between j and k)
    axis = positions[k] - positions[j]
    axis = axis / np.linalg.norm(axis)


    current_angle = get_dihedral(positions[i], positions[j], positions[k], positions[l])
    delta_angle = angle_rad - current_angle

    origin = positions[j]  # rotate around atom j

    # Apply rotation to specified atoms only
    new_positions = positions.copy()
    for idx in rotate_indices:
        v = positions[idx] - origin
        v_rot = rotate_around_axis(v, axis, delta_angle)
        new_positions[idx] = origin + v_rot

    return new_positions


def adjust_mol_dihedral(mol_znbr2, surf, angle_frag1=45, angle_frag2=160, alpha=0, beta=0, gamma=0, z_from_surf=3, x_from_center=0, y_from_center=0, ref_atom=30, rotate_indices=None, ref_one_atom=False):
    """Adjust dihedral angle in the molecule ZnBr2, one is for the phenyl group and the other is for another phenyl group."""

    # adjust the torsion angle of the molecule
    mol_torsion = mol_znbr2.copy()
    surf = surf.copy()
    positions = mol_torsion.get_positions()
    # Define mol_torsion for torsion i-j-k-l
    i, j, k, l =  25, 11, 6, 26    #57, 59, 46, 61          #8, 46, 6, 7
    
    # Define which mol_torsion you want to rotate
    rotate_indices = [11, 46, 47, 49, 51, 53, 50, 48, 25, 26, 52, 30, 31, 64, 65, 34, 0]  # manually chosen based on your structure
    
    # Desired new dihedral angle in degrees
    new_angle = angle_frag1
    
    # Apply custom rotation
    new_positions = set_dihedral_with_mask(positions, i, j, k, l, new_angle, rotate_indices)
    mol_torsion.set_positions(new_positions)
    
    i, j, k, l =  32, 14, 23, 33    #57, 59, 46, 61          #8, 46, 6, 7
    
    # Define which mol_torsion you want to rotate
    rotate_indices = [23, 61, 62, 63, 56, 57, 58, 59, 60, 32, 33, 66, 67, 35, 36, 37, 1]  # manually chosen based on your structure
    
    # Desired new dihedral angle in degrees
    new_angle = angle_frag2

    # Apply custom rotation
    new_positions = set_dihedral_with_mask(new_positions, i, j, k, l, new_angle, rotate_indices)
    mol_torsion.set_positions(new_positions)



    # adjust the molecule to the surface z + rotation angle


    rot = R.from_euler('xyz', [alpha, beta, gamma], degrees=True)
    
    mol_rot=mol_torsion.copy()
    mol_rot.translate(-mol_rot.get_center_of_mass())
    mol_rot.positions = rot.apply(mol_rot.positions)

    mol_shift = mol_rot.copy()
    z_surf_max = surf.get_positions()[:, 2].max()

    # choose one atom as the referred position of the molecule (Zn)
    if ref_one_atom:
        ref_mol_idx = np.where(mol_shift.get_atomic_numbers() == ref_atom)[0][0]
        ref_mol_pos = mol_shift.get_positions()[ref_mol_idx]
        mol_shift.translate([surf.get_positions()[:, 0].mean()+x_from_center, surf.get_positions()[:, 1].mean()+y_from_center, z_surf_max - ref_mol_pos[2] + z_from_surf])
    else:
        # choose the lowest z position of the molecule as the reference point
        mol_shift.translate([surf.get_positions()[:, 0].mean()+x_from_center, surf.get_positions()[:, 1].mean()+y_from_center, z_surf_max - mol_shift.positions[:, 2].min() + z_from_surf])
    complex=surf + mol_shift
    return complex