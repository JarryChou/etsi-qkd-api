from project import app, KME

kme_instance = KME()
app.config['kme'] = kme_instance

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
