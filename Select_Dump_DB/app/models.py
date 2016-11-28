from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
import datetime


user_role = db.Table('user_dbs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('dbs_id', db.Integer, db.ForeignKey('dbs.id')),
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(120), index = True, unique = True)
    role  = db.Column(db.String(64),default='1')
    roles = db.relationship('DBInfo',secondary=user_role,backref=db.backref('user',lazy='dynamic'),lazy='dynamic')

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
        
class DBInfo(db.Model):
    __tablename__ = 'dbs'
    id = db.Column(db.Integer,primary_key=True)
    hostname = db.Column(db.String(32),index = True)
    hostip = db.Column(db.String(32))
    hostport = db.Column(db.Integer)
    hostuser = db.Column(db.String(64))
    hostpasspath = db.Column(db.String(64))
    dbhost = db.Column(db.String(64),index = True, unique = True)
    dbname = db.Column(db.String(64))
    dbuser = db.Column(db.String(64))
    dbpass = db.Column(db.String(64))




#python manager.py db init
#python manager.py db migrate -m 'mesages'
#python manager.py db upgrade