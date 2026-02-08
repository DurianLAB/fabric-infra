# Akash GitOps Management Plane

This setup creates a decentralized management plane on Akash that securely manages your home LXD/KVM infrastructure via Tailscale VPN.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Your Laptop (Developer)                                     │
│  └── git push → Akash Container                             │
└───────────────────────┬─────────────────────────────────────┘
                        │ Public Internet
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  Akash Container (The "Brain")                              │
│  ├── Git Server (bare repo)                                 │
│  ├── Tailscale Client (100.x.y.z)                          │
│  ├── Fabric Automation                                      │
│  └── post-receive hook triggers deployment                  │
└──────────┬──────────────────────────────────────────────────┘
           │ Tailscale VPN (WireGuard)
           ▼
┌─────────────────────────────────────────────────────────────┐
│  Home LXD Host (The "Brawn")                                │
│  ├── Tailscale Client (100.x.y.z)                          │
│  ├── LXD/KVM Hypervisor                                     │
│  └── Terraform applies infrastructure                       │
└─────────────────────────────────────────────────────────────┘
```

## Why This Works

1. **No exposed ports** on your home network
2. **GitOps workflow** - push to deploy
3. **Always-on management** plane ($1-2/month on Akash)
4. **Secure** - Tailscale WireGuard encryption
5. **Flexible** - Access from anywhere via Akash

## Quick Start

### 1. Deploy to Akash

```bash
# Install Akash CLI and configure
# See: https://docs.akash.network/guides/cli

# Create deployment
akash tx deployment create deploy.yml --from $KEY_NAME --chain-id $CHAIN_ID

# Get lease and URI
akash query market lease list --owner $ACCOUNT_ADDRESS
```

### 2. Configure Tailscale

On Akash container (auto-starts via entrypoint):
- Auth key provided via `TAILSCALE_AUTH_KEY` env var
- Container joins your tailnet automatically

On Home LXD Host:
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Get your home IP
tailscale ip -4
# Output: 100.x.y.z (use this in fabfile.py)
```

### 3. Configure SSH Access

```bash
# On home LXD host, add Akash container's SSH key
cat ~/.ssh/id_ed25519.pub | ssh user@home-host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Copy private key to Akash (via env var in deploy.yml)
# Never commit keys to git!
```

### 4. Push and Deploy

```bash
# Add Akash Git remote
git remote add akash ssh://git@akash-uri:2222/home/git/fabric.git

# Push to trigger deployment
git push akash main
```

## File Structure

```
.
├── Dockerfile              # Akash container image
├── deploy.yml              # Akash deployment manifest
├── entrypoint.sh           # Container startup script
├── fabfile.py              # Fabric automation (runs in Akash)
├── hooks/
│   └── post-receive        # Git trigger
└── README.md               # This file
```

## Security Considerations

1. **Tailscale** - Uses WireGuard, no exposed ports
2. **SSH Keys** - Passed via Akash env vars, never in git
3. **Git Server** - Runs on non-standard port (2222)
4. **State** - Terraform state stays on home machine
5. **Network** - Home network isolated from internet

## Cost Breakdown

- **Akash Container**: ~$1-2/month (1 CPU, 1GB RAM, 5GB storage)
- **Tailscale**: Free for personal use (up to 20 devices)
- **Total**: $1-2/month for always-on management plane

## Troubleshooting

### Tailscale not connecting
```bash
# Check logs in Akash container
tailscale status
journalctl -u tailscaled
```

### Git push failing
```bash
# Test SSH from local machine
ssh -p 2222 git@akash-uri

# Check git server logs in container
cat /var/log/git-server.log
```

### Fabric connection issues
```bash
# Test from Akash container
fab test-connection --host=100.x.y.z --user=homeuser

# Verify Tailscale connectivity
ping 100.x.y.z
```

## Updates and Maintenance

### Update Akash Container
```bash
# Build new image
docker build -t yourrepo/fabric-manager:latest .
docker push yourrepo/fabric-manager:latest

# Update Akash deployment with new image
```

### Update Terraform Code
```bash
# Just push to Akash - post-receive updates submodule
git push akash main
```

## Advanced Features

- **Multi-host management** - Manage multiple LXD hosts
- **CI/CD integration** - GitHub Actions → Akash → Home
- **Monitoring** - Prometheus/Grafana in Akash container
- **Backups** - Automated state backups to S3/MinIO

## References

- [Akash Documentation](https://docs.akash.network/)
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Fabric Documentation](https://www.fabfile.org/)
- [Terraform Documentation](https://www.terraform.io/docs)
