from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = '1f0cd60a6b15c76009c7f5b8c5eb5259'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

# Absolute Path to api
absolute_path_to_api="/home/harsha/Desktop/schools/dnd-demo/api/"
# Paths to other folders
pickleFolder =absolute_path_to_api+"picklesFolder/"

#Routes
from api import routes

