FROM python:3.11-slim
FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc gfortran libmumps-dev liblapack-dev libblas-dev git \
    build-essential cmake git gfortran libmumps-dev liblapack-dev libblas-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir numpy scipy tinyarray \
    && pip install --no-cache-dir kwant
RUN pip install --no-cache-dir "numpy<2" scipy tinyarray kwant
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]
