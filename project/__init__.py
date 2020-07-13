from flask import Flask
from project.kme import KME


app = Flask(__name__)

from project import routes


kme_instance = KME("/home/alvin/PycharmProjects/etsi-qkd-api/key_files")
#kme_instance = KME("key_files")
app.config['kme'] = kme_instance
