# LXC K3s Terraform Configuration

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fdurianlab.tech)](https://durianlab.tech) [![GitHub issues](https://img.shields.io/github/issues/DurianLAB/terraform.svg)](https://github.com/DurianLAB/terraform/issues) [![GitHub pull requests](https://img.shields.io/github/issues-pr/DurianLAB/terraform.svg)](https://github.com/DurianLAB/terraform/pulls) [![License: Custom](https://img.shields.io/badge/License-Custom%20Non--Commercial-blue.svg)](https://github.com/DurianLAB/terraform/blob/main/LICENSE) [![Last commit](https://img.shields.io/github/last-commit/DurianLAB/terraform.svg)](https://github.com/DurianLAB/terraform/commits/main)

This repository contains Terraform configurations for deploying K3s clusters in LXD virtual machines with two different networking scenarios.

## License

This project is licensed under a Custom Non-Commercial License - see the [LICENSE](LICENSE) file for details. This license allows free sharing and modification for non-commercial use but prohibits commercial sale or commercial exploitation.

Developed by [DurianLAB](https://durianlab.tech/).

## Repository Structure

```
├── terraform/                 # Git submodule - DurianLAB/terraform
│   ├── scenarios/
│   │   ├── bridge-networking/     # Development scenario with bridge networks
│   │   └── macvlan-networking/    # Production scenario with macvlan networks
│   ├── test-macvlan-*.sh          # Connectivity testing scripts
│   └── TROUBLESHOOTING.md         # Network configuration troubleshooting
├── fabfile.py                 # Fabric automation tasks
└── README.md                  # This file
```

## Fabric Automation

This repository includes [Fabric](https://www.fabfile.org/) automation tasks to simplify Terraform operations. **All Terraform commands run on a remote host via SSH**, allowing you to manage infrastructure from your local machine.

### Prerequisites

**Local Machine:**
```bash
pip install fabric
```

**Remote Host (where Terraform/LXD runs):**
- Ubuntu/Debian Linux
- Terraform >= 1.0
- LXD installed and configured
- SSH access with your user
- SSH public key at `~/fabric/terraform/id_ed25519.pub`

### Configuration

Set environment variables or pass parameters:

```bash
# Option 1: Environment variables
export TF_HOST=192.168.1.100
export TF_USER=ubuntu

# Option 2: Command line parameters
fab apply --scenario=bridge-networking --env=dev --host=192.168.1.100 --user=ubuntu
```

### First Time Setup

1. **Setup the remote machine** (one-time):
   ```bash
   fab setup --host=192.168.1.100 --user=ubuntu
   ```

2. **Initialize and deploy**:
   ```bash
   fab init apply --scenario=bridge-networking --env=dev
   ```

### Available Fabric Tasks

| Task | Description | Example |
|------|-------------|---------|
| `setup` | Setup remote host and clone repo | `fab setup --host=192.168.1.100` |
| `init` | Initialize Terraform | `fab init --scenario=bridge-networking` |
| `plan` | Plan Terraform changes | `fab plan --scenario=bridge-networking --env=dev` |
| `apply` | Apply Terraform changes | `fab apply --scenario=macvlan-networking --env=prod` |
| `destroy` | Destroy infrastructure | `fab destroy --scenario=bridge-networking --env=dev` |
| `validate` | Validate configuration | `fab validate --scenario=bridge-networking` |
| `test` | Run connectivity tests | `fab test --scenario=macvlan-networking` |
| `deploy-all` | Deploy to all environments | `fab deploy-all --scenario=bridge-networking` |
| `status` | Check deployment status | `fab status` |
| `logs` | View K3s logs | `fab logs --env=dev` |
| `shell` | Open shell in container | `fab shell --env=dev` |
| `update-submodule` | Update terraform code | `fab update-submodule` |

### Quick Start with Fabric (Remote)

**1. Configure Remote Host:**
```bash
# Set environment variables
export TF_HOST=192.168.1.100      # Your LXD/Terraform server
export TF_USER=ubuntu              # SSH username
```

**2. First Time Setup (Remote Machine):**
```bash
# This clones the repo and installs dependencies on remote host
fab setup
```

**3. Deploy Infrastructure:**
```bash
# Initialize and deploy bridge networking (development)
fab init --scenario=bridge-networking
fab apply --scenario=bridge-networking --env=dev

# Deploy production with macvlan networking
fab init --scenario=macvlan-networking
fab apply --scenario=macvlan-networking --env=prod

# Run validation and tests
fab validate --scenario=bridge-networking
fab test --scenario=bridge-networking
```

**4. Monitor and Manage:**
```bash
# Check deployment status
fab status

# View K3s logs
fab logs --env=dev

# Open shell in container
fab shell --env=dev
```

### Setup with Git Submodules

This project uses the [DurianLAB/terraform](https://github.com/DurianLAB/terraform) repository as a git submodule.

**Clone with submodules:**
```bash
git clone --recurse-submodules <your-repo-url>
```

**Or if already cloned:**
```bash
git submodule update --init --recursive
```

**Update submodule to latest:**
```bash
git submodule update --remote
```

## Networking Scenarios

### Bridge Networking (`scenarios/bridge-networking/`)

- **Use Case**: Development and testing environments
- **Network Type**: LXD bridge with NAT
- **Host Access**: Direct communication with VMs
- **External Access**: Requires port forwarding
- **IP Range**: Isolated subnet (10.150.x.x)

### Macvlan Networking (`scenarios/macvlan-networking/`)

- **Use Case**: Production deployments
- **Network Type**: LXD macvlan for direct access
- **Host Access**: Isolated from host (L2 limitation)
- **External Access**: Direct from network clients
- **IP Range**: Host subnet (192.168.1.x)

## Features

- Multi-environment support with Terraform workspaces
- Deploys LXC virtual machines with Ubuntu 22.04
- Installs and configures K3s
- Two complete networking scenarios
- Configurable CPU, memory, and storage
- Cloud-init for initial setup and SSH access
- **Fabric automation for streamlined deployments**

## Prerequisites

**Local Machine (Your Laptop/Workstation):**
- Python >= 3.6
- Fabric (`pip install fabric`)
- SSH key configured for remote host access

**Remote Host (Terraform/LXD Server):**
- Ubuntu/Debian Linux (or compatible)
- Terraform >= 1.0
- LXD installed and configured
- Git (for cloning/updating)
- SSH public key for ansible user (will be generated during setup)

## Quick Start

### Remote Deployment Workflow

1. **Configure your remote host:**
   ```bash
   export TF_HOST=192.168.1.100  # Your LXD/Terraform server
   export TF_USER=ubuntu
   ```

2. **Setup remote machine** (one-time):
   ```bash
   fab setup
   ```

3. **Choose your networking scenario and deploy:**
   - **Development**: `--scenario=bridge-networking`
   - **Production**: `--scenario=macvlan-networking`

4. **Deploy with Fabric:**
   ```bash
   fab init apply --scenario=bridge-networking --env=dev
   ```

### Using Fabric (Recommended)

```bash
# Set remote host (or use --host/--user flags)
export TF_HOST=192.168.1.100
export TF_USER=ubuntu

# First time setup on remote machine
fab setup

# One-line deployment
fab init apply --scenario=bridge-networking --env=dev

# Full workflow with validation
fab init validate plan apply test --scenario=macvlan-networking --env=prod

# Update terraform module to latest on remote
fab update-submodule

# Check what's running
fab status
```

### Bridge Scenario (`scenarios/bridge-networking/`)

See `scenarios/bridge-networking/README.md` for detailed information.

### Macvlan Scenario (`scenarios/macvlan-networking/`)

See `scenarios/macvlan-networking/README.md` for detailed information.

## Testing and Verification

### Manual Testing

```bash
# Use the provided test scripts
./test-macvlan-connectivity.sh
./test-external-connectivity.sh
./vm-connectivity-test.sh
```

### Automated Testing with Fabric

```bash
# Run all tests for a scenario
fab test --scenario=macvlan-networking
```

### Manual Verification

After deployment, verify with:

```bash
# Check VM status
lxc list | grep k3s

# Verify K3s service
lxc exec k3s-{env}-cluster-01 -- systemctl status k3s

# Check network configuration
lxc network show k3s-{env}-net
```

## Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ssh_public_key` | SSH public key for ansible user | Yes |

## Outputs

| Output | Description |
|--------|-------------|
| `k3s_node_ip` | IPv4 address of the K3s node |
| `check_commands` | Commands to verify K3s and SSH setup |

### Current Network Configuration

The current deployment uses macvlan networks. To verify:

```bash
# Check network type
lxc network show k3s-{env}-net | grep "type:"

# Check VM IP assignment
lxc list | grep k3s-{env}-cluster-01
```

## Verification

After deployment, use the provided check commands to verify:

- K3s service is running
- SSH key is properly configured

```bash
# Check K3s status (replace {env} with your workspace)
lxc exec k3s-{env}-cluster-01 -- systemctl status k3s

# Verify SSH access
lxc exec k3s-{env}-cluster-01 -- cat /home/ansible/.ssh/authorized_keys
```

### Macvlan Network Testing

For macvlan network deployments, use the provided test scripts to verify network connectivity and service accessibility:

```bash
# Run the connectivity test script
./test-macvlan-connectivity.sh

# Test from external clients on the network
./test-external-connectivity.sh

# Run comprehensive test inside VM
./vm-connectivity-test.sh
```

The test scripts verify:

- VM network configuration and routing
- External connectivity to gateway and internet
- Service availability (SSH, K3s)
- Host isolation (expected macvlan behavior)

Note: These tests are specific to macvlan deployments where VMs need direct external network access.

## Security Notes

- SSH password authentication is disabled
- Ansible user has sudo privileges with no password
- Update the SSH key in cloud_config before deployment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Important Notes

- **Scenario Isolation**: Each scenario folder (`bridge-networking`, `macvlan-networking`) contains completely separate Terraform configurations with their own state files
- **No Switching Required**: Choose the appropriate scenario folder for your use case - no manual switching needed
- **Testing Scripts**: The test scripts in the root directory work with both scenarios
- **Network Conflicts**: Do not deploy both scenarios simultaneously as they may create conflicting networks

## Troubleshooting

- Ensure LXD has permissions to create networks
- Check that the storage pool exists
- Use `terraform workspace list` to see available environments
- For network configuration issues, see TROUBLESHOOTING.md

## Fabric Troubleshooting

### Connection Issues
- **"Please set TF_HOST environment variable"**: Set `export TF_HOST=<remote-ip>` or use `--host=<ip>`
- **"Please set TF_USER environment variable"**: Set `export TF_USER=<username>` or use `--user=<username>`
- **SSH connection refused**: Ensure remote host is reachable and SSH is running
- **Permission denied**: Add your SSH key to remote host: `ssh-copy-id user@host`

### Remote Execution Issues
- **Terraform not found**: Run `fab setup` to ensure Terraform is installed on remote
- **LXD not found**: Install LXD on remote: `snap install lxd` or `apt install lxd`
- **"No such file or directory"**: Run `fab setup` first to clone the repo on remote
- **Terraform workspace errors**: Run `fab init` first before other commands

### General Issues
- **Fabric not found**: Install with `pip install fabric`
- **Submodule issues**: Run `fab update-submodule` to sync latest terraform code
