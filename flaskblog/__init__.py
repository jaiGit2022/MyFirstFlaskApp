import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jai:root@localhost/testing'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jkishan421@gmail.com'
app.config['MAIL_PASSWORD'] = '...'
mail = Mail(app)


from flaskblog.users.routes import users
from flaskblog.main.routes import main
from flaskblog.tasks.routes import tasks

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(tasks)
