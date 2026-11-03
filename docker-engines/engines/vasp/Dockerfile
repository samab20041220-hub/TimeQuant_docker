FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    openmpi-bin ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
USER timequant
WORKDIR /workspace
# VASP is BYOB, providing a dummy wrapper
RUN echo '#!/bin/bash\necho "VASP BYOB wrapper run"' > /usr/local/bin/vasp_std && chmod +x /usr/local/bin/vasp_std
ENTRYPOINT ["vasp_std"]
