# TimeQuant Docker Architecture

## Overview
This repository contains the Docker files for 31 scientific computing engines used in the TimeQuant platform.

## Image Categories
- **Group 1**: Ab-Initio & Semi-Empirical DFT Engines (Fortran/C/MPI)
- **Group 2**: Scientific Python, Chemistry & Transport Engines
- **Group 3**: Molecular AI, Graph Neural Networks & MLIP (GPU/CUDA)
- **Group 4**: Tools, Databases & Analytical Models

## Interface Standard
All engines use `/workspace` as the default working directory and are executed by a non-root user (`UID 1000:GID 1000`).
Volumes mapped to `/workspace` will receive the standard outputs.
