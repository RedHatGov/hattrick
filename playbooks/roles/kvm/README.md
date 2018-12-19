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

| Variable        | Required | Default  | Description                                                                                                                                                                                                                                     |
| --------------- | -------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `kvm_hostname_full` | :heavy_check_mark:      | kvm.example.com | The FQDN for the RHEL+KVM system |
| `kvm_disks` | :x:      | ```  root: sda``` | A dictionary of disks to utilize for the installation |
| `kvm_packages` | :x:      | see defaults/main.yml | List of packages to install |
| `kvm_repos` | :heavy_check_mark:      |  | A list of Red Hat repositories to enable |

Dependencies
------------

- redhatgov.rhsm

Example Playbook
----------------

```yaml
- hosts: kvm
  tasks:
  - name: Deploy kvm
    roles:
      - reghatgov.kvm
```

License
-------

GPLv3

Author Information
------------------

[Red Hat North American Public Sector Solution Architects](https://redhatgov.io)
