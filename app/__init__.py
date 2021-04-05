from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(Config)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'COMP3161FinalProject'
#db = SQLAlchemy(app)
mysql = MySQL(app)
from app import views