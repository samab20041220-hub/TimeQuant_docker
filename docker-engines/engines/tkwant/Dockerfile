FROM python:3.11-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc gfortran libmumps-dev libopenmpi-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir tkwant kwant mpi4py
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
