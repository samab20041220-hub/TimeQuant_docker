FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    quantum-espresso quantum-espresso-data openmpi-bin ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ENV ESPRESSO_PSEUDO=/opt/pseudos
RUN mkdir -p /opt/pseudos /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/usr/bin/pw.x"]
