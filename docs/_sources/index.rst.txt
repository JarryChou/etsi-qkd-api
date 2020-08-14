.. etsi-qkd-api documentation master file, created by
   sphinx-quickstart on Fri Jul 24 14:41:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to etsi-qkd-api's documentation!
========================================

This is an implementation of the `ETSI QKD API <https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_qkd014v010101p.pdf>`_.
The API implementation is contained within the ``api`` module that has three submodules shown below. It uses the `Flask <flask.palletsprojects.com>`_
framework and is hosted on an `Apache <www.apache.org>`_ web server.

Git Branches
============
Currently, the repository contains 3 branches:

``master`` - the master branch that contains a working version of the ETSI API.

``dev`` - a development branch where experimental features are tested before being merged with master.

``chat-demo`` - contains only the code needed to run a very minimal chat app that consumes qcrypto keys to send encrypted
messages. Keys are consumed locally for the chat app--the web server functionality has been stripped from this branch for simplicity.

Folders
=======
There are several main folders in ``master`` that are relevant to the functionality of the API. The ``api`` folder is where the
bulk of the QKD API logic is contained. ``key_files`` is where the qcrypto key files are stored by default, although this is left up to the user
and can be changed. The ``tests`` folder contains unit tests for several of the API functions defined in ``api``.
The ``docs`` and ``docsrc`` folders contain the build and source files for the documentation, which is what you are reading now.


Documentation
=============
.. autosummary::
   :toctree: modules

    api.kme
    api.helper
    api.crawler
    api.routes

.. toctree::
   :caption: Guides
   :glob:
   :numbered:

   contents/quickstart.rst
   contents/api_description
   contents/apache.rst
   contents/senetas_vm.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
