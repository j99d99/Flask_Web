from flask import render_template, flash, redirect,url_for,request,send_from_directory
from . import auth
#from forms import .....
#from ..models import ...
from .. import db

@auth.route('/')
@auth.route('/index')
def index():
	pass
