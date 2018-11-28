# ht
Project Hat Trick

The playbooks in this project can be used as a baseline for deploying a vast majority of Red Hat's product portfolio in a defined manner. The playbooks were originally built out to deploy on a set of field kits used by Red Hat North American Public Sector Solutions Architects.

The playbooks are setup in a way to be utilized in a standalone fashion for each function or for deploying a complete Red Hat Cloud Suite infrastructure.

Currently the provisioning of utility resources happens on a main RHEL+KVM host for deployment. After that either Red Hat OpenStack Platform or Red Hat Virtualization should be deployed. Once the chosen infrastructure is up and running, the remaining resources are provisioned on top. The provisioning mechanisms could be replaced with another infrastructure provider like VMware or Public Clouds.

All required variables are in_vars/vars.yml.sample. If you need to customize further, you'll have to dig into the roles to see all the available vars to override.

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
- Red Hat Identity Manager (LDAP and provides DNS)
- Red Hat Repo Server
- Red Hat OpenStack Platform Director

## Prerequisites

You need to configure an ansible host to execute these playbooks
- Ansible 2.6
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

## To Deploy the initial RHEL+KVM admin host:

1. Follow the [instructions to create a bootable custom ISO](https://github.com/redhat-kejones/ht/tree/master/admin-iso)
to install the RHEL+KVM utility server
2. Verify your networking is the way you expect. We recommend to bridges for the VMs. br1 for the external network and br2 for the provisioning network
3. Download the setup playbook that will clone this repo and copy the ssh key
> NOTE: you may need to mod the credentials in this file if you changed them
> in your custom ISO or provisioned the KVM host with different credentials
```
# wget https://raw.githubusercontent.com/redhat-kejones/hattrick/master/00-hattrick-setup.yml
```
4. Run the setup playbook
```
# ansible-playbook 
```
5. Set up your Ansible Vault file
> NOTE: you will be prompted to create an Ansible Vault password. You will need
> this password for the remaining automation
```
# ansible-vault encrypt /root/hattrick/group_vars/all/vault
# ansible-vault edit /root/hattrick/group_vars/all/vault
```
6. Move into the hattrick directory
```
# cd hattrick/
```
7. You need to either modify and use one of the existing inventory files or
create your own. They are located in /root/hattrick/inventories
```
# vi inventories/inventory-hattrick
```
8. You need to either modify and use one of the existing group_vars files or
create your own. They are located in /root/hattrick/group_vars
```
# vi group_vars/hattrick
```
9. Modify the group_vars/all/vars file
> NOTE: "destructive_filesystem" is destructive and will destroy any partitions
> that are created and defined in the roles folder that calls the filesytem
> module. Default is YES.
```
# vi group_vars/all/vars
```
10. Deploy your infrastructure. Currently only RHHI4C is complete
```
# screen -S ops
# ansible-playbook -i inventories/inventory-hattrick --ask-vault-pass deploy-rhhi4c.yaml
```
11. Modify the cf-vars file in order to deploy CloudForms
```
# vi cf-vars.yml
```
12. Deploy CloudForms on top
```
# ansible-playbook -i inventories/inventory-local --ask-vault-pass 08-rhcloudforms.yml
```
13. Modify the ocp-vars file in order to deploy OpenShift Container Platform
```
# vi ocp-vars.yml
```
14. Deploy OpenShift on top
```
# ansible-playbook -i inventories/inventory-local --ask-vault-pass 09-rhocp.yml
```
15. Modify the tower-vars file in order to deploy Ansible Tower
```
# vi tower-vars.yml
```
16. Deploy Ansible Tower on top
```
# ansible-playbook -i inventories/inventory-local --ask-vault-pass 10-ansible-tower.yml
```
