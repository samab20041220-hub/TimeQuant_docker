FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-gpaw gpaw-data ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace /opt/gpaw-setups
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["gpaw"]
