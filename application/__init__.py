from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session
from flask_login import LoginManager
from application.extensions import bcrypt
import pymongo

app = Flask(__name__)

app.config["SECRET_KEY"]= "a0b189f94b26d9484a00ac686430f5bf3bd8fff6"

conn = "mongodb+srv://atharvarajpurkar03:athu9184@cluster1.kx71t.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"

client = pymongo.MongoClient(conn, serverSelectionTimeoutMS=8000)
db = client.db

# Session Configuration
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem to store sessions
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # Protect against cookie tampering
app.config['SESSION_KEY_PREFIX'] = 'todo_'  # Prefix for session keys
Session(app)  # Initialize session

login_manager = LoginManager(app)
login_manager.login_view = "login"

bcrypt.init_app(app)

from application import routes


