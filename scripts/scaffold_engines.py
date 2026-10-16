import os
import json
import stat

engines = {
    # =========================================================================
    # Group 1: Ab-Initio & Semi-Empirical DFT Engines (Fortran/C/MPI)
    # =========================================================================
    'qe': {
        'group': 1,
        'dockerfile': 'FROM ubuntu:22.04\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    quantum-espresso quantum-espresso-data openmpi-bin ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*\nENV ESPRESSO_PSEUDO=/opt/pseudos\nRUN mkdir -p /opt/pseudos /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/usr/bin/pw.x"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Quantum ESPRESSO..."\nwhich pw.x\nwhich ph.x\nwhich pp.x\necho "QE OK" > output.log\n',
    },
    'siesta': {
        'group': 1,
        'dockerfile': 'FROM mambaorg/micromamba:latest\nUSER root\nRUN micromamba install -y -n base -c conda-forge siesta && micromamba clean --all --yes\nENV PATH="/opt/conda/bin:$PATH"\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/opt/conda/bin/siesta"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying SIESTA..."\nwhich siesta || which /opt/conda/bin/siesta\necho "SIESTA OK" > output.log\n',
    },
    'cp2k': {
        'group': 1,
        'dockerfile': 'FROM ubuntu:22.04\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    cp2k cp2k-data openmpi-bin ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*\nRUN mkdir -p /workspace /opt/cp2k/data\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "cp2k"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying CP2K..."\nwhich cp2k\ncp2k --version\necho "CP2K OK" > output.log\n',
    },
    'dftb': {
        'group': 1,
        'dockerfile': 'FROM mambaorg/micromamba:latest\nUSER root\nRUN micromamba install -y -n base -c conda-forge dftbplus && micromamba clean --all --yes\nENV PATH="/opt/conda/bin:$PATH"\nRUN mkdir -p /workspace /opt/slater_koster\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/opt/conda/bin/dftb+"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying DFTB+..."\nwhich dftb+ || which /opt/conda/bin/dftb+\necho "DFTB+ OK" > output.log\n',
    },
    'openmx': {
        'group': 1,
        'dockerfile': 'FROM ubuntu:22.04\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    openmx openmx-data openmpi-bin ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "openmx"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying OpenMX..."\nwhich openmx\necho "OpenMX OK" > output.log\n',
    },
    'vasp': {
        'group': 1,
        'dockerfile': 'FROM ubuntu:22.04\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    openmpi-bin ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\n# VASP is BYOB: placeholder binary, to be replaced by the licensed vasp_std\nRUN printf \'#!/bin/bash\\necho "VASP BYOB wrapper run"\\n\' > /usr/local/bin/vasp_std && chmod 755 /usr/local/bin/vasp_std\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "vasp_std"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying VASP (BYOB wrapper)..."\nwhich vasp_std\nvasp_std\necho "VASP BYOB OK" > output.log\n',
    },
    'wannier90': {
        'group': 1,
        'dockerfile': 'FROM ubuntu:22.04\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    wannier90 openmpi-bin ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "wannier90"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Wannier90..."\nif which wannier90.x >/dev/null 2>&1; then\n    which wannier90.x\nelif which wannier90 >/dev/null 2>&1; then\n    which wannier90\nelse\n    echo "Wannier90 binary not found" && exit 1\nfi\necho "Wannier90 OK" > output.log\n',
    },
    'yambo': {
        'group': 1,
        'dockerfile': 'FROM mambaorg/micromamba:latest\nUSER root\nRUN micromamba install -y -n base -c conda-forge yambo && micromamba clean --all --yes\nENV PATH="/opt/conda/bin:$PATH"\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/opt/conda/bin/yambo"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Yambo..."\nwhich yambo || which /opt/conda/bin/yambo\necho "Yambo OK" > output.log\n',
    },
    # =========================================================================
    # Group 2: Tight-Binding, Many-Body, Transport & Phonons (Scientific Python)
    # =========================================================================
    'models': {
        'group': 2,
        'dockerfile': 'FROM python:3.12-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir --upgrade pip numpy scipy\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && mkdir -p /workspace && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Analytical Models..."\npython3 -c "import numpy, scipy; print(\'NumPy version:\', numpy.__version__)"\necho "Models OK" > output.log\n',
    },
    'ase_tools': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir ase spglib pymatgen\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying ASE & PyMatGen..."\npython3 -c "import ase; import pymatgen; print(\'ASE version:\', ase.__version__)"\necho "ASE Tools OK" > output.log\n',
    },
    'qeh': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir numpy scipy matplotlib ase qeh\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying QEH..."\npython3 -c "import qeh; print(\'QEH version:\', getattr(qeh, \'__version__\', \'OK\'))"\necho "QEH OK" > output.log\n',
    },
    'hetdb': {
        'group': 2,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nENV CMAKE_POLICY_VERSION_MINIMUM=3.5\nENV CFLAGS="-fPIC"\nENV CXXFLAGS="-fPIC -include cmath"\nRUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake \\\n    && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir pybind11\nRUN pip install --no-cache-dir hetbuilder ase pymatgen\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying HetDB / HetBuilder..."\npython3 -c "import hetbuilder; print(\'HetBuilder version:\', getattr(hetbuilder, \'__version__\', \'OK\'))"\necho "HetDB OK" > output.log\n',
    },
    'sisl': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --default-timeout=100 --no-cache-dir sisl netCDF4 xarray\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying sisl..."\npython3 -c "import sisl; print(\'sisl version:\', sisl.__version__)"\necho "sisl OK" > output.log\n',
    },
    'phonopy': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir phonopy spglib seekpath\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Phonopy..."\npython3 -c "import phonopy; print(\'Phonopy version:\', phonopy.__version__)"\necho "Phonopy OK" > output.log\n',
    },
    'atomistics': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir atomistics\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Atomistics..."\npython3 -c "import atomistics; print(\'Atomistics version:\', getattr(atomistics, \'__version__\', \'OK\'))"\necho "Atomistics OK" > output.log\n',
    },
    'boltztrap': {
        'group': 2,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git \\\n    && rm -rf /var/lib/apt/lists/*\nENV CMAKE_ARGS="-DSPGLIB_WITH_TESTS=OFF -DSPGLIB_TEST=OFF -DSPGLIB_TESTING=OFF"\nRUN pip install --no-cache-dir BoltzTraP2 spglib ase\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying BoltzTraP2..."\npython3 -c "import BoltzTraP2; print(\'BoltzTraP2 OK\')"\necho "BoltzTraP2 OK" > output.log\n',
    },
    'amset': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nFROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*\nRUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git \\\n    && rm -rf /var/lib/apt/lists/*\nENV CMAKE_ARGS="-DSPGLIB_WITH_TESTS=OFF -DSPGLIB_TEST=OFF -DSPGLIB_TESTING=OFF"\nRUN pip install --no-cache-dir amset pymatgen interpolation\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying AMSET..."\npython3 -c "import amset; print(\'AMSET version:\', amset.__version__)"\necho "AMSET OK" > output.log\n',
    },
    'wannier_berri': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir wannierberri scipy numba h5py\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying WannierBerri..."\npython3 -c "import wannierberri; print(\'WannierBerri version:\', wannierberri.__version__)"\necho "WannierBerri OK" > output.log\n',
    },
    'qutip': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir qutip scipy cython\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying QuTiP..."\npython3 -c "import qutip; print(\'QuTiP version:\', qutip.__version__)"\necho "QuTiP OK" > output.log\n',
    },
    'pyscf': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nFROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y gcc cmake build-essential && rm -rf /var/lib/apt/lists/*\nRUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git \\\n    && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir pyscf geometric pyberny\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying PySCF..."\npython3 -c "import pyscf; print(\'PySCF version:\', pyscf.__version__)"\necho "PySCF OK" > output.log\n',
    },
    'gpaw': {
        'group': 2,
        'dockerfile': 'FROM ubuntu:22.04\nFROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    python3-gpaw gpaw-data ca-certificates \\\nENV CC="g++"\nRUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git \\\n    && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir gpaw ase scipy\nRUN mkdir -p /workspace /opt/gpaw-setups\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "gpaw"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying GPAW..."\ngpaw info 2>&1 | head -n 10 || python3 -c "import gpaw; print(\'GPAW version:\', gpaw.__version__)"\necho "GPAW OK" > output.log\n',
    },
    'kwant': {
        'group': 2,
        'dockerfile': 'FROM python:3.11-slim\nFROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    gcc gfortran libmumps-dev liblapack-dev libblas-dev git \\\n    build-essential cmake git gfortran libmumps-dev liblapack-dev libblas-dev \\\n    && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir --upgrade pip \\\n    && pip install --no-cache-dir numpy scipy tinyarray \\\n    && pip install --no-cache-dir kwant\nRUN pip install --no-cache-dir "numpy<2" scipy tinyarray kwant\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && mkdir -p /workspace && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Kwant..."\npython3 -c "import kwant; print(\'Kwant version:\', kwant.__version__)"\necho "Kwant OK" > output.log\n',
    },
    'tkwant': {
        'group': 2,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    build-essential cmake git gfortran libmumps-dev liblapack-dev libblas-dev libopenmpi-dev openmpi-bin \\\n    && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir "numpy<2" scipy tinyarray kwant mpi4py sympy\nRUN pip install --no-cache-dir tkwant\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying TKwant..."\npython3 -c "import tkwant; print(\'TKwant version:\', tkwant.__version__)"\necho "TKwant OK" > output.log\n',
    },
    # =========================================================================
    # Group 3: Molecular AI, ML Potentials & PINNs (PyTorch/ML Frameworks)
    # =========================================================================
    'nanoworks': {
        'group': 3,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nENV CC="g++"\nRUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git \\\n    && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir nanoworks ase numpy scipy matplotlib\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Nanoworks..."\npython3 -c "import nanoworks; print(\'Nanoworks version:\', getattr(nanoworks, \'__version__\', \'OK\'))"\necho "Nanoworks OK" > output.log\n',
    },
    'electronex': {
        'group': 3,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir electronex numpy scipy matplotlib cython\nRUN mkdir -p /workspace /opt/electronex\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying ELEQTRONeX / electronex..."\npython3 -c "import electronex; print(\'electronex version:\', getattr(electronex, \'__version__\', \'OK\'))"\necho "ELEQTRONeX OK" > output.log\n',
    },
    'pinn': {
        'group': 3,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir --upgrade pip \\\n    && pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu \\\n    && pip install --no-cache-dir DeepXDE\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying PINN (DeepXDE)..."\npython3 -c "import deepxde; print(\'DeepXDE version:\', deepxde.__version__)"\necho "PINN OK" > output.log\n',
    },
    'deeptb': {
        'group': 3,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir --upgrade pip \\\n    && pip install --no-cache-dir torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu \\\n    && pip install --no-cache-dir torch-scatter -f https://data.pyg.org/whl/torch-2.5.1+cpu.html \\\n    && pip install --no-cache-dir dptb ase\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying DeePTB..."\npython3 -c "import dptb; print(\'DeePTB (dptb) version:\', getattr(dptb, \'__version__\', \'OK\'))"\necho "DeePTB OK" > output.log\n',
    },
    'rhodent': {
        'group': 3,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nENV CC="g++"\nRUN apt-get update && apt-get install -y --no-install-recommends build-essential git \\\n    && rm -rf /var/lib/apt/lists/*\nRUN pip install --no-cache-dir --upgrade pip \\\n    && pip install --no-cache-dir torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu \\\n    && pip install --no-cache-dir torch-scatter -f https://data.pyg.org/whl/torch-2.5.1+cpu.html \\\n    && pip install --no-cache-dir rhodent e3nn\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying Rhodent..."\npython3 -c "import rhodent; print(\'Rhodent version:\', getattr(rhodent, \'__version__\', \'OK\'))"\necho "Rhodent OK" > output.log\n',
    },
    'deepgreen': {
        'group': 3,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir --upgrade pip \\\n    && pip install --no-cache-dir torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu \\\n    && pip install --no-cache-dir torch-geometric greenlearning \\\n    && pip install --no-cache-dir \'numpy<2\' \'matplotlib<3.6\'\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying DeepGreen / GreenLearning..."\npython3 -c "import greenlearning; print(\'GreenLearning OK\')"\necho "DeepGreen OK" > output.log\n',
    },
    'mace': {
        'group': 3,
        'dockerfile': 'FROM python:3.10-slim\nENV DEBIAN_FRONTEND=noninteractive\nRUN pip install --no-cache-dir --upgrade pip \\\n    && pip install --no-cache-dir torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu \\\n    && pip install --no-cache-dir mace-torch ase torch-geometric\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && mkdir -p /workspace && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying MACE..."\npython3 -c "import mace; print(\'MACE version:\', getattr(mace, \'__version__\', \'OK\'))"\necho "MACE OK" > output.log\n',
    },
    # =========================================================================
    # Group 4: Potentials & Materials Databases
    # =========================================================================
    'kim': {
        'group': 4,
        'dockerfile': 'FROM ubuntu:22.04\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y --no-install-recommends \\\n    libkim-api-dev openkim-models ca-certificates curl \\\n    && rm -rf /var/lib/apt/lists/*\nRUN mkdir -p /workspace\nRUN useradd -u 1000 -m -s /bin/bash timequant \\\n    && chown -R timequant:timequant /workspace\nCOPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh\nRUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh\nUSER timequant\nWORKDIR /workspace\nENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "kim-api-collections-management"]\n',
        'test_script': '#!/bin/bash\nset -e\necho "[Test] Verifying OpenKIM..."\nwhich kim-api-collections-management\nkim-api-collections-management list\necho "OpenKIM OK" > output.log\n',
    },
}

def main():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = file_dir if os.path.exists(os.path.join(file_dir, "docker-engines")) else os.path.dirname(file_dir)
    base_dir = os.path.join(repo_root, "docker-engines", "engines")

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for engine, data in engines.items():
        engine_dir = os.path.join(base_dir, engine)
        test_dir = os.path.join(engine_dir, "test")

        os.makedirs(engine_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)

        # Write Dockerfile
        dockerfile_path = os.path.join(engine_dir, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(data['dockerfile'])

        # Write test.sh
        test_sh_path = os.path.join(engine_dir, "test.sh")
        with open(test_sh_path, "w") as f:
            f.write(data['test_script'])
        os.chmod(test_sh_path, 0o755)

        # Write README.md
        readme_path = os.path.join(engine_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write(f"# Engine: {engine}\n\nGroup: {data['group']}\n")

        # Write input/expected files
        with open(os.path.join(test_dir, "input.txt"), "w") as f:
            f.write("input\n")
        with open(os.path.join(test_dir, "expected.json"), "w") as f:
            json.dump({"status": "ok"}, f)

    print(f"Scaffolded and updated {len(engines)} full engines with real packages and smoke tests.")

if __name__ == "__main__":
    main()
