FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir electronex numpy scipy matplotlib cython
RUN mkdir -p /workspace /opt/electronex
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]
