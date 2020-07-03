from flask import Flask
from project.kme import KME


app = Flask(__name__)

from project import routes

