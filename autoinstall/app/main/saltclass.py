import salt.client
from salt.client.ssh.client import SSHClient as sshclient
import os

s = sshclient(c_path='/etc/salt/master')
file_roots = s.opts.get('file_roots')['base'][0]
client = salt.client.LocalClient()

class salt_api:
	def __init__(self,ipaddress):
		self.ipaddress = ipaddress

class salt_ssh(salt_api):
	def __init__(self,ipaddress,user,passwd):
		salt_api.__init__(self,ipaddress)
		self.user = user
		self.passwd = passwd

	def ssh(self):
		ret = s.cmd(tgt=self.ipaddress,fun='test.ping',ignore_host_keys=True,ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		s.cmd(tgt=self.ipaddress, fun='pkg.install',arg=['salt-minion'], ignore_host_keys=False,ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		s.cmd(tgt=self.ipaddress,fun='file.sed',arg=['/etc/salt/minion','#master: salt','master: 192.168.1.134'],ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		s.cmd(tgt=self.ipaddress,fun='file.sed',arg=['/etc/salt/minion','#id:','id: %s' % self.ipaddress],ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		s.cmd(tgt=self.ipaddress,fun='service.start',arg=['salt-minion'],ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		ret = client.cmd(self.ipaddress,'test.ping')
		return ret


class salt_command(salt_api):
	def __init__(self,ipaddress):
		salt_api.__init__(self,ipaddress)

	def cpfile(self,filenames):
		self.filenames = filenames
		print self.filenames
		#try:
		if os.path.isfile(file_roots+self.filenames):
		#if os.path.isfile(self.filenames):
			ret = client.cmd(self.ipaddress,'cp.get_file',['salt://%s' % self.filenames,'/tmp/%s' % self.filenames])
			return ret
		if os.path.isdir(file_roots+self.filenames):
			ret = client.cmd(self.ipaddress,'cp.get_dir',['salt://%s' % self.filenames,'/tmp/'])
			return ret
		
		else:
		#finally:
			ret =  "it's not a file or dir"
			return ret
	

	def script(self,scriptname,*args):
		self.scriptname = scriptname
		print len(args)
		if len(args) != 0:
			self.arg1 = args[0]
			print self.arg1
			ret = client.cmd(self.ipaddress,'cmd.script',['salt://%s' % self.scriptname,self.arg1])
		print self.scriptname
		if len(args) == 0:
			ret = client.cmd(self.ipaddress,'cmd.script',['salt://%s' % self.scriptname])
		print ret
		return ret
		

		

	def archivefile(self):
		pass

	def pkginstall(self,servicename):
		self.service = servicename
		client.cmd(self.ipaddress,'pkg.install',[self.service])

	def editfile(self):
		pass

	def servicemanage(self):
		pass

#a = salt_ssh('192.168.1.128','root','RDkj2016')
#a = salt_command('192.168.1.128')
#result = a.cpfile('get-pip.py')
#print result
