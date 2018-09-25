OSP Instance
=========

Create an instance on OpenStack.

Requirements
------------

- python >= 2.7
- openstacksdk

Role Variables
--------------

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `os_auth` | :heavy_check_mark: | _omit_ | Dictionary containing auth information as needed by the cloud's auth plugin strategy. For the default password plugin, this would contain `auth_url`, `username`, `password`, `project_name` and any information about domains if the cloud supports them. For other plugins, this param will need to contain whatever parameters that auth plugin requires.<br><br>This parameter is not needed if a named cloud is provided or OpenStack `OS_*` environment variables are present. |
| `os_instance_name` | :heavy_check_mark: | | Name that has to be given to the instance. |
| `os_instance_image` | :heavy_check_mark: | | The name or id of the base image to boot. |
| `os_instance_flavor` | :heavy_check_mark: | | The name or id of the flavor in which the new instance has to be created. |
| `os_instance_key_name` | :heavy_check_mark: | | The key pair name to be used when creating a instance. |
| `os_instance_auto_ip` | :x: | `yes` | Ensure instance has public ip however the cloud wants to do that. |
| `os_instance_timeout` | :x: | `300` | The amount of time the module should wait for the instance to get into active state. |
| `os_instance_volumes` | :x: | `[]` | A list of volumes to create and attach to the instance. Each volume in the list would contain `name` and `size`. |
| `os_instance_security_groups` | :x: | `[]` | The security groups to create and to which the instance should be added. Each security group in the list would contain `name`, `rules`, and optionally `description`.<br><br>The `rules` parameter would contain options defined [here](https://docs.ansible.com/ansible/2.6/modules/os_security_group_rule_module.html#os-security-group-rule-module). |
| `os_auth` | :heavy_check_mark: | _omit_ | Dictionary containing auth information as needed by the cloud's auth plugin strategy. For the default password plugin, this would contain `auth_url`, `username`, `password`, `project_name` and any information about domains if the cloud supports them. For other plugins, this param will need to contain whatever parameters that auth plugin requires.<br><br>This parameter is not needed if a named cloud is provided or OpenStack `OS_*` environment variables are present. |
| `os_instance_name` | :heavy_check_mark: | | Name that has to be given to the instance. |
| `os_instance_image` | :heavy_check_mark: | | The name or id of the base image to boot. |
| `os_instance_flavor` | :heavy_check_mark: | | The name or id of the flavor in which the new instance has to be created. |
| `os_instance_key_name` | :heavy_check_mark: | | The key pair name to be used when creating a instance. |
| `os_instance_network` | :heavy_check_mark: | | Name or ID of a network to attach this instance to. |
| `os_instance_auto_ip` | :x: | `yes` | Ensure instance has public ip however the cloud wants to do that. |
| `os_instance_timeout` | :x: | `300` | The amount of time the module should wait for the instance to get into active state. |
| `os_instance_volumes` | :x: | `[]` | A list of volumes to create and attach to the instance. Each volume in the list would contain `name` and `size`. |
| `os_instance_security_groups` | :x: | `[]` | The security groups to create and to which the instance should be added. Each security group in the list would contain `name`, `rules`, and optionally `description`.<br><br>The `rules` parameter would contain options defined [here](https://docs.ansible.com/ansible/2.6/modules/os_security_group_rule_module.html#os-security-group-rule-module). |

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- hosts: servers
  roles:
    - role: openstack_instance
      os_auth:
        auth_url: http://openstack.example.com:5000
        username: admin
        password: p@ssw0rd
        project_name: myproject
      os_instance_name: myinstance
      os_instance_image: rhel75
      os_instance_flavor: m4.xlarge
      os_instance_key_name: user1-key
      os_instance_network: private
      os_instance_auto_ip: yes
      os_instance_timeout: 300
      os_instance_volumes:
        - name: scratch
          size: 10
        - name: db
          size: 50
      os_instance_security_groups:
        - name: ssh
          description: Allow SSH
          rules:
            - protocol: tcp
              port_range_min: 22
              port_range_max: 22
              remote_ip_prefix: 0.0.0.0/0
        - name: web
          rules:
            - protocol: tcp
              port_range_min: 80
              port_range_max: 80
              remote_ip_prefix: 0.0.0.0/0
            - protocol: tcp
              port_range_min: 443
              port_range_max: 443
              remote_ip_prefix: 0.0.0.0/0
```

License
-------

BSD
