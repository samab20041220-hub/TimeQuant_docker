FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ gfortran libopenblas-dev liblapack-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir 'cython<3' 'numpy<2' 'scipy<1.14' sympy matplotlib ase \
    && pip install --no-cache-dir --no-build-isolation tinyarray mpi4py kwant kwantspectrum tkwant
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "/usr/local/bin/python3"]
