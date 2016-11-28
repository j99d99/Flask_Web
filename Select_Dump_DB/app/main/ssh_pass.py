import os
import paramiko
import ConfigParser
import time
import ssh_pass


# config = ConfigParser.ConfigParser()
# config.read('config.ini')

# ipaddress = config.get('Server', 'ipaddress')
# username = config.get('Server', 'user')
# password = config.get('Server', 'password')
# port = config.get('Server', 'port')
# num = 2

# cmds = ['pwd\n', 'w\n', 'q\n']


##password login
def ssh_connection(ipaddress,username,password):
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=ipaddress, username=username, password=password)
	return ssh

##key login
def ssh_key_connection(ipaddress,username,port,key_path):
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	privatekey = os.path.expanduser(key_path)
	key = paramiko.RSAKey.from_private_key_file(privatekey)
	ssh.connect(hostname=ipaddress,username=username,port=port,pkey=key)
	return ssh


def ssh_key_downfile(ipaddress,username,port,key_path):
	sftp = paramiko.Transport((ipaddress,port))
	privatekey = os.path.expanduser(key_path)
	key = paramiko.RSAKey.from_private_key_file(privatekey)
	sftp.connect(username=username,pkey=key)
	sftpssh = paramiko.SFTPClient.from_transport(sftp)
	# sftpssh.get(downloadfilename,filename)
	# sftp.close()
	return sftpssh



# key_path = os.path.abspath('.')

# # ssh = ssh_connection(ipaddress,username,password)
# ssh = ssh_key_connection(ipaddress, username, key_path+'\id_rsa')
# stdin, stdout, stderr = ssh.exec_command('ip addr')
# print stdout.read()
# ssh.close()
