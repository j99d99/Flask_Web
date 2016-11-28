#coding: utf8
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required, DataRequired, Length

class LoginUser(Form):
    username = StringField('Username', validators=[
                           DataRequired(), Length(6, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Login')