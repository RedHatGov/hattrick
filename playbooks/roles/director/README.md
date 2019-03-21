director
=========

This role provisions, installs, and configures Red Hat OpenStack Platform Director

Requirements
------------

- Expects a working RHEL 7 system to target
- Red Hat Network account with a Red Hat OpenStack Platform subscription available

Role Variables
--------------

| Variable        | Required | Default  | Description                                                                                                                                                                                                                                     |
| --------------- | -------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `domain` | :x:      | ```hattrick.lab``` | The domain for the environment |
| `dns_server_public` | :x:      | ```1.1.1.1``` | The default upstream DNS server to use |
| `idm_hostname` | :heavy_check_mark:      |  | The short hostname for IdM |
| `idm_ssh_user` | :x:      | ```root``` | The default user to use for SSH access to IdM |
| `idm_ssh_pwd` | :x:      | ```p@ssw0rd``` | The default password to use for SSH access to IdM. Obviously you'd change this :) |
| `idm_public_ip` | :heavy_check_mark:      |  | The reachable public IP for IdM |
| `idm_base_img` | :heavy_check_mark:      |  | Name of the base image located in /var/lib/libvirt/images on the KVM hypervisor |
| `idm_vcpus` | :x:      | ```1``` | Number of vCPUS to assign to IdM |
| `idm_ram` | :x:      | ```4096``` | Amount of ram to give to IdM in megabytes |
| `idm_os_disk_name` | :x:      | ```{{ idm_hostname }}``` | Name of the OS disk in /var/lib/libvirt/images |
| `idm_os_disk_size` | :x:      | ```45G``` | Size of OS disk for IdM |
| `idm_nics` | :heavy_check_mark:      | ```see example playbook``` | Dictionary of NICs to create for IdM (only needs one) |
| `idm_repos` | :x:      | ```see defaults/main.yml``` | Dictionary of Repos to enable for IdM |
| `idm_packages` | :x:      | ```see defaults/main.yml``` | Dictionary of Packages to create for IdM |
| `idm_realm` | :heavy_check_mark:      |  | Identity Realm for IdM (ex: HATTRICK.LAB) |
| `idm_dm_pwd` | :heavy_check_mark:      |  | Identity Realm for IdM (ex: HATTRICK.LAB) |
| `idm_admin_pwd` | :heavy_check_mark:      |  | Password for admin user for IdM |
| `idm_forward_ip` | :heavy_check_mark:      | ```{{ dns_server_public }}```  | IP of Upstream DNS to set as the forwarder (for disconnected, don't set a forward IP) |
| `idm_reverse_zone` | :heavy_check_mark:      |  | Reverse zone to create in IdM (ex: "168.192.in-addr.arpa.") |
| `idm_users` | :heavy_check_mark:      |  | Dictionary of users to create in IdM post configuration |
| `idm_dns_records` | :heavy_check_mark:      |  | Dictionary of DNS records to create in IdM post configuration |

Dependencies
------------

None

Example Playbook
----------------

```yaml
---
- hosts: idm
  tags: install
  vars:
    domain: "example.com"
    dns_server_public: 1.1.1.1
    idm_hostname: idm #Short hostname
    idm_ssh_user: root
    idm_ssh_pwd: redhat
    idm_public_ip: "192.168.0.4"
    idm_base_img: rhel-guest-image-7.qcow2 #Name of base image in /var/lib/libvirt/images on KVM hypervisor
    idm_os_disk_name: "{{ idm_hostname }}"
    idm_nics:
      - name: eth0
        bootproto: static
        onboot: yes
        ip: "{{ idm_public_ip }}"
        prefix: "24"
        gateway: "192.168.0.1"
        dns_server: "{{ dns_server_public }}"
        config: "--type bridge --source br1 --model virtio"
    idm_repos:
      - rhel-7-server-rpms
      - rhel-7-server-extras-rpms
      - rhel-7-server-optional-rpms
    idm_packages:
      - ipa-server
      - ipa-server-dns
    idm_realm: "{{ domain | upper }}"
    idm_dm_pwd: "Redhat1993"
    idm_admin_pwd: "Redhat1993"
    idm_forward_ip: "{{ dns_server_public }}"
    idm_reverse_zone: "168.192.in-addr.arpa."
    idm_users:
       - username: operator
         password: redhat1234
         display_name: "Operator"
         first_name: Oper
         last_name: Ator
         email: "operator@redhat.com"
         phone: "+18887334281"
         title: "Systems Administrator"
    idm_dns_records:
       - hostname: router
         record_type: A
         ip_address: 192.168.0.1
         reverse_record: 1.0
       - hostname: switch
         record_type: A
         ip_address: 192.168.0.2
         reverse_record: 2.0
       - hostname: kvm
         record_type: A
         ip_address: 192.168.0.3
         reverse_record: 3.0
  tasks:
    - name: Install IDM
      include_role:
        name: idm
      tags: install

    - name: Configure IDM
      include_role:
        name: idm
        tasks_from: post_config
      tags: post-config
```

License
-------

GPLv3

Author Information
------------------

[Red Hat North American Public Sector Solution Architects](https://redhatgov.io)
