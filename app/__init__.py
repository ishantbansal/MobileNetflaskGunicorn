from flask import Flask
from flask import render_template, jsonify, Flask, redirect, url_for, request
import random
import os
import tensorflow as tf
from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.layers import Activation, Dense
from keras.models import load_model
from keras.applications.mobilenet import preprocess_input, decode_predictions
from keras.applications import imagenet_utils, mobilenet
import numpy as np
import requests
import datetime

app = Flask(__name__, instance_path = '/home/ishant/Desktop/flask/app/static')

# Setup the app with the config.py file
app.config.from_object('app.config')

# Setup the logger
from app.logger_setup import logger

# Setup the database
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the mail server
from flask.ext.mail import Mail
mail = Mail(app)

#model initialize
model= mobilenet.MobileNet(weights='/home/ishant/Desktop/flask/app/static/model/mobilenet224.h5')
graph = tf.get_default_graph()


# Setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension(app)

# Setup the password crypting
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import the views
from app.views import main, user, error
app.register_blueprint(user.userbp)

# Setup the user login process
from flask.ext.login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()

from app import admin
