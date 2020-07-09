from project import app, KME


kme_instance = KME("etsi-qkd-api/key_files")
#kme_instance = KME("key_files")
app.config['kme'] = kme_instance

if __name__ == '__main__':
    app.run(host="10.0.1.30", port='443', debug=False, ssl_context='adhoc')
