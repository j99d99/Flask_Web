from . import db
from werkzeug.security import  generate_password_hash,check_password_hash
from . import login_manager
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    rl_name = db.Column(db.String(64),index=True, unique = True)
    username = db.Column(db.String(64),index=True,unique = True)
    password_hash = db.Column(db.String(120), index=True, unique=True)
    roles = db.Column(db.SmallInteger, default = '0')
    role_status = db.Column(db.SmallInteger, default = '0')
    # user_db = db.relationship('DBInfo', secondary=user_db, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    # user_pro = db.relationship('Pros', secondary=user_pros, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  

class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(64),index=True,unique=True,)
    ipaddress = db.Column(db.String(64),index=True,unique=True,nullable=False)
    ssh_user = db.Column(db.String(32),default = 'root')
    general_user = db.Column(db.String(32),default = 'www')
    ssh_port = db.Column(db.SmallInteger,default = '22')
    # type_value = db.Column(db.SmallInteger,default = '0')
    ssh_passwd = db.Column(db.String(128))
    # ssh_key_path = db.Column(db.String(128))
    projecttype = db.Column(db.String(64),default = None)
    comment = db.Column(db.String(9999),default = None)
    #domaininfo = db.Column(db.String(64),default = None)

    # def to_json(self):
    #     return dict(id=self.id,hostname=self.hostname,ipaddress=self.ipaddress,ssh_user=self.ssh_user,ssh_port=self.ssh_port,type_value=self.type_value,ssh_passwd=self.ssh_passwd,ssh_key_path=self.ssh_key_path)    

class  ConfigInfo(db.Model):
    __tablename__ = 'configinfo'
    id = db.Column(db.Integer,primary_key=True)
    modelname = db.Column(db.String(64))
    modelpath = db.Column(db.String(64))
    modelcodepath = db.Column(db.String(64))
    modellogpath = db.Column(db.String(64))
        

#python manager.py db init
#python manager.py db migrate -m 'mesages'
#python manager.py db upgrade
