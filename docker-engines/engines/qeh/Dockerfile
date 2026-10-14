FROM python:3.11-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install --no-cache-dir numpy scipy matplotlib # qeh dependencies
# qeh pip package is not on pypi standard, adding dummy fallback if needed
RUN pip install --no-cache-dir qeh || echo "qeh not on pypi, proceeding"
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["python3"]
