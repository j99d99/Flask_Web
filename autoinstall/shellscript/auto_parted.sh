#!/bin/bash
#------------------------
[ $(id -u) != "0" ] && { echo "Error: You must be root to run this script"; exit 1; } 

MOUNT_DIR=/data

count=0

# check lock file, one time only let the script run one time 
LOCKfile=/tmp/.$(basename $0)
if [ -f "$LOCKfile" ];then
  echo
  echo "The script is already exist, please next time to run this script"
  echo
  exit
else
  echo
  echo "Step 1.No lock file, begin to create lock file and continue"
  echo
  touch $LOCKfile
fi

> $LOCKfile
for i in `fdisk -l | grep -oE 'Disk /dev/x?[sv]d[b-z]' | awk '{print $2}'`
do
if [ -z "$(blkid | grep -v 'PTTYPE="dos"' | grep -w "$i")" ];then
if [ -z "$(mount | grep "$i")" -a ! -e "${i}1" ]; then
echo $i >> $LOCKfile
#echo "You have a free disk, Now will fdisk it and mount it"
fi
if [ -z "$(mount | grep "$i")" -a -e "${i}1" ]; then
 echo "The $i has been partitioned! " 
fi
fi
done
DISK_LIST=$(cat $LOCKfile)
if [ "X$DISK_LIST" == "X" ];then
echo "No free disk need to be fdisk. Exit script"
rm -rf $LOCKfile
exit 0
else
echo "This system have free disk "
for i in `echo $DISK_LIST`
do
echo "$i"
fdisk -S 56 $i << EOF
n
p
1
 
 
wq
EOF
sleep 5
mkfs.ext4 ${i}1
cat >>/etc/fstab <<EOF
`blkid ${i}1 | awk '{print $2}'|sed 's/\"//g' ` ${MOUNT_DIR}  ext4 noatime,nodiratime,acl,defaults 0 0
EOF
mkdir ${MOUNT_DIR}
mount -a
df -h
count=$((count+1))
done
#[ $count -gt 1 ] && { echo "This system has at least two free disk, You must manually mount it"; exit 0; } 
fi
rm -rf $LOCKfile
