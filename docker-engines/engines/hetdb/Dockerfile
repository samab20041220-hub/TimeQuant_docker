FROM python:3.11-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir hetdb || echo "hetdb missing from pypi"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
