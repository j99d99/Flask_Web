#coding: utf8
from flask import render_template, flash, redirect,url_for,request,send_from_directory,abort
from . import main
from forms import UserForm,DBForm,CommandForm
from ..models import User,DBInfo,user_role,LogInfo
from flask.ext.login import login_required,logout_user,login_user,current_user
from ssh_pass import ssh_connection,ssh_key_connection,ssh_key_downfile
from .. import db
import os
from config import Config
import time

@main.route('/')
@main.route('/index')
@login_required
def index():
	return render_template('index.html')

#显示用户列表,管理员拥有权限
@main.route('/listuser')
@login_required
def listuser():
	if current_user.role == '0':
		userinfo = User.query.all()
		return render_template('listuser.html',data=userinfo)
	return abort(403)

#授权某用户时显示该用户id未授权的项目,管理员拥有权限
@main.route('/unauthorized/<id>',methods=['GET','POST'])
@login_required
def unauthorized(id):
	if current_user.role != '0':
		return abort(403)
	user = User.query.filter_by(id=id).first()
	datainfo = user.roles
	datainfos = DBInfo.query.all()
	data = []
	for i in datainfo:
		datainfos.remove(i)
	print datainfos
	if request.method == 'POST' and current_user.role == '0':
		dbsid = request.form['dbid']
		dbinfo = DBInfo.query.filter_by(id=dbsid).first()
		user.roles.append(dbinfo)
		db.session.add(user)
		db.session.commit()
		flash(u'添加成功')
		return redirect(url_for('main.listuser'))
	return render_template('unauthorized.html',data=datainfos,username=user.username,userid=user.id)

#查看用户已授权的项目,管理员拥有权限
@main.route('/authorized/<id>',methods=['GET','POST'])
@login_required
def authorized(id):
	if current_user.role != '0':
		return abort(403)
	user = User.query.filter_by(id=id).first()
	datainfo = user.roles
	return render_template('authorized.html',data=datainfo,username=user.username,userid=user.id)

#添加用户,管理员拥有权限
@main.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
	print current_user.role
	if current_user.role == '0':
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']
			adduser = User(username=username,password=password)
			print adduser
			db.session.add(adduser)
			db.session.commit()
			flash(u'添加成功')
			return redirect(url_for('main.listuser'))
	else:
		return abort(403)
	return render_template('adduser.html')

#显示所有已添加的项目,管理员拥有权限
@main.route('/dbinfo')
@login_required
def dbinfo():
	if current_user.role != '0':
		userid = current_user.id
		datainfo = User.query.filter_by(id=userid).first().roles.all()
		return render_template('dbinfo.html',data=datainfo)
	datainfo = DBInfo.query.all()
	return render_template('dbinfo.html',data=datainfo)

	# datainfo = User.query.filter_by(id=current_user.id).first().roles.all()
	# print datainfo
	# for i in datainfo:
	# 	print i 
	# return render_template('list.html',data=datainfo)

##添加项目,管理员拥有权限
@main.route('/adddb',methods=['GET','POST'])
@login_required
def adddb():
	if current_user.role == '0':
		if request.method == 'POST':
			hostip = request.form['hostip']
			#获取form上传的文件内容
			prv_file = request.files['hostpasspath']
			#定义文件保存路径
			file_name = os.path.join(Config.UPLOAD_FOLDER,hostip)
			print file_name
			#保存上传的文件
			prv_file.save(file_name)
			hostname = request.form['hostname']
			hostuser = request.form['hostuser']
			hostport = request.form['hostport']
			dbhost = request.form['dbhost']
			dbname = request.form['dbname']
			dbuser = request.form['dbuser']
			dbpass = request.form['dbpass']
			#添加信息到数据库
			host = DBInfo(hostname=hostname,
				hostport=hostport,
				hostuser=hostuser,
				dbhost=dbhost,
				hostpasspath=file_name,
				dbname=dbname,
				dbuser=dbuser,
				dbpass=dbpass,
				hostip=hostip)
			print host
			db.session.add(host)
			db.session.commit()
			flash(u'添加成功')
			return redirect(url_for('main.dbinfo'))
	else:
		return abort(403)
	return render_template('adddb.html')

