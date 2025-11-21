# Active_learning_MLIPs


<!-- Badges -->
[![Paper](https://img.shields.io/badge/Paper-arXiv-blue)](https://doi.org/10.1021/jacs.4c14757)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/USERNAME/REPO)](https://github.com/Meganwu/AutoOSS_nanonis)
[![Documentation Status](https://readthedocs.org/projects/YOURDOC/badge/?version=latest)](https://YOURDOC.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxx.svg)](https://doi.org/10.5281/zenodo.13761822)
[![GitHub Release](https://img.shields.io/github/v/release/Meganwu/AutoOSS_nanonis)](https://github.com/Meganwu/AutoOSS_nanonis/releases)

---

# 📑 Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Releases](#releases)
- [Citation](#citation)
- [License](#license)




# About AutoOSS
<img src="./Image/total_architecture_zn_color_hel_font.png" alt="Workflow" style="width:90%;">

We developed the framework of AutoOSS (Autonomous on-surface synthesis) to automate chemical reactions (break bond, move fragments, form bond and assebmle structures) in scanning tunneling microscopy based on Nanonis V5 (part function based on Createc is also avaialble on GitHub https://github.com/Meganwu/AutoOSS_nanonis). It comprises the remote connection, target dection module, interpetation module (image classifiers to identify reactants and products), decision-making module to optimize manipulation parameters for each function as well as miscellaneous analysis scritps. 


## Project Structure

.
├── data
│   ├── raw
│   └── processed
├── src
│   ├── main.py
│   ├── utils.py
│   └── models
│       └── model.py
└── README.md

# Installation




# Step 1 randomly generate few initial dataset based on torsion angles and distance of molecules away from the surface
(example: ZnBr2Me4DPP majorly two flexible torsion angle)

## first 30 initial configs (optimized by DFT), choose configs at the interval of 5, 10, 15, 20.

# Step2  Train MLIPs (based on Mace here)
## from scratch
## refine from the foundation model


# Step3  Generate more configurations based on MLIPs
## a. BOSS  (random from all degrees of freedom, more on molecules close to surfaces, more on surfaces)
## b. MACE optimization  (C-H at most less than 2.5, C-Br less than 2.0
## C. MACE molecular dynamics
## d. randomly creat distorsions by changing bonds or angles from some inital configurations


# Step4 Evaluate these configurations
## Similarity
  ### RMSD (atomic positions n:3) 
  ### Similarity like SSIM and Cosine based on fingerprints (mace model node feature n: 640)
  ### QBC

### choose 50. all  in top 150 of three methods
### Randomly distort these 50 configs by distortions on rattle, bond, and angle.


# Step5 Construct new training dataset from step4



# Step6 Evaluate the performance of MLIPs
## STM images
## Optimization
## Diffusion energy







