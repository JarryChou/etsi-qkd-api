# from flask import Flask
# from project.kme import kme
#
#
# app = Flask(__name__)
# kme_instance = kme()
# app.config['kme'] = kme_instance
#
# import routes

from project import app, kme

kme_instance = kme()
app.config['kme'] = kme_instance

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
