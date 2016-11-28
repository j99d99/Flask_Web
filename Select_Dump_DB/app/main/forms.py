from flask.ext.wtf import Form
from wtforms import TextField, BooleanField ,StringField, SubmitField,PasswordField,IntegerField
from wtforms.validators import Required,DataRequired

class UserForm(Form):
	username = TextField('username',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
    
class DBForm(Form):
    hostname = TextField('hostname',validators=[DataRequired()])
    hostip = TextField('hostip',validators=[DataRequired()])
    hostuser = TextField('hostuser',validators=[DataRequired()])
    hostport = IntegerField('hostuser',validators=[DataRequired()])
    hostpasspath = PasswordField('hostpasspath',validators=[DataRequired()])
    dbhost = TextField('dbhost',validators=[DataRequired()])
    dbname = TextField('dbname',validators=[DataRequired()])
    dbuser = TextField('dbuser',validators=[DataRequired()])
    dbpass = TextField('dbpass',validators=[DataRequired()])

class CommandForm(Form):
    command = TextField('command',validators=[DataRequired()])

