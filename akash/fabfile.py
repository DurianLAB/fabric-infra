from fabric import Connection, task, Config
import os

# Configuration
TERRAFORM_DIR = "terraform"
DEFAULT_HOST = os.environ.get('TF_HOST', 'your-remote-host')
DEFAULT_USER = os.environ.get('TF_USER', 'your-username')

def get_connection(host=None, user=None):
    """Create SSH connection to remote host"""
    host = host or DEFAULT_HOST
    user = user or DEFAULT_USER
    
    if host == 'your-remote-host':
        raise ValueError("Please set TF_HOST environment variable or pass --host parameter")
    if user == 'your-username':
        raise ValueError("Please set TF_USER environment variable or pass --user parameter")
    
    return Connection(host=host, user=user)

@task
def setup(c, host=None, user=None):
    """Initial setup on remote machine - clone repo and initialize"""
    conn = get_connection(host, user)
    
    with conn:
        # Check if terraform is installed
        conn.run("terraform --version", hide=True)
        
        # Check if lxd is installed
        conn.run("lxd --version", hide=True)
        
        # Clone or update repository
        conn.run("""
            if [ -d ~/fabric ]; then
                cd ~/fabric && git pull
            else
                git clone --recurse-submodules https://github.com/your-username/fabric.git ~/fabric
            fi
        """)
        
        # Initialize submodule
        conn.run("cd ~/fabric && git submodule update --init --recursive")
        
    print("[OK] Remote setup complete")

@task
def init(c, scenario="bridge-networking", host=None, user=None):
    """Initialize Terraform on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        conn.run(f"cd ~/fabric/{TERRAFORM_DIR}/scenarios/{scenario} && terraform init")

@task
def plan(c, scenario="bridge-networking", env="dev", host=None, user=None):
    """Plan Terraform changes on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        with conn.cd(f"~/fabric/{TERRAFORM_DIR}/scenarios/{scenario}"):
            conn.run(f"terraform workspace select {env} || terraform workspace new {env}")
            conn.run(f"terraform plan -var='ssh_public_key=$(cat ~/fabric/{TERRAFORM_DIR}/id_ed25519.pub)'")

@task
def apply(c, scenario="bridge-networking", env="dev", auto_approve=False, host=None, user=None):
    """Apply Terraform changes on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        with conn.cd(f"~/fabric/{TERRAFORM_DIR}/scenarios/{scenario}"):
            conn.run(f"terraform workspace select {env}")
            auto = "-auto-approve" if auto_approve else ""
            conn.run(f"terraform apply {auto} -var='ssh_public_key=$(cat ~/fabric/{TERRAFORM_DIR}/id_ed25519.pub)'")

@task
def destroy(c, scenario="bridge-networking", env="dev", host=None, user=None):
    """Destroy Terraform infrastructure on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        with conn.cd(f"~/fabric/{TERRAFORM_DIR}/scenarios/{scenario}"):
            conn.run(f"terraform workspace select {env}")
            conn.run(f"terraform destroy -var='ssh_public_key=$(cat ~/fabric/{TERRAFORM_DIR}/id_ed25519.pub)'")

@task
def validate(c, scenario="bridge-networking", host=None, user=None):
    """Validate Terraform configuration on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        with conn.cd(f"~/fabric/{TERRAFORM_DIR}/scenarios/{scenario}"):
            conn.run("terraform validate")
            conn.run("terraform fmt -check")

@task
def test(c, scenario="bridge-networking", host=None, user=None):
    """Run connectivity tests on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        with conn.cd(f"~/fabric/{TERRAFORM_DIR}"):
            if scenario == "macvlan-networking":
                conn.run("./test-macvlan-connectivity.sh")
                conn.run("./test-external-connectivity.sh")
            conn.run("./vm-connectivity-test.sh")

@task
def deploy_all(c, scenario="bridge-networking", host=None, user=None):
    """Deploy to dev, staging, and prod sequentially on remote host"""
    for env in ["dev", "staging", "prod"]:
        print(f"\n{'='*50}")
        print(f"Deploying to {env} environment...")
        print(f"{'='*50}\n")
        init(c, scenario, host, user)
        apply(c, scenario, env, auto_approve=True, host=host, user=user)

@task
def update_submodule(c, host=None, user=None):
    """Update terraform submodule on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        conn.run("cd ~/fabric && git submodule update --remote")
        conn.run("cd ~/fabric && git status")

@task
def status(c, host=None, user=None):
    """Check status of remote deployment"""
    conn = get_connection(host, user)
    
    with conn:
        conn.run("lxc list | grep k3s || echo 'No k3s containers found'")

@task
def logs(c, env="dev", host=None, user=None):
    """View K3s logs on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        conn.run(f"lxc exec k3s-{env}-cluster-01 -- journalctl -u k3s -f || echo 'Container not found'")

@task
def shell(c, env="dev", host=None, user=None):
    """Open shell in k3s container on remote host"""
    conn = get_connection(host, user)
    
    with conn:
        conn.run(f"lxc exec k3s-{env}-cluster-01 -- bash || echo 'Container not found'")
