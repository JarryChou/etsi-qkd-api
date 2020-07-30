Installing Apache
=================

Deploying the API on the Flask built-in Werkzeug server is fine. However, Werkzeug is mainly built for testing purposes,
and if we want to deploy the API for real-world use, we will need to utilize production-ready servers such as `Apache <www.apache.org>`_
or `NGINX <www.nginx.com>`_. For our purposes we choose Apache. We assume the user is running a Linux OS. To install,

.. code-block::

    $ sudo apt-get update
    $ sudo apt-get install apache2

There is some configuration to do with Apache. First, go to ``app.wsgi`` located in your repository and add your repository
to the system path:

.. code-block::

    ...
    sys.path.insert(0, '/path/to/etsi-qkd-api/')
    ...

We want the API to be accessed using secure HTTPS connections, so we need to provide a SSL certificate to the Apache server.
A certificate can be obtained in many ways--through an official certificate authority (CA), or it can be self-created using OpenSSL. Once created,
you will need to give Apache access to the certificates. This can be set in the ``/etc/apache2/sites-available/etsi-qkd-api.conf`` file, which looks like
this on my Ubuntu machine:

.. image:: /images/apacheconf.png

Note the SSLParameters section. This will vary depending on how you configure your SSL certificates, but this should give you a rough idea. The configuration
you see is using SSL certificates verified by Senetas' CM7 software, so that the API can interface with their virtual encryptors. Also take note of the ServerName,
which should be your desired server IP, and the relevant WSGI parameters such as the Python path to your virtual environment.

Next, we can proceed to run the Apache server.

.. code-block::

    $ sudo a2enmod wsgi
    $ sudo apachectl -f /etc/apache2/apache2.conf -k start

Then navigate to your web browser with the correct IP address and check that the API calls work. You should notice that the connection is now
secured over HTTPS.