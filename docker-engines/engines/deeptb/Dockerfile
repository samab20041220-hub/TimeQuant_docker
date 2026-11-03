FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive
# deeptb not strictly on pypi standard everywhere, fallback provided
RUN pip install --no-cache-dir deeptb ase || echo "deeptb package missing from pypi, placeholder"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
