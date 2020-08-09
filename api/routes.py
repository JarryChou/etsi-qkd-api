"""Functions that handle routing for the Flask web server hosting the API.
"""
from flask import jsonify, request
from api import app
import sys


@app.route('/')
def home():
    return "Hello World from SpeQtral's ETSI QKD API!"


@app.route('/api/v1/keys/<id>/enc_keys', methods=['GET', 'POST'])
def get_key(id):

    try:
        if request.method == 'POST':
            # POST returns number and size in int
            req_data = request.get_json()
            number = req_data['number']
            size = req_data['size']
        else:
            # GET returns arguments in string format
            number = request.args.get('number')
            size = request.args.get('size')

            # convert from string to int.
            # if number or size is None, int(None) will throw TypeError
            if number is not None:
                number = int(number)

            if size is not None:
                size = int(size)

        if size is not None and size % 32 != 0:
            return 'Key size not multiple of 32 bits', 400

        key_container = app.config['kme'].get_key(number, size)

    except KeyError:
        return 'Bad Request Format: Missing parameters in POST request', 400
    except ValueError:
        return 'Requesting for more keys than there are available', 400

    sys.stdout = open('/home/alvin/get_output.logs', 'a')
    print(key_container, flush=True)
    return jsonify(key_container)


@app.route('/api/v1/keys/<id>/status', methods=['GET'])
def get_status(id):
    return jsonify(app.config['kme'].get_status())


@app.route('/api/v1/keys/<id>/dec_keys', methods=['GET', 'POST'])
def get_key_with_id(id):

    try:
        if request.method == 'POST':
            req_data = request.get_json()
            key_id = req_data['key_IDs']
            # key_IDs_extension = req_data['key_IDs_extension']

            sys.stdout = open('/home/alvin/post_output.logs', 'a')
            print(req_data,flush=True)

            key_id = req_data['key_IDs']
        else:
            key_id = request.args.get('key_ID')

        key_container = app.config['kme'].get_key_with_id(key_id)

    except KeyError:
        return 'Bad Request Format: Missing parameters in POST request', 400

    return jsonify(key_container)

