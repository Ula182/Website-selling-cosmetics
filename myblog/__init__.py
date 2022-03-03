import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'web'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

from myblog import routes