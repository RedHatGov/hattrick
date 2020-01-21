# Project Hat Trick

The playbooks in this project can be used as a baseline for deploying a vast majority of Red Hat's product portfolio in a defined manner. The playbooks were originally built out to deploy on a set of field kits used by Red Hat North American Public Sector Solutions Architects.

The playbooks are setup in a way to be utilized in a standalone fashion for each function or for deploying a complete Red Hat Cloud Suite infrastructure.

Currently the provisioning of utility resources happens on a main RHEL+KVM host for deployment. After that either Red Hat OpenStack Platform or Red Hat Virtualization should be deployed. Once the chosen infrastructure is up and running, the remaining resources are provisioned on top. The provisioning mechanisms could be replaced with another infrastructure provider like VMware or Public Clouds.

All *required* variables are in_vars/vars.example.yml. If you need to customize further, you'll have to dig into the roles to see all the available vars to override.

We've attempted to make this setup very flexible. However, if you believe there is a better way, please contribute.

## Prerequisites

You need to configure an Ansible host to execute these playbooks

> NOTE: If you intend on running these playbooks from a RHEL 7 system, you need
> the system subscribed and have the following repos enabled:
> - rhel-7-server-rpms
> - rhel-7-server-extras-rpms
> - rhel-7-server-optional-rpms
> - rhel-7-server-ansible-2.9-rpms

You can do this manually, or you can use the provided [playbook](https://raw.githubusercontent.com/RedHatGov/hattrick/master/playbooks/hattrick/ansible-host-setup.yml)

## Configure your Ansible host using the provided playbook

1. Install Ansible on your target Ansible host

2. Download the playbook from the hattrick repo
```
$ curl https://raw.githubusercontent.com/RedHatGov/hattrick/master/playbooks/hattrick/ansible-host-setup.yml -o ansible-host-setup.yml
```
3. Run the playbook
```
$ ansible-playbook ansible-host-setup.yml
```

> NOTE: The playbook automatically clones the hattrick repo and places it
> in a folder named hattrick in the current working directory

4. Modify your vars file
```
$ cd hattrick/
$ vi vars/vars.yml
```
> NOTE: The vars example file only exposes the variables you must care about. If you need to dig deeper you'll have to dig into the roles.

## Enter pipenv shell

Before you run any of the following playbooks, you need to enter the pipenv
shell that was created for you during the ansible-host-setup playbook.

```
$ cd hattrick/
$ pipenv shell
```

## To deploy the initial RHEL+KVM admin host

1. Follow the [instructions to create a bootable custom ISO](https://github.com/RedHatGov/hattrick/tree/master/admin-iso) to install the base operating system for what will become the initial RHEL+KVM utility server
2. Verify your networking is the way you expect. We recommend two bridges for the VMs. br1 for the external network and br2 for the provisioning network
3. Run the kvm playbook from the ht directory
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/kvm.yml
```

## To deploy the RHEL Identity Manager (IdM) on a RHEL+KVM hypervisor

1. Follow the instructions above for Cloning and configuring the repository
2. Run the IdM playbook
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/idm.yml
```
> NOTE: If you need to teardown the IdM vm, run the following playbook. This will destroy and undefine the VM that was created.
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/kvm-teardown.yml --extra-vars "kvm_vm_name=idm"
```

## To deploy the RHEL Local Content Server (Repos, Registry, NFS) on a RHEL+KVM hypervisor

1. Follow the instructions above for Cloning and configuring the repository
2. Run the content playbook
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/content.yml
```
> NOTE: If you need to teardown the content server vm, run the following playbook. This will destroy and undefine the VM that was created.
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/kvm-teardown.yml --extra-vars "kvm_vm_name=content"
```

## To deploy the Red Hat OpenStack Platform Director on a RHEL+KVM hypervisor

1. Run the Director playbook
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/director.yml
```
> NOTE: If you need to teardown the Director vm, run the following playbook. This will destroy and undefine the VM that was created.
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/kvm-teardown.yml --extra-vars "kvm_vm_name=director"
```

## To deploy the Red Hat OpenStack Platform overcloud

> NOTE: The overcloud deployment templates stored in this repo have been built to deploy
> on our Project Hat Trick hardware kits. If you are deploying against different
> hardware, you will likely need to modify the templates which are stored in
> the overcloud role inside playbooks/roles/

1. Run the overcloud playbook
```
$ ansible-playbook -i inventory/inventory.yml -e @vars/vars.yml playbooks/hattrick/overcloud.yml
```

## To deploy the rest (to be continued):

> The remainder of this readme will be completed as the capabilities come into the repo
