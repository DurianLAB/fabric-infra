FROM ubuntu:22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install base dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    openssh-server \
    python3 \
    python3-pip \
    jq \
    vim \
    sudo \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Terraform
RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list \
    && apt-get update \
    && apt-get install -y terraform \
    && rm -rf /var/lib/apt/lists/*

# Install Tailscale
RUN curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/$(lsb_release -cs).noarmor.gpg | tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null \
    && curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/$(lsb_release -cs).tailscale-keyring.list | tee /etc/apt/sources.list.d/tailscale.list \
    && apt-get update \
    && apt-get install -y tailscale \
    && rm -rf /var/lib/apt/lists/*

# Install Fabric
RUN pip3 install fabric invoke

# Install TFLint
RUN curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Create git user
RUN useradd -m -s /bin/bash git \
    && mkdir -p /home/git/.ssh \
    && chown -R git:git /home/git

# Setup SSH server for Git
RUN mkdir -p /var/run/sshd \
    && echo 'Port 2222' >> /etc/ssh/sshd_config \
    && echo 'PermitRootLogin no' >> /etc/ssh/sshd_config \
    && echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config \
    && echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config \
    && echo 'AllowUsers git' >> /etc/ssh/sshd_config

# Create bare git repository
RUN mkdir -p /home/git/fabric.git \
    && cd /home/git/fabric.git \
    && git init --bare \
    && chown -R git:git /home/git/fabric.git

# Copy hooks
COPY hooks/post-receive /home/git/fabric.git/hooks/post-receive
RUN chmod +x /home/git/fabric.git/hooks/post-receive \
    && chown git:git /home/git/fabric.git/hooks/post-receive

# Copy Fabric tasks
COPY fabfile.py /home/git/
RUN chown -R git:git /home/git/fabfile.py

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Environment variables (will be set via Akash SDL)
ENV TAILSCALE_AUTH_KEY=""
ENV HOME_LXD_HOST=""
ENV HOME_LXD_USER=""
ENV SSH_PRIVATE_KEY=""
ENV TERRAFORM_DIR="/home/git/terraform"

# Expose Git SSH port
EXPOSE 2222

# Start services via entrypoint
ENTRYPOINT ["/entrypoint.sh"]
