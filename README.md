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

This repository includes [Fabric](https://www.fabfile.org/) automation tasks to simplify Terraform operations. Fabric provides a Pythonic way to automate deployment workflows.

### Prerequisites

```bash
pip install fabric
```

### Available Fabric Tasks

| Task | Description | Example |
|------|-------------|---------|
| `init` | Initialize Terraform | `fab init --scenario=bridge-networking` |
| `plan` | Plan Terraform changes | `fab plan --scenario=bridge-networking --env=dev` |
| `apply` | Apply Terraform changes | `fab apply --scenario=macvlan-networking --env=prod` |
| `destroy` | Destroy infrastructure | `fab destroy --scenario=bridge-networking --env=dev` |
| `validate` | Validate configuration | `fab validate --scenario=bridge-networking` |
| `test` | Run connectivity tests | `fab test --scenario=macvlan-networking` |
| `deploy-all` | Deploy to all environments | `fab deploy-all --scenario=bridge-networking` |

### Quick Start with Fabric

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

### Fabric Task File

Create a `fabfile.py` in the repository root:

```python
from fabric import task

TERRAFORM_DIR = "terraform"

@task
def init(c, scenario="bridge-networking"):
    """Initialize Terraform for the specified scenario"""
    with c.cd(f"{TERRAFORM_DIR}/scenarios/{scenario}"):
        c.run("terraform init")

@task
def plan(c, scenario="bridge-networking", env="dev"):
    """Plan Terraform changes"""
    with c.cd(f"{TERRAFORM_DIR}/scenarios/{scenario}"):
        c.run(f"terraform workspace select {env} || terraform workspace new {env}")
        c.run(f"terraform plan -var='ssh_public_key=$(cat ../../../id_ed25519.pub)'")

@task
def apply(c, scenario="bridge-networking", env="dev", auto_approve=False):
    """Apply Terraform changes"""
    with c.cd(f"{TERRAFORM_DIR}/scenarios/{scenario}"):
        c.run(f"terraform workspace select {env}")
        auto = "-auto-approve" if auto_approve else ""
        c.run(f"terraform apply {auto} -var='ssh_public_key=$(cat ../../../id_ed25519.pub)'")

@task
def destroy(c, scenario="bridge-networking", env="dev"):
    """Destroy Terraform infrastructure"""
    with c.cd(f"{TERRAFORM_DIR}/scenarios/{scenario}"):
        c.run(f"terraform workspace select {env}")
        c.run("terraform destroy -var='ssh_public_key=$(cat ../../../id_ed25519.pub)'")

@task
def validate(c, scenario="bridge-networking"):
    """Validate Terraform configuration"""
    with c.cd(f"{TERRAFORM_DIR}/scenarios/{scenario}"):
        c.run("terraform validate")
        c.run("terraform fmt -check")

@task
def test(c, scenario="bridge-networking"):
    """Run connectivity tests"""
    with c.cd(TERRAFORM_DIR):
        if scenario == "macvlan-networking":
            c.run("./test-macvlan-connectivity.sh")
            c.run("./test-external-connectivity.sh")
        c.run("./vm-connectivity-test.sh")

@task
def deploy_all(c, scenario="bridge-networking"):
    """Deploy to dev, staging, and prod sequentially"""
    for env in ["dev", "staging", "prod"]:
        print(f"\n{'='*50}")
        print(f"Deploying to {env} environment...")
        print(f"{'='*50}\n")
        init(c, scenario)
        apply(c, scenario, env, auto_approve=True)

@task
def update_submodule(c):
    """Update terraform submodule to latest version"""
    c.run("git submodule update --remote")
    c.run("git status")
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

- Terraform >= 1.0
- LXD installed and configured on the host
- SSH key for ansible user access
- Python >= 3.6 (for Fabric automation)
- Fabric (`pip install fabric`)

## Quick Start

1. Choose your networking scenario:
   - **Development**: `cd scenarios/bridge-networking`
   - **Production**: `cd scenarios/macvlan-networking`

2. Initialize and deploy:
   ```bash
   terraform init
   terraform workspace select <env>  # dev, staging, or prod
   terraform plan -var="ssh_public_key=$(cat ../../id_ed25519.pub)"
   terraform apply -var="ssh_public_key=$(cat ../../id_ed25519.pub)"
   ```

### Using Fabric (Recommended)

```bash
# First, ensure submodule is initialized
git submodule update --init --recursive

# One-line deployment
fab init apply --scenario=bridge-networking --env=dev

# Full workflow with validation
fab init validate plan apply test --scenario=macvlan-networking --env=prod

# Update terraform module to latest
fab update-submodule
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

- **Fabric not found**: Install with `pip install fabric`
- **Permission denied**: Ensure SSH keys are properly configured
- **Terraform workspace errors**: Run `fab init` first before other commands
- **Connection errors**: Verify LXD is running: `lxc list`
