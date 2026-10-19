FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git libxc-dev libxc9 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pybind11 numpy scipy ase
RUN mkdir -p /root/.gpaw && \
    echo 'libxc = True' > /root/.gpaw/siteconfig.py && \
    echo 'libraries += ["xc"]' >> /root/.gpaw/siteconfig.py && \
    pip install --no-cache-dir --no-binary gpaw --no-build-isolation gpaw
RUN mkdir -p /workspace /opt/gpaw-setups \
    && gpaw -P 1 install-data /opt/gpaw-setups || true
ENV GPAW_SETUP_PATH=/opt/gpaw-setups
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace /opt/gpaw-setups
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh"]
CMD ["gpaw"]
