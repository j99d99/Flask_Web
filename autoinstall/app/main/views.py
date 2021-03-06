#coding: utf-8
from flask import render_template, flash, redirect,url_for,request,send_from_directory,current_app,make_response,jsonify
from . import main
from .. import db
from ..models import User,ConfigInfo,Hosts
from flask.ext.login import login_required,logout_user,login_user,current_user
# from ssh_paramiko import ssh_paramiko
# from ssh_upmanage import ops_manage
import os,time
from saltclass import salt_ssh,salt_command
import random
from ssh_paramiko import ssh_paramiko

@main.route('/host-info/<id>')
@login_required
def hostinfo(id):
	hostinfo = Hosts.query.get(id)
	return render_template('host-info.html',hostinfo=hostinfo)
@main.route('/')
@main.route('/host-list')
@login_required
def hostlist():
	hosts = Hosts.query.all()
	return render_template('host-list.html',hosts=hosts)

@main.route('/host-del',methods=['POST'])
@login_required
def delHost():
	id = request.form['delid']
	print id
	delhost = Hosts.query.get(id)
	db.session.delete(delhost)
	db.session.commit()
	return redirect(url_for('main.hostlist'))
	
@main.route('/host_add',methods=['GET','POST'])
@login_required
def addHostiframe():
	if request.method == 'POST':
		projectname = request.form['projectname']
		ipaddress = request.form['ipaddress']
		username = request.form['sshuser']
		general_user = request.form.get('general_user','None')
		#port = request.form['ssh_port']
		passwd = request.form['password']
		projecttype = request.form.get('projecttype','None')
		comment = request.form.get('comment','None')
		#manageruser = request.form['manageuser']
		#managerpasswd = request.form['managepasswd']
		#domaininfo = request.form['domaininfo']
		print ipaddress
		hostinfo = Hosts(projectname=projectname,ipaddress=ipaddress,ssh_user=username,ssh_passwd=passwd,projecttype=projecttype,comment=comment,general_user=general_user)
		db.session.add(hostinfo)
		db.session.commit()
		return 'OK'
	return render_template('_add.html')
@main.route('/host-add',methods=['POST','GET'])
@login_required
def addHost():
	if request.method == 'POST':
		projectname = request.form['projectname']
		ipaddress = request.form['ipaddress']
		username = request.form['sshuser']
		general_user = request.form.get('general_user','None')
		#port = request.form['ssh_port']
		passwd = request.form['password']
		projecttype = request.form.get('projecttype','None')
		comment = request.form.get('comment','None')
		#manageruser = request.form['manageuser']
		#managerpasswd = request.form['managepasswd']
		#domaininfo = request.form['domaininfo']
		print ipaddress
		hostinfo = Hosts(projectname=projectname,ipaddress=ipaddress,ssh_user=username,ssh_passwd=passwd,projecttype=projecttype,comment=comment,general_user=general_user)
		db.session.add(hostinfo)
		db.session.commit()
		return 'OK'
	return render_template('host-add.html')

@main.route('/salt_minioninstall/<id>',methods=['POST'])
@login_required
def saltminion(id):
	hostinfo = Hosts.query.get(id)
	saltssh = salt_ssh(hostinfo.ipaddress,hostinfo.ssh_user,hostinfo.ssh_passwd)
	print hostinfo.ipaddress
	print hostinfo.ssh_user
	result = saltssh.ssh()
	print result
	return jsonify({'message':result})


@main.route('/test/<id>',methods=['POST'])
@login_required
def xdinstall(id):
	hostinfo = Hosts.query.get(id)
	client = salt_command(hostinfo.ipaddress)
	client.script('auto_parted.sh')
	#ret = s.cmd(ip,'cmd.script',['salt://xiaodai/xd.sh','testxd'])
	if int(hostinfo.projecttype) == 0: 
		client.cpfile('xiaodai')
		client.script('install_xd.sh')
	if int(hostinfo.projecttype) == 1: 
		client.cpfile('rongyun')
		client.script('install_rongyun.sh')
	if int(hostinfo.projecttype) == 2: 
		client.cpfile('p2pv2')
		client.script('install_p2p.sh')
	ret = client.script('create_rsakey.sh',hostinfo.general_user)
	client.set_filemode('/usr/local/tomcat_*')
	#change ssh port
	sshport =  random.randint(40000,65536)
	print sshport
	client.editfile('/etc/ssh/sshd_config','#Port 22','Port %s' % sshport)
	client.editfile('/etc/ssh/sshd_config','#PermitRootLogin yes','PermitRootLogin no')
	client.editfile('/etc/ssh/sshd_config','PermitRootLogin yes','PermitRootLogin no')
	client.getfile_from_minion('/home/%s/.ssh/%s.tar.gz' % (hostinfo.general_user,hostinfo.general_user))
	hostinfo.ssh_port = sshport
	db.session.add(hostinfo)
	db.session.commit()
	client.servicemanage('sshd')
	print jsonify({'message':ret})
	return jsonify({'message':ret})


@main.route('/ssh_command',methods=['POST'])
def ssh_command():
	id = request.form.get('id')
	print id
	command = request.form.get('command')
	print command
	hostinfo = Hosts.query.get(id)
	ssh_connection = ssh_paramiko(hostinfo.ipaddress,hostinfo.ssh_user,hostinfo.ssh_passwd)
	ssh = ssh_connection.ssh_connection()
	stdin, stdout, stderr = ssh.exec_command(command)
	result = stdout.read().strip('\n')
	return result
	

#@main.route('/download/hostinfo/<id>',methods=['GET','POST'])
#def download(id):
#	hostinfo = Hosts.query.get(id)
