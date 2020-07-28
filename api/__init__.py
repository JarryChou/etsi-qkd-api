from flask import Flask
from api.kme import KME


app = Flask(__name__)

from api import routes


kme_instance = KME("/home/alvin/PycharmProjects/etsi-qkd-api/key_files")
app.config['kme'] = kme_instance
