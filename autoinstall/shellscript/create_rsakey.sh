#!/bin/bash
username=$1
useradd ${username}
su -c "ssh-keygen -t rsa -b 2048" ${username} << EOF




EOF
cd /home/${username}/.ssh/
cat /home/${username}/.ssh/id_rsa.pub >/home/${username}/.ssh/authorized_keys
chown ${username}:${username} /home/${username}/.ssh/authorized_keys
chmod 600 /home/${username}/.ssh/authorized_keys
tar zcvf ${username}.tar.gz /home/${username}/.ssh/id_rsa*
