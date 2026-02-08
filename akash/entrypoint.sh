#!/bin/bash
set -e

echo "=== Starting Akash Fabric Manager ==="

# Start Tailscale in background
echo "Starting Tailscale..."
if [ -n "$TAILSCALE_AUTH_KEY" ]; then
    tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock &
    sleep 2
    tailscale up --authkey="$TAILSCALE_AUTH_KEY" --hostname="akash-fabric-manager" --accept-routes
    echo "✓ Tailscale connected"
    echo "Tailscale IP: $(tailscale ip -4)"
else
    echo "⚠ WARNING: TAILSCALE_AUTH_KEY not set, Tailscale will not start"
fi

# Setup SSH keys if provided
if [ -n "$SSH_PRIVATE_KEY" ]; then
    echo "Setting up SSH keys..."
    mkdir -p /home/git/.ssh
    echo "$SSH_PRIVATE_KEY" > /home/git/.ssh/id_ed25519
    chmod 600 /home/git/.ssh/id_ed25519
    chown -R git:git /home/git/.ssh
    echo "✓ SSH keys configured"
fi

# Clone terraform repo if not exists
if [ ! -d "$TERRAFORM_DIR" ]; then
    echo "Cloning terraform repository..."
    cd /home/git
    git clone --recurse-submodules https://github.com/DurianLAB/terraform.git terraform || true
    chown -R git:git terraform
    echo "✓ Terraform repo cloned"
fi

# Start SSH server for Git
echo "Starting SSH server on port 2222..."
/usr/sbin/sshd -D &
SSHD_PID=$!
echo "✓ SSH server started (PID: $SSHD_PID)"

# Display connection info
echo ""
echo "=========================================="
echo "  Akash Fabric Manager is running!"
echo "=========================================="
echo ""
echo "Git Repository: ssh://git@<akash-uri>:2222/home/git/fabric.git"
echo "Tailscale IP: $(tailscale ip -4 2>/dev/null || echo 'Not connected')"
echo ""
echo "To push and deploy:"
echo "  git remote add akash ssh://git@<akash-uri>:2222/home/git/fabric.git"
echo "  git push akash main"
echo ""
echo "=========================================="

# Keep container running
wait $SSHD_PID
