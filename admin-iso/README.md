# Building a Custom ISO for the initial RHEL+KVM Utility server

In order to utilize the automation in the main
[Hat Trick repo](https://github.com/redhat-kejones/hattrick), you need to first
build a RHEL+KVM utility server. This server will serve as the Ansilbe Host for
which all the automation will execute from. It will also serve as a hypervisor
for some of the necessary infrastructure VMs (like IDM and RHOSP Director).

The procedures below will work to generate a custom ISO file which can be
written to a bootable USB device or could be served from a PXE server.

## Custom ISO Build Process

> NOTE: To start with the official RHEL 7 ISO you will need an active
> RHEL subscription

1. Download the [latest RHEL DVD ISO](https://access.redhat.com/downloads/content/69/ver=/rhel---7/latest/x86_64/product-software)
2. Make some directories to utilize during the process
```
# mkdir -p /mnt/{iso,working}
```
3. Mount the RHEL-DVD.ISO file
```
# mount -t iso9660 <path to rhel-dvd.iso> /mnt/iso
```
4. Copy all of the contents of the .iso to the working directory
```
# cp -rPf /mnt/iso/* /mnt/working
```
5. Create a true repo inside the “Packages” directory that will be used to
install certain packages that are listed in the custom kickstart file
> NOTE: This next step requires installation of the createrepo packages
> ON RHEL/CentOS, yum install createrepo. On Fedora, dnf install createrepo
```
# cd /mnt/working/Packages
# createrepo .
```
6. Download the rhel-7-server-ansible-<latest>-rpms repo to the /mnt/working/
directory.
> NOTE: Some of the automation in the Hat Trick repo requires Ansible > 2.5.
> The idea is that you will have the Ansible 2.5 (or higher) repos available for installation
> during the kickstart process.
> [How to Create a Local Repo in RHEL](https://access.redhat.com/solutions/9892)
7. Create the ansible repo in the
/mnt/working/rhel-7-server-ansible-<version>-rpms/Packages directory
```
# cd /mnt/working/rhel-7-server-ansible-<version>-rpms/Packages
# createrepo .
```
8. Copy the custom kickstart file into the /mnt/working directory
> NOTE: the one we are using here is called
> [admin-ks.cfg](https://raw.githubusercontent.com/redhat-kejones/ht/master/admin-iso/admin-ks.cfg)
9. Edit the admin-ks.cfg file for whatever changes are needed in your environment
> NOTE: You will want to change the root password and most the network configs
10. Once all the info is in the kickstart file, you are ready to create your
custom ISO file
```
# cd /mnt/working
# mkisofs -r -T -J -V "htadmin" -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot -e images/efiboot.img -no-emul-boot -o ../htadmin.iso .
```
11. Use the isohybrid command to specify this .iso file is used for UEFI
```
# cd ../
# isohybrid --uefi htadmin.iso
```
12. Using the ‘dd’ command to copy the .iso over to a usable USB device
```
# dd if=htadmin.iso of=/dev/sd<usb device location> bs=4M status=progress; sync
```
> NOTE: You can watch the buffer get written out with the following command
```
# watch grep -e Dirty: -e Writeback: /proc/meminfo
```
13. Mount the new usb - there should be 2 partitions (ex. /dev/sdc1 & /dev/sdc2)
14. Mount the second device (should be smaller like 8M)
```
# mkdir /mnt/partition2
# mount /dev/sd<device name/number> /mnt/partition2
# cd /mnt/partition2
```
15. You should see a EFI/BOOT/grub.cfg file in the 2nd partition - edit the file
```
#vi /mnt/partition2/EFI/BOOT/grub.cfg

*Look for the search line and make it look like below*
search --no-floppy --set=root -l 'htadmin'

*Look for the 'linuxefi line for the first installation option
and make it look like below*
linuxefi /images/pxeboot/vmlinuz inst.stage2=hd:LABEL=htadmin inst.ks=hd:LABEL=htadmin:/admin-ks.cfg quiet
```
16. After this is verified/changed - you can unmount the usb device
and use it to boot

## Improvements

Anyone trying this process that sees room for improvement, please submit a PR
