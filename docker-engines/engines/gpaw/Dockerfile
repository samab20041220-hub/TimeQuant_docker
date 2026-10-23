FROM mambaorg/micromamba:latest
USER root
ENV HOME=/tmp
RUN micromamba install -y -n base -c conda-forge gpaw ase scipy && micromamba clean --all --yes
ENV PATH="/opt/conda/bin:$PATH"
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
