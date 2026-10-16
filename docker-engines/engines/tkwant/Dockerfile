FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git gfortran libmumps-dev liblapack-dev libblas-dev libopenmpi-dev openmpi-bin \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "numpy<2" scipy tinyarray kwant mpi4py sympy
RUN pip install --no-cache-dir tkwant
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]
