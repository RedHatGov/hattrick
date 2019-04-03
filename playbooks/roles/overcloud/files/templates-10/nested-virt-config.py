#!/usr/bin/python
import subprocess
import socket
import re

def setup_nested_virt():

 nested_conf_file = "/etc/modprobe.d/nested.conf"

 # Check if Intel or AMD
 virt_extensions = ""
 cpuinfo_output = cmd(["cat", "/proc/cpuinfo"])
 for line in cpuinfo_output.split('\n'):
  if re.search('vmx', line):
   print "INFO: Intel VT-x enabled (vmx)"
   virt_extensions = "vmx"
  if re.search('svm', line):
   print "INFO:  AMD-V enabled (svm)"
   virt_extensions = "svm"

 if virt_extensions is "vmx":
  # Intel Nested Virt Setup

  # Overwrite nested.conf (for permanently applying parameters)
  nested_conf = open(nested_conf_file,"w")
  nested_conf.write("# Nested Virtualization Configuration written by OSP-Director\n\n")
  nested_conf.write("options kvm ignore_msrs=1\n")
  nested_conf.write("options kvm_intel nested=1\n")
  nested_conf.write("options kvm_intel ept=1\n")
  nested_conf.write("options kvm_intel enable_shadow_vmcs=1\n")
  nested_conf.write("options kvm_intel enable_apicv=1\n")
  nested_conf.close()

  # Reload the kvm_intel module 
  no_kvm_intel = True
  lsmod_output = cmd(["lsmod"])
  for line in lsmod_output.split('\n'):
   if re.search('kvm_intel', line):
    no_kvm_intel = False

  if not no_kvm_intel:
   try:
    print "INFO: Reloading kvm_intel module"
    print cmd(["modprobe", "-r", "kvm_intel"])
    print cmd(["modprobe", "kvm_intel"])
   except:
    print "ERROR: kvm_intel module reload failed.  Are instances running?"

  # Nova cpu mode host-passthrough
  nova_passthrough_exists = False
  try:
   passthrough_get =  cmd(["crudini", "--get", "/etc/nova/nova.conf", "libvirt", "cpu_mode"])
   for line in passthrough_get.split('\n'):
    if re.search('host-passthrough', line):
     print "INFO: CPU mode already set to host-passthrough"
     nova_passthrough_exists = True
  except:
    print "INFO: Nova CPU Host Passthrough not currently enabled"

  if not nova_passthrough_exists:
   print "INFO: Configuring nova.conf for CPU Host Passthrough"
   print cmd(["crudini", "--set", "/etc/nova/nova.conf", "libvirt", "cpu_mode", "host-passthrough"])
   print "INFO: Restarting nova compute"
   print cmd(["systemctl", "restart", "openstack-nova-compute.service"])

 elif virt_extensions is "svm":
  # AMD Nested Virt Setup

  # Overwrite nested.conf (for permanently applying parameters)
  nested_conf = open(nested_conf_file,"w")
  nested_conf.write("# Nested Virtualization Configuration written by OSP-Director\n\n")
  nested_conf.write("options kvm ignore_msrs=1\n")
  nested_conf.write("options kvm_amd nested=1\n")
  nested_conf.close()

  # Reload the kvm_amd module 
  no_kvm_amd = True
  lsmod_output = cmd(["lsmod"])
  for line in lsmod_output.split('\n'):
   if re.search('kvm_amd', line):
    no_kvm_amd = False

  if not no_kvm_amd:
   try:
    print "INFO: Reloading kvm_amd module"
    print cmd(["modprobe", "-r", "kvm_amd"])
    print cmd(["modprobe", "kvm_amd"])
   except:
    print "ERROR: kvm_amd module reload failed.  Are instances running?"

  # Nova cpu mode host-passthrough
  nova_passthrough_exists = False
  try:
   passthrough_get =  cmd(["crudini", "--get", "/etc/nova/nova.conf", "libvirt", "cpu_mode"])
   for line in passthrough_get.split('\n'):
    if re.search('host-passthrough', line):
     print "INFO: CPU mode already set to host-passthrough"
     nova_passthrough_exists = True
  except:
    print "INFO: Nova CPU Host Passthrough not currently enabled"

  if not nova_passthrough_exists:
   print "INFO: Configuring nova.conf for CPU Host Passthrough"
   print cmd(["crudini", "--set", "/etc/nova/nova.conf", "libvirt", "cpu_mode", "host-passthrough"])
   print "INFO: Restarting nova compute"
   print cmd(["systemctl", "restart", "openstack-nova-compute.service"])

 else:
  print "ERROR: No virtualization extensions found" 

def cmd(args):
    return subprocess.check_output(args)

def main():
 hostname = socket.gethostname()
 if "compute" in hostname:
  print("This is a compute node... continuing")
  setup_nested_virt()
 else:
  print("Not a compute node, so I'm not doing anything")

if __name__ == '__main__':
	main()
