from __main__ import app
from flask import jsonify, request


@app.route('/api/v1/keys/<id>/enc_keys', methods=['GET', 'POST'])
def get_key(id):

    try:
        if request.method == 'POST':
            req_data = request.get_json()
            number = req_data['number']
            size = req_data['size']
        else:
            number = request.args.get('number')
            size = request.args.get('size')

        key_container = app.config['kme'].get_key(number, size)

    except KeyError:
        return 'Bad Request Format: Missing parameters in POST request', 400
    except ValueError:
        return 'Requesting for more keys than there are available', 400

    return jsonify(key_container)


@app.route('/api/v1/keys/<id>/status', methods=['GET'])
def get_status(id):
    return jsonify(app.config['kme'].get_status())


@app.route('/api/v1/keys/<id>/dec_keys', methods=['GET', 'POST'])
def get_key_with_id(id):
    if request.method == 'POST':
        key_id = request.args.get('key_ID')
    else:
        req_data = request.get_json()
        key_id = req_data['keys_IDs']

    key_container = app.config['kme'].get_key_with_id(key_id)
    return jsonify(key_container)

