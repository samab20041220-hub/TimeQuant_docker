FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/tmp
ENV DDE_BACKEND=pytorch
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir DeepXDE
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]
