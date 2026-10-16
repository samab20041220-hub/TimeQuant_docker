FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir mace-torch ase torch-geometric
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]
