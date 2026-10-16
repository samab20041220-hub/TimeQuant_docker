FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    openmpi-bin ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /workspace
RUN useradd -u 1000 -m -s /bin/bash timequant \
    && chown -R timequant:timequant /workspace
# VASP is BYOB: placeholder binary, to be replaced by the licensed vasp_std
RUN printf '#!/bin/bash\necho "VASP BYOB wrapper run"\n' > /usr/local/bin/vasp_std && chmod 755 /usr/local/bin/vasp_std
COPY common/entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod 755 /usr/local/bin/entrypoint-wrapper.sh
USER timequant
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh", "vasp_std"]
