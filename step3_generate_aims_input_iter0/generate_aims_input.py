import argparse
from ase.io import read, write
import os
import shutil

parser = argparse.ArgumentParser(description='Generate FHI-aims input files for a list of molecules.')
parser.add_argument('-i', '--input_xyz', type=str, required=True, help='Path to the input XYZ file containing multiple molecules.')
parser.add_argument('-o', '--output_dir', default='aims_inputs', type=str, help='Directory to save the generated FHI-aims input files.')

path=os.getcwd()
args = parser.parse_args()

mols = read(args.input_xyz, index=':')
os.makedirs(args.output_dir, exist_ok=True)

for i, mol in enumerate(mols):
    write(os.path.join(args.output_dir, f'mol_{i}.in'), mol, format='aims')
    os.makedirs(os.path.join(args.output_dir, f'mol_{i}'), exist_ok=True)
    shutil.copy('control.in', os.path.join(args.output_dir, f'mol_{i}', 'control.in'))
    shutil.move(os.path.join(args.output_dir, f'mol_{i}.in'), os.path.join(args.output_dir, f'mol_{i}'))
    os.chdir(os.path.join(args.output_dir, f'mol_{i}'))
    shutil.copy(f'mol_{i}.in', 'geometry.in')
    os.chdir(path)

    
