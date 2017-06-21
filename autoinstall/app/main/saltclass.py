import salt.client
from salt.client.ssh.client import SSHClient as sshclient
import os

s = sshclient(c_path='/etc/salt/master')
file_roots = s.opts.get('file_roots')['base'][0]
getfile_destdir = s.opts.get('cachedir')
client = salt.client.LocalClient()
epel6 = "https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm"
epel7 = "https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm"

class salt_api:
	def __init__(self,ipaddress):
		self.ipaddress = ipaddress

class salt_ssh(salt_api):
	def __init__(self,ipaddress,user,passwd):
		salt_api.__init__(self,ipaddress)
		self.user = user
		self.passwd = passwd

	def ssh(self):
		s.cmd(tgt=self.ipaddress,fun='test.ping',ignore_host_keys=True,ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		s.cmd(tgt=self.ipaddress,fun='cp.get_file',arg=['salt://epel-release-latest-6.noarch.rpm','/tmp/epel-release-latest-6.noarch.rpm'],ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		s.cmd(tgt=self.ipaddress,fun='cmd.shell',arg=['rpm -vih /tmp/epel-release-latest-6.noarch.rpm'],ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		ret = s.cmd(tgt=self.ipaddress, fun='pkg.install',arg=['salt-minion'],ignore_host_keys=True,ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
		print ret
		s.cmd(tgt=self.ipaddress,fun='file.sed',arg=['/etc/salt/minion','#master: salt','master: 172.16.88.192'],ssh_user=self.user, ssh_passwd=self.passwd,roster='scan')
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
		if len(args) != 0:
			self.arg1 = args[0]
			print self.arg1
			ret = client.cmd(self.ipaddress,'cmd.script',['salt://%s' % self.scriptname,self.arg1])
		if len(args) == 0:
			ret = client.cmd(self.ipaddress,'cmd.script',['salt://%s' % self.scriptname])
		return ret
		

	def set_filemode(self,filename):
		self.filename = filename
		client.cmd(self.ipaddress,'file.set_mode',[self.filename])
		

	def archivefile(self):
		pass

	def pkginstall(self,servicename):
		self.service = servicename
		client.cmd(self.ipaddress,'pkg.install',[self.service])

	def getfile_from_minion(self,file_path):
		self.file_path = file_path
		print self.file_path
		ret = client.cmd(self.ipaddress,'cp.push',[self.file_path])
		print ret
		abs_file_path = getfile_destdir + '/minions/' +self.ipaddress+'/files/'+file_path
		cpcommand = "mv %s %s" % (abs_file_path,file_roots)
		print abs_file_path
		os.system(cpcommand)

	def editfile(self,*args):
		if len(args) != 3:
			return 'you should input 3 args'
		if len(args) == 3:
			self.arg1 =  args[0]
			self.arg2 =  args[1]
			self.arg3 =  args[2]
			client.cmd(self.ipaddress,'file.sed',[self.arg1,self.arg2,self.arg3])

	def servicemanage(self,servicename):
		self.service = servicename
		client.cmd(self.ipaddress,'service.restart',[self.service])
		

#a = salt_ssh('192.168.1.128','root','RDkj2016')
#a = salt_command('192.168.1.128')
#result = a.cpfile('get-pip.py')
#print result
