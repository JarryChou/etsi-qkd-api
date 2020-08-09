Quickstart
==========

First, start by cloning the repository, then installing the pre-requisites in a virtual environment (recommended):

.. code-block::

    $ git clone https://github.com/SpeQtral/etsi-qkd-api.git
    $ cd etsi-qkd-api
    $ python3 -m venv venv
    $ pip install -r requirements.txt

Next, we need to configure the KME. There are two steps to this.

1. Navigate to the ``config.ini`` file located in the ``/api`` folder. Update ``key_file_path`` with the **ABSOLUTE** file
path to the folder containing the qcrypto key files. You can ignore step b) denoted in the file as we are not yet looking to deploy
the API on an Apache server.

2. Navigate to ``__init__.py`` in the same folder and update variable ``config_path`` with the ABSOLUTE file path
to ``config.ini`` you edited above.

Then deploy the Flask app with the built-in Werkzeug web server:

.. code-block::

    $ python app.py
     * Serving Flask app "api" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Navigate to http://127.0.0.1:5000/ on your web browser and you should be greeted with a message: "Hello World from SpeQtral's ETSI QKD API!".

ETSI API Calls
++++++++++++++

Now that Hello World is working, let's check the various API calls specified by the ETSI document. Ensure that you have valid qcrypto key files in the key file path
you specified earlier. Navigate to http://127.0.0.1:5000/api/v1/keys/_ID_/status, where _ID_ can be *any number you want* (it is supposed
to be the IP of the SAE, but for now I have programmed it to allow any arbitrary ID). You should see something like

.. code-block:: json

    {

        "key_size": 32,
        "master_SAE_ID": "10.0.1.10",
        "max_SAE_ID_count": 0,
        "max_key_count": 3002,
        "max_key_per_request": 10,
        "max_key_size": 1024,
        "min_key_size": 32,
        "slave_SAE_ID": null,
        "source_KME_ID": "10.0.1.30",
        "stored_key_count": 3002,
        "target_KME_ID": "10.0.1.40"

    }

The returned JSON provides information such as the number of stored keys, minimum key size etc. This is in adherence to the ETSI API's
``Get status`` function call.

To retrieve keys, let us call the ``Get key`` method to retrieve a single key of size 32bits (each key in qcrypto is 32bits). Navigate to http://127.0.0.1:5000/api/v1/keys/2/enc_keys.
You should see something like

.. code-block:: json

    {

        "keys": [
            {
                "key": "HgV54g==",
                "key_ID": "e3e70682-c209-4cac-629f-6fbed82c07cd"
            }
        ]

    }

which adheres to the ETSI key container specification containing a single key. The key is supplied in ``base64`` format, and the key ID as a UUID.
Now if we call ``Get status`` again, you should see ``stored_key_count`` updated:

.. code-block:: json

    {

        ...
        "stored_key_count": 3001,
        ...

    }

To retrieve multiple keys, you can pass the desired number and size of each key in a ``GET`` or ``POST`` request. We will demonstrate a ``GET`` request here; a ``POST``
request can be done using `Postman <https://www.postman.com>`_. To obtain 3 keys of size 128bits, navigate to http://127.0.0.1:5000/api/v1/keys/2/enc_keys?number=3&size=128.

.. code-block:: json

    {

        "keys": [
            {
                "key": "XC0Kvi+6A7Ropi2rqRZDSQ==",
                "key_ID": "f728b4fa-4248-5e3a-0a5d-2f346baa9455+eb1167b3-67a9-c378-7c65-c1e582e2e662+f7c1bd87-4da5-e709-d471-3d60c8a70639+e443df78-9558-867f-5ba9-1faf7a024204"
            },
            {
                "key": "52RFCZcFVLODleAe/7FmNQ==",
                "key_ID": "23a7711a-8133-2876-37eb-dcd9e87a1613+1846d424-c17c-6279-23c6-612f48268673+fcbd04c3-4021-2ef7-cca5-a5a19e4d6e3c+b4862b21-fb97-d435-8856-1712e8e5216a"
            },
            {
                "key": "WknxA6QiLwcaS6dpb5lP6Q==",
                "key_ID": "259f4329-e6f4-590b-9a16-4106cf6a659e+12e0c8b2-bad6-40fb-1948-8dec4f65d4d9+5487ce1e-af19-922a-d9b8-a714e61a441c+5a921187-19c7-8df4-8f4f-f31e78de5857"
            }
        ]

    }

We see 3 keys returned, and as 128bit keys can be formed by concatenating 4 32bit keys, the ``key_ID`` of each key is formed by appending
the UUIDs of 4 keys, separated by a '+' delimiter. Another check with ``Get status`` should show the key count updated accordingly.
