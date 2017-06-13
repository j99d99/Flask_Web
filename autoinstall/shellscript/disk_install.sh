#!/bin/bash
disk=$1
fdisk -S 56 /dev/$disk << EOF
n
p
1


wq
EOF
sleep 5
mkfs.ext4 /dev/${disk}1
cat >>/etc/fstab <<EOF
`blkid /dev/${disk}1 | awk '{print $2}'|sed 's/\"//g' ` /data  ext4 noatime,nodiratime,acl,defaults 0 0
EOF
mkdir /data
mount -a
