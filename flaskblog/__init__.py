from flask import Flask, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail



app = Flask(__name__)

app.config['SECRET_KEY'] = "47cbc83e5d0ca093b0f8fb560178904c"#unless and until form will render this secret key the request will not met
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db =SQLAlchemy(app)

app.app_context().push()

bcrypt=Bcrypt(app)
login_manager=LoginManager(app)#maintain session

mail = Mail(app) # instantiate the mail class 
   
# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '####'
app.config['MAIL_PASSWORD'] = '####'
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 


from flaskblog.route import *#running route page
