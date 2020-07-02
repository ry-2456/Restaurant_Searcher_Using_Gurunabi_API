from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db"

db = SQLAlchemy(app)

from rest_searcher import views
