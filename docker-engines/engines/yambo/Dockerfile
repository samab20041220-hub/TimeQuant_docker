FROM mambaorg/micromamba:latest
USER root
RUN micromamba install -y -n base -c conda-forge yambo && micromamba clean --all --yes
ENV PATH="/opt/conda/bin:$PATH"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/opt/conda/bin/yambo"]
