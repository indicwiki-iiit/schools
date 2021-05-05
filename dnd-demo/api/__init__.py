from flask import Flask

app = Flask(__name__)


pathToData = '/media/harsha/UDrive/2.IndicWiki/schools/curDir/data/'

#Routes
from api import routes

