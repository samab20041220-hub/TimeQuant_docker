FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV CMAKE_POLICY_VERSION_MINIMUM=3.5
ENV CFLAGS="-fPIC"
ENV CXXFLAGS="-fPIC -include cmath"
RUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pybind11
RUN pip install --no-cache-dir hetbuilder ase pymatgen
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "python3"]
