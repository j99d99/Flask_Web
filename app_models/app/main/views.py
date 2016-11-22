from flask import render_template, flash, redirect,url_for,request,send_from_directory
from . import main
#from forms import .....
#from ..models import ...
from .. import db

@main.route('/')
@main.route('/index')
def index():
	pass
