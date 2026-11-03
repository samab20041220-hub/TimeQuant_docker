FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir numpy scipy ase
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
