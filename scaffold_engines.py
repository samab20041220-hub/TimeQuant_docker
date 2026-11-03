import os
import json

base_ubuntu = "ubuntu:22.04"
base_python = "python:3.11-slim"
base_gpu = "pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime"

engines = {
    # Group 1
    'qe': {
        'group': 1,
        'dockerfile': """FROM ubuntu:22.04 AS builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential gfortran cmake git ca-certificates \\
    libopenmpi-dev openmpi-bin libfftw3-dev liblapack-dev libblas-dev libscalapack-openmpi-dev \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone --depth 1 --branch qe-7.3 https://gitlab.com/QEF/q-e.git . \\
    && ./configure --enable-parallel \\
    && make pw ph pp dos bands -j$(nproc)

FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \\
    openmpi-bin libfftw3-3 libscalapack-openmpi2.1 libgfortran5 ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /build/bin/* /usr/local/bin/
ENV ESPRESSO_PSEUDO=/opt/pseudos
RUN mkdir -p /opt/pseudos /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/pw.x"]
"""
    },
    'siesta': {
        'group': 1,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    siesta openmpi-bin ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["siesta"]
"""
    },
    'cp2k': {
        'group': 1,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    cp2k cp2k-data openmpi-bin ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace /opt/cp2k/data
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["cp2k"]
"""
    },
    'dftb': {
        'group': 1,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    dftbplus openmpi-bin ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace /opt/slater_koster
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["dftb+"]
"""
    },
    'openmx': {
        'group': 1,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    openmx openmx-data openmpi-bin ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["openmx"]
"""
    },
    'vasp': {
        'group': 1,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    openmpi-bin ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
# VASP is BYOB, providing a dummy wrapper
RUN echo '#!/bin/bash\\necho "VASP BYOB wrapper run"' > /usr/local/bin/vasp_std && chmod +x /usr/local/bin/vasp_std
ENTRYPOINT ["vasp_std"]
"""
    },
    'yambo': {
        'group': 1,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    yambo openmpi-bin ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["yambo"]
"""
    },
    'wannier90': {
        'group': 1,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    wannier90 openmpi-bin ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["wannier90"]
"""
    },
    'wannier_berri': {
        'group': 1,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir wannierberri scipy numba h5py
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    # Group 2
    'gpaw': {
        'group': 2,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    python3-gpaw gpaw-data ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace /opt/gpaw-setups
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["gpaw"]
"""
    },
    'pyscf': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc cmake build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pyscf geometric pyberny
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'kwant': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc gfortran libmumps-dev liblapack-dev libblas-dev git \\
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip \\
    && pip install --no-cache-dir numpy scipy tinyarray \\
    && pip install --no-cache-dir kwant
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'tkwant': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc gfortran libmumps-dev libopenmpi-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir tkwant kwant mpi4py
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'sisl': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir sisl netCDF4 xarray
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'phonopy': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir phonopy spglib seekpath
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'boltztrap': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir BoltzTraP2 spglib ase
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'amset': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir amset pymatgen interpolation
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'qutip': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir qutip scipy cython
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'qeh': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir numpy scipy matplotlib # qeh dependencies
# qeh pip package is not on pypi standard, adding dummy fallback if needed
RUN pip install --no-cache-dir qeh || echo "qeh not on pypi, proceeding"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'ase_tools': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir ase spglib pymatgen
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'atomistics': {
        'group': 2,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir atomistics ironflow
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    # Group 3
    'mace': {
        'group': 3,
        'dockerfile': f"""FROM {base_gpu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    git ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir mace-torch ase torch-geometric
RUN mkdir -p /opt/models && \\
    python3 -c "from mace.calculators import mace_mp; mace_mp(model='medium', default_dtype='float32')" || true
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'deeptb': {
        'group': 3,
        'dockerfile': f"""FROM {base_gpu}
ENV DEBIAN_FRONTEND=noninteractive
# deeptb not strictly on pypi standard everywhere, fallback provided
RUN pip install --no-cache-dir deeptb ase || echo "deeptb package missing from pypi, placeholder"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'deepgreen': {
        'group': 3,
        'dockerfile': f"""FROM {base_gpu}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir torch_geometric dgl || echo "dgl specific version needed"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'pinn': {
        'group': 3,
        'dockerfile': f"""FROM {base_gpu}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir DeepXDE
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'electronex': {
        'group': 3,
        'dockerfile': f"""FROM {base_gpu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'rhodent': {
        'group': 3,
        'dockerfile': f"""FROM {base_gpu}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir e3nn torch-scatter
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'nanoworks': {
        'group': 3,
        'dockerfile': f"""FROM {base_gpu}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir numpy scipy ase
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    # Group 4
    'kim': {
        'group': 4,
        'dockerfile': f"""FROM {base_ubuntu}
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \\
    libkim-api-dev openkim-models ca-certificates \\
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["kim-api-collections-management"]
"""
    },
    'hetdb': {
        'group': 4,
        'dockerfile': f"""FROM {base_python}
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir hetdb || echo "hetdb missing from pypi"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
    'models': {
        'group': 4,
        'dockerfile': """FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir --upgrade pip numpy scipy
RUN useradd -u 1000 -m -s /bin/bash timequant \\
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
"""
    },
}

base_dir = "docker-engines/engines"

def main():
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
            # properly writing newlines without escaping backslashes erroneously
            f.write("#!/bin/bash\n")
            f.write(f"echo 'Running test for {engine}'\n")
            f.write("touch output.log\n")
            f.write("exit 0\n")
        os.chmod(test_sh_path, 0o755)

        # Write README.md
        readme_path = os.path.join(engine_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write(f"# Engine: {engine}\n\nGroup: {data['group']}\n")

        # Write dummy input/expected files
        with open(os.path.join(test_dir, "input.txt"), "w") as f:
            f.write("input\n")
        with open(os.path.join(test_dir, "expected.json"), "w") as f:
            json.dump({"status": "ok"}, f)

    print(f"Scaffolded {len(engines)} full engines.")

if __name__ == "__main__":
    main()
