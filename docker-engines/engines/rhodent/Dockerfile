FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV CC="g++"
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir torch-scatter -f https://data.pyg.org/whl/torch-2.5.1+cpu.html \
    && pip install --no-cache-dir rhodent e3nn
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]
