from flask import render_template, flash, redirect
from app import app
from forms import LoginForm,ShowForm
from models import User

@app.route('/')
@app.route('/index')
def index():
	pass
