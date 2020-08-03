.. etsi-qkd-api documentation master file, created by
   sphinx-quickstart on Fri Jul 24 14:41:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to etsi-qkd-api's documentation!
========================================

This is an implementation of the `ETSI QKD API <https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_qkd014v010101p.pdf>`_.
The API implementation is contained within the ``api`` module that has three submodules shown below. It uses the `Flask <flask.palletsprojects.com>`_
framework and is hosted on an `Apache <www.apache.org>`_ web server.

.. autosummary::
   :toctree: modules

    api.kme
    api.helper
    api.routes

Overview
========
From a high-level perspective, the ``etsi-akd-api`` contains several different folders. The ``api`` folder is where the
bulk of the QKD API logic is contained. The ``chat-app`` folder contains a simple GUI-based chat app implemented using PyQt, the Python
implement of the popular `Qt <https://www.qt.io/>`_ GUI framework. The chat app makes requests to the
QKD API as a minimal working demo. The ``tests`` folder contains unit tests for several of the API functions defined in ``api``.
The ``docs`` and ``docsrc`` folders contain the build and source files for the documentation, which is what you are reading now.

``api.routes`` - handles the URL routing when the API is called. These URLs are defined in adherence to the ETSI API, which can
be verified by referring to the ``@app.route()`` Flask decorators above every function definition in the source code.

``api.kme`` - contains the ``KME`` class, whose methods are called by ``api.routes`` when the API is called by a user. The class
contains most of the logic for handling and manipulating qcrypto keys, but will delegate some of logic to the ``api.helper``
functions.

``api.helper`` - a collection of convenient helper functions that aid primarily in retrieval of keys from qcrypto key files, and conversion
between various data types such as ``str``, ``int`` or ``bytes`` and so on.

.. toctree::
   :caption: Tutorial :
   :maxdepth: 2
   :glob:
   :numbered:

   contents/*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
