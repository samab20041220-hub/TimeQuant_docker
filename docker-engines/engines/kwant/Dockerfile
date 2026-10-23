FROM mambaorg/micromamba:latest
USER root
ENV HOME=/tmp
RUN micromamba install -y -n base -c conda-forge kwant python=3.10 numpy scipy tinyarray matplotlib && micromamba clean --all --yes
ENV PATH="/opt/conda/bin:$PATH"
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/opt/conda/bin/python3"]