#获取点击查询按钮post的值,并通过处理将值传递到查询页面
@main.route('/select',methods=['GET','POST'])
@login_required
def select():
	if request.method =='POST':
		dbid = request.form['listid']
		print dbid
		datainfo = DBInfo.query.filter_by(id=dbid).first()
		serverip = datainfo.hostip
		serveruser = datainfo.hostuser
		serverport = datainfo.hostport
		serverpath = datainfo.hostpasspath
		dbuser = datainfo.dbuser
		dbpass = datainfo.dbpass
		dbhost = datainfo.dbhost
		dbname = datainfo.dbname
		return render_template('select.html',dbid=dbid,hostname=datainfo.hostname,dbname=datainfo.dbname)
	return redirect(url_for('main.index'))

##select跳转后的查询信息处理收集
@main.route('/display',methods=['GET','POST'])
@login_required
def display():
	if request.method == 'POST':
		id = request.form['dbid']
		comm = request.form['command']

		datainfo = DBInfo.query.filter_by(id=id).first()
		serverip = datainfo.hostip
		serveruser = datainfo.hostuser
		serverport = datainfo.hostport
		serverpath = datainfo.hostpasspath
		dbuser = datainfo.dbuser
		dbpass = datainfo.dbpass
		dbhost = datainfo.dbhost
		dbname = datainfo.dbname

		command = comm.strip().lower()
		print serverip
		if command.startswith('select'):
			commands = "mysql -u"+dbuser+" -p"+dbpass+" -h"+dbhost+" --default-character-set utf8 "+dbname+" -e 'select %s'" % command.split('select')[1]
			print commands
			# ssh = ssh_connection(serverip,serveruser,serverpass)
			ssh = ssh_key_connection(serverip, serveruser,serverport, os.path.abspath('.')+os.sep+serverpath)
			stdin, stdout, stderr = ssh.exec_command(commands)
			print type(stdout)
			datas = stdout.readlines()
			print datas
			list = []
			for data in datas:
				print type(data)
				data = data.split('\t')
				print data
				print type(data)
				list.append(tuple(data))

			print list
			ssh.close()
			log = LogInfo(user=current_user.username,hostname=datainfo.hostname,command=commands)
			db.session.add(log)
			db.session.commit()
			return render_template('select.html',dbid=id,data=list,hostname=datainfo.hostname,dbname=datainfo.dbname)
			# return redirect(url_for('main.select',dbid=id,data=list,hostname=datainfo.hostname,dbname=datainfo.dbname))
		if command.startswith('show'):
			commands = "mysql -u"+dbuser+" -p"+dbpass+" -h"+dbhost+" --default-character-set utf8 "+dbname+" -e 'show %s'" % command.split('show')[1]
			print commands
			# ssh = ssh_connection(serverip,serveruser,serverpass)
			ssh = ssh_key_connection(serverip, serveruser,serverport, os.path.abspath('.')+os.sep+serverpath)
			stdin, stdout, stderr = ssh.exec_command(commands)
			print type(stdout)
			datas = stdout.readlines()
			list = []
			for data in datas:
				print type(data)
				data = data.split('\t')
				print data
				print type(data)
				list.append(tuple(data))

			print list
			ssh.close()
			log = LogInfo(user=current_user.username,hostname=datainfo.hostname,command=commands)
			db.session.add(log)
			db.session.commit()
			return render_template('select.html',dbid=id,data=list,hostname=datainfo.hostname,dbname=datainfo.dbname)
		else:
			log = LogInfo(user=current_user.username,hostname=datainfo.hostname,command=comm)
			db.session.add(log)
			db.session.commit()
			return render_template('selecterror.html')
	return redirect(url_for('main.index'))

