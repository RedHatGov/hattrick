kvm
=========

Turn a regular RHEL 7 server into a RHEL+KVM hypervisor.

Requirements
------------

- Expects a base RHEL 7 installation
- Reachable on at least 1 IP
- SSH enabled and root password authentication on
- Either physical virtualization or nested virtualization

Role Variables
--------------

- `domain`: the domain for the machine. Default is "example.com"
- `dns_server_local`: Local dns server IP for your environment. Default is "192.168.0.4"
- `dns_server_public`: Public dns server IP. Default is "1.1.1.1"
- `git_repo`: Location of the Project Hat Trick repo on GitHub. Set to "https://github.com/redhat-kejones/ht"


kvm_hostname_full: kvm.{{ domain }}
kvm_disks:
  root: sda
  #libvirt_images: sdb
  #content: sdc
kvm_repos:
  - rhel-7-server-rpms
  - rhel-7-server-extras-rpms
  - rhel-7-server-rh-common-rpms
kvm_packages:
  - 'screen'
  - 'wget'
  - 'vim'
  - 'tree'
  - 'yum-utils'
  - 'git'
  - 'qemu-kvm'
  - 'qemu-img'
  - 'libvirt'
  - 'virt-install'
  - 'libvirt-client'
  - 'libvirt-python'
  - 'libguestfs-tools-c'
  - 'rhel-guest-image-7'
  - 'ansible'

Dependencies
------------

- redhatgov.rhsm

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

GPLv3

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
