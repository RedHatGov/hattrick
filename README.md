# Project Hat Trick

The playbooks in this project can be used as a baseline for deploying a vast majority of Red Hat's product portfolio in a defined manner. The playbooks were originally built out to deploy on a set of field kits used by Red Hat North American Public Sector Solutions Architects.

The playbooks are setup in a way to be utilized in a standalone fashion for each function or for deploying a complete Red Hat Cloud Suite infrastructure.

Currently the provisioning of utility resources happens on a main RHEL+KVM host for deployment. After that either Red Hat OpenStack Platform or Red Hat Virtualization should be deployed. Once the chosen infrastructure is up and running, the remaining resources are provisioned on top. The provisioning mechanisms could be replaced with another infrastructure provider like VMware or Public Clouds.

All required variables are in_vars/vars.example.yml. If you need to customize further, you'll have to dig into the roles to see all the available vars to override.

We've attempted to make this setup very flexible. However, if you believe there is a better way, please contribute.

Contributors:
- Jason Ritenour
- Chris Reynolds
- Jared Hocutt
- Chris Alliey
- Laurent Domb
- Kevin Jones
- Jamie Duncan
- Steven Carter
- Kellen Gattis
- Russell Builta

RHEL+KVM
VMs:
- Red Hat Identity Manager (IdM) (Provides local DNS and LDAP)
- Red Hat Content Server (Local Repos and Registry)
- Red Hat OpenStack Platform (RHOSP) Director

## Prerequisites

You need to configure an ansible host to execute these playbooks
- Ansible >= 2.6
- Git
- Python VirtualEnv
- screen or tmux (optional and your preference)

## Clone and configure the repository

1. Clone the Project Hattrick repository
```
$ git clone https://github.com/redhat-kejones/ht.git
```
2. Setup your vars file
```
$ cd ht/
$ cp vars/vars.example.yml vars/vars.yml
$ vi vars/vars.yml
```
> NOTE: The vars example file only exposes the variables you must care about. If you need to dig deeper you'll have to dig into the roles.

## To Deploy the initial RHEL+KVM admin host

1. Follow the [instructions to create a bootable custom ISO](https://github.com/redhat-kejones/ht/tree/master/admin-iso)
to install the base operating system for what will become the intitial RHEL+KVM utility server
2. Verify your networking is the way you expect. We recommend two bridges for the VMs. br1 for the external network and br2 for the provisioning network
3. Run the kvm playbook from the ht directory
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/kvm.yml
```

## To Deploy the RHEL Identity Manager (IdM) on a RHEL+KVM hypervisor

1. Follow the instructions above for Cloning and configuring the repository
2. Run the IdM playbook
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/idm.yml
```
> NOTE: If you need to teardown the IdM vm, run the following playbook. This will destroy and undefine the VM that was created.
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/idm-teardown.yml
```

## To Deploy the RHEL Local Content Server (Repos, Registry, NFS) on a RHEL+KVM hypervisor

1. Follow the instructions above for Cloning and configuring the repository
2. Run the content playbook
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/content.yml
```
> NOTE: If you need to teardown the content server vm, run the following playbook. This will destroy and undefine the VM that was created.
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/content-teardown.yml
```

## To Deploy the rest (to be continued):

> The remainder of this readme will be completed as the capabilities come into the repo
