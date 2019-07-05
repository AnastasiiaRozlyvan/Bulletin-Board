from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from ads.blueprint import ads

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

app.register_blueprint(ads, url_prefix='/board')
