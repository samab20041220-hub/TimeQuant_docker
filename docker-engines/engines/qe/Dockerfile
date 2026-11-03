FROM ubuntu:22.04 AS builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gfortran cmake git ca-certificates \
    libopenmpi-dev openmpi-bin libfftw3-dev liblapack-dev libblas-dev libscalapack-openmpi-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build
RUN git clone --depth 1 --branch qe-7.3 https://gitlab.com/QEF/q-e.git . \
    && ./configure --enable-parallel \
    && make pw ph pp dos bands -j$(nproc)

FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    openmpi-bin libfftw3-3 libscalapack-openmpi2.1 libgfortran5 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /build/bin/* /usr/local/bin/
ENV ESPRESSO_PSEUDO=/opt/pseudos
RUN mkdir -p /opt/pseudos /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/pw.x"]
