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

@main.route('/host-info')
def hostinfo():
	return render_template('host-info.html')
@main.route('/')
@main.route('/host-list')
def hostlist():
	hosts = Hosts.query.all()
	return render_template('host-list.html',hosts=hosts)

@main.route('/host-del',methods=['POST'])
def delHost():
	id = request.form['delid']
	print id
	delhost = Hosts.query.get(id)
	db.session.delete(delhost)
	db.session.commit()
	return redirect(url_for('main.hostlist'))
	

@main.route('/host-add',methods=['POST','GET'])
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
def saltminion(id):
	hostinfo = Hosts.query.get(id)
	saltssh = salt_ssh(hostinfo.ipaddress,hostinfo.ssh_user,hostinfo.ssh_passwd)
	result = saltssh.ssh()
	print result
	return jsonify({'message':result})


@main.route('/test/<id>',methods=['POST'])
def xdinstall(id):
	hostinfo = Hosts.query.get(id)
	client = salt_command(hostinfo.ipaddress)
	client.cpfile('xiaodai')
	#ret = s.cmd(ip,'cmd.script',['salt://xiaodai/xd.sh','testxd'])
	if int(hostinfo.projecttype) == 0: 
		client.script('install_xd.sh')
	if int(hostinfo.projecttype) == 1: 
		client.script('install_rongyun.sh')
	if int(hostinfo.projecttype) == 2: 
		client.script('install_p2p.sh')
	ret = client.script('create_rsakey.sh',hostinfo.general_user)
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
	print jsonify({'message':ret})
	return jsonify({'message':ret})















