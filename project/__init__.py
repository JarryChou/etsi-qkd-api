from flask import Flask
from project.kme import kme


app = Flask(__name__)

from project import routes

