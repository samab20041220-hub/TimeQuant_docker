FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir mace-torch ase torch-geometric
RUN mkdir -p /opt/models && \
    python3 -c "from mace.calculators import mace_mp; mace_mp(model='medium', default_dtype='float32')" || true
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
