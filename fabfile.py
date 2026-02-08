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

@task
def setup(c):
    """Initial setup - initialize git submodules"""
    c.run("git submodule update --init --recursive")
    print("✓ Submodule initialized successfully")
    print("\nYou can now use Fabric tasks:")
    print("  fab init --scenario=bridge-networking")
    print("  fab apply --scenario=bridge-networking --env=dev")
