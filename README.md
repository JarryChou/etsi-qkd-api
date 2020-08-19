# ETSI QKD API

This is an implementation of the ETSI QKD API. A comprehsensive documentation is hosted at https://speqtral.github.io/etsi-qkd-api/, which covers installation, code documentation, design principles and open areas of improvement. If you wish to build the docs locally, clone the repository and install the requirements in a virtual environment

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
