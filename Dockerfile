FROM debian:13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
    # SSH-Server (Gateway connectet via SSH)
    openssh-server \
    # Dev-Tools
    git curl wget ca-certificates gnupg \
    build-essential \
    openjdk-21-jdk \
    maven \
    python3 python3-pip python3-venv \
    ripgrep \
    # JetBrains Remote-Backend braucht das
    libxext6 libxrender1 libxtst6 libxi6 libfreetype6 \
    procps \
    sudo nano \
    tmux \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Node.js + openclaude
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

#Opencode
RUN curl -fsSL https://opencode.ai/install | bash \
    && cp /root/.opencode/bin/opencode /usr/local/bin/opencode \
    && chmod +x /usr/local/bin/opencode \
    && /usr/local/bin/opencode --version

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    pipx \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3 /usr/local/bin/python

# User
ARG USERNAME=dev
RUN useradd -m -s /bin/bash ${USERNAME} \
    && usermod -aG sudo ${USERNAME} \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && mkdir -p /home/${USERNAME}/.ssh \
    && chmod 700 /home/${USERNAME}/.ssh \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.ssh

# SSH-Server vorbereiten
RUN mkdir -p /var/run/sshd \
    && printf 'PasswordAuthentication no\nPermitRootLogin no\nPubkeyAuthentication yes\n' \
       > /etc/ssh/sshd_config.d/99-hardening.conf

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
