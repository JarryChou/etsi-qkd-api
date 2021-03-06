# ETSI QKD API
This is an implementation of the ETSI QKD API.

## Online docs
A comprehensive documentation is hosted at **https://speqtral.github.io/etsi-qkd-api/**, which covers installation, running with Senetas's CV1000 encryptor VMs, code documentation, design principles and open areas of improvement. 

## Build docs locally

If you wish to build the docs locally, clone the repository and install the requirements in a virtual environment

```
$ cd etsi-qkd-api
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Then proceed to build the docs in ``docsrc``:

```
$ cd docsrc
$ make html
```

You will notice several warnings--you can ignore them as they do not affect any functionality. The htmls that are built are located in ``docsrc/_build/html``. To open the docs in your browser while in ``docsrc``, do 

```
$ google-chrome _build/html/index.html
```

or if you use Firefox,

```
$ firefox _build/html/index.html
```

## Publishing docs to Github Pages

If the user has modified the docs and wishes to publish it to Github Pages, the user must copy *all* contents located in ``docsrc/_build/html`` created by ``make html``, and paste them into ``docs`` before pushing it to ``master``. Github Pages automatically reads html content off ``master/docs`` and publishes it on the webpage.
