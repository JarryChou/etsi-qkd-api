from flask import Flask
from api.kme import KME


app = Flask(__name__)

from api import routes

# **********************************CHANGE ABSOLUTE PATH TO config.ini HERE*************************************
config_path = "/home/alvin/PycharmProjects/etsi-qkd-api/api/config.ini"
# ***************************************************************************************************************

kme_instance = KME(config_path)
app.config['kme'] = kme_instance