@main.route('/mysqldump',methods=['POST','GET'])
@login_required
def mysqldump():
	id = request.form['listid']
	print id
	#根据id获取数据库信息
	datainfo = DBInfo.query.filter_by(id=id).first()
	serverip = datainfo.hostip
	serveruser = datainfo.hostuser
	serverport = datainfo.hostport
	serverpath = datainfo.hostpasspath
	dbuser = datainfo.dbuser
	dbpass = datainfo.dbpass
	dbhost = datainfo.dbhost
	dbname = datainfo.dbname

	print dbname
	if request.method == 'POST':
		#备份文件命名
		backfilename = "%s.%s.sql" % (dbname,time.strftime('%Y%m%d%H%M%S'))
		#压缩后文件
		zipfile = backfilename+'.zip'
		#备份命令
		command1 = "mysqldump -u%s -p%s --default-character-set utf8 -h%s %s > %s"  % (dbuser,dbpass,dbhost,dbname,backfilename)
		#压缩命令
		command2 = "zip -P 'RD1111' %s %s"  % (zipfile,backfilename)
		# ssh = ssh_connection(serverip,serveruser,serverpass)
		#paramiko秘钥方式登录服务器
		ssh = ssh_key_connection(serverip, serveruser,int(serverport), os.path.abspath('.')+os.sep+serverpath)
		print command1
		#执行备份命令
		ssh.exec_command(command1)
		#ssh.exec_command(command2)
		ssh.close()
		#paramiko sftp秘钥登录服务器
		sftpssh = ssh_key_downfile(serverip, serveruser, int(serverport), os.path.abspath('.')+os.sep+serverpath)
		print os.path.abspath('.')+os.sep+'back'+os.sep+backfilename
		#下载刚刚备份的文件
		sftpssh.get(backfilename, os.path.abspath('.')+os.sep+'back'+os.sep+backfilename)
		sftpssh.close()
		log = LogInfo(user=current_user.username,hostname=datainfo.hostname,command=command1)
		db.session.add(log)
		db.session.commit()
		#在本地压缩
		command = 'cd '+ os.path.abspath('.')+os.sep+'back && '+command2
		print command
		os.system(command)
		#return redirect(request.url_root+'back'+os.sep+str(zipfile))
		#下载文件到本地
		return send_from_directory(os.path.abspath('.')+os.sep+'back',backfilename,as_attachment=True)
	else:
		return abort(403)


##############################################################
#备份所选项目
# @main.route('/mysqldump',methods=['POST','GET'])
# @login_required
# def myslqdump():
# 	id = request.form['dbid']
	#根据id获取数据库信息
	# datainfo = DBInfo.query.filter_by(id=id).first()
	# serverip = datainfo.hostip
	# serveruser = datainfo.hostuser
	# serverport = datainfo.hostport
	# serverpath = datainfo.hostpasspath
	# dbuser = datainfo.dbuser
	# dbpass = datainfo.dbpass
	# dbhost = datainfo.dbhost
	# dbname = datainfo.dbname

	# user = User.query.filter_by(id=current_user.id).first()
	# dbs = []
	# for i in user.roles:
	# 	dbs.append(i.id)
	# # if int(id) in dbs:
	# if request.method == 'POST':
	# 	#备份文件命名
	# 	backfilename = "%s.%s.sql" % (dbname,time.strftime('%Y%m%d%H%M%S'))
	# 	#压缩后文件
	# 	zipfile = backfilename+'.zip'
	# 	#备份命令
	# 	command1 = "mysqldump -u%s -p%s --default-character-set utf8 -h%s %s > %s"  % (dbuser,dbpass,dbhost,dbname,backfilename)
	# 	#压缩命令
	# 	command2 = "zip -P 'RD1111' %s %s"  % (zipfile,backfilename)
	# 	# ssh = ssh_connection(serverip,serveruser,serverpass)
	# 	#paramiko秘钥方式登录服务器
	# 	ssh = ssh_key_connection(serverip, serveruser,int(serverport), os.path.abspath('.')+os.sep+serverpath)
	# 	print command1
	# 	#执行备份命令
	# 	ssh.exec_command(command1)
	# 	#ssh.exec_command(command2)
	# 	ssh.close()
	# 	#paramiko sftp秘钥登录服务器
	# 	sftpssh = ssh_key_downfile(serverip, serveruser, int(serverport), os.path.abspath('.')+os.sep+serverpath)
	# 	print os.path.abspath('.')+os.sep+'back'+os.sep+backfilename
	# 	#下载刚刚备份的文件
	# 	sftpssh.get(backfilename, os.path.abspath('.')+os.sep+'back'+os.sep+backfilename)
	# 	sftpssh.close()
	# 	#在本地压缩
	# 	command = 'cd '+ os.path.abspath('.')+os.sep+'back && '+command2
	# 	print command
	# 	os.system(command)
	# 	#return redirect(request.url_root+'back'+os.sep+str(zipfile))
	# 	#下载文件到本地
	# 	return send_from_directory(os.path.abspath('.')+os.sep+'back',backfilename,as_attachment=True)
	# else:
	# 	return render_template('selectforiden.html')