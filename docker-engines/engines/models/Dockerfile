FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir --upgrade pip numpy scipy
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && mkdir -p /workspace && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
