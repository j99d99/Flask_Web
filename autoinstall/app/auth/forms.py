#coding: utf8
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required, DataRequired, Length

class LoginUser(Form):
    # realname = SelectField('realname',validators=[DataRequired()])
    user_name = StringField('Username', validators=[
                           DataRequired(), Length(6, 64)])
    user_password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('remember me')
    submit = SubmitField('Login')
