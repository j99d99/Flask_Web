from salt.client.ssh.client import SSHClient as sshclient
s = sshclient(c_path='/etc/salt/master')
def ssh(saltmodels,*args): 
	arg = []
	if len(args) == 0:
		print "s.cmd(tgt='172.16.88.191',fun='%s',ignore_host_keys=True,ssh_user='root', ssh_passwd='RDkj2016',roster='scan')" % saltmodels
		ret = s.cmd(tgt='172.16.88.182',fun=saltmodels,ssh_user='root', ssh_passwd='RDkj2016',roster='scan')
	for arg_index in range(len(args)):
		arg.append(args[arg_index])
	rel = s.cmd(tgt='172.16.88.182',fun=saltmodels,arg=arg,ignore_host_keys=True,ssh_user='root', ssh_passwd='RDkj2016',roster='scan')
	return rel

result = ssh('test.ping')
print result


