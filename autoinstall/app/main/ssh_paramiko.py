# -*- coding: UTF-8 -*-
import os
import paramiko
import time

class ssh_paramiko:

	def __init__(self,ipaddress,username,password,port=22):
		'''
		ipaddress	服务器ip
		username	服务器登录用户
		password	服务器登录密码或者登录key路径
		port		服务器登录端口,默认22
		'''
		self.ipaddress = ipaddress
		self.username = username
		self.password = password
		self.port = port
		# self.key_path = key_path
	##ssh password login
	def ssh_connection(self):
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=self.ipaddress, username=self.username, port=self.port,password=self.password)
		return ssh

	##ssh key login
	def ssh_key_connection(self):
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		privatekey = os.path.expanduser(self.password)
		key = paramiko.RSAKey.from_private_key_file(privatekey)
		ssh.connect(hostname=self.ipaddress,username=self.username, port=self.port,pkey=key)
		return ssh

	##sftp ssh login
	def ssh_upload(self):
		sftp = paramiko.Transport((self.ipaddress,self.port))
		sftp.connect(username=self.username,password=self.password)
		sftpssh = paramiko.SFTPClient.from_transport(sftp)
		return sftpssh

	##sftp key login
	def ssh_key_upload(self):
		sftp = paramiko.Transport((self.ipaddress,self.port))
		privatekey = os.path.expanduser(self.password)
		key = paramiko.RSAKey.from_private_key_file(privatekey)
		sftp.connect(username=self.username,pkey=key)
		sftpssh = paramiko.SFTPClient.from_transport(sftp)
		return sftpssh
