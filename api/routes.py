"""Functions that handle routing for the Flask web server hosting the API.
"""
from flask import jsonify, request
from api import app
import sys


@app.route('/')
def home():
    """
    Hello World for API set as the 'home page URL'.

    Return
    ------
    str
        Returns *"Hello World from SpeQtral's ETSI QKD API!"* if API is running and called correctly.
    """
    return "Hello World from SpeQtral's ETSI QKD API!"


@app.route('/api/v1/keys/<id>/enc_keys', methods=['GET', 'POST'])
def get_key(id):
    """
    Method for getting key, corresponding to ``Get key`` in ETSI standard. Both GET and POST requests are allowed.

    Parameters
    ----------
    id: str
        The ID (typically the IP address) of the caller. Currently any ID is allowed, hence this parameter is unused
        in the function call. Ideally in a multi-user setup where different IPs call the same API, the API should have
        logic for keeping track of different IDs, for eg. blocking off different keys for specific IPs.

    Returns
    -------
    json
        Key container containing the requested keys and key IDs, corresponding to the ETSI standard.
    """
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
    """
    Method for getting the status of the KME. Corresponds to ``Get status`` method in the ETSI standard/

    Parameters
    ----------
    id: str
        ID of the caller.

    Returns
    -------
    json
        Container containing status data formatted according to ETSI standard.
    """
    return jsonify(app.config['kme'].get_status())


@app.route('/api/v1/keys/<id>/dec_keys', methods=['GET', 'POST'])
def get_key_with_id(id):
    """
    Method for getting key given the key IDs, corresponding to ``Get key with key IDs`` method in the ETSI standard.

    Parameters
    ---------
    id: str
        ID of the caller.

    Returns
    -------
    json
        Key container containing the requested keys and key IDs, corresponding to the ETSI standard.
    """
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

